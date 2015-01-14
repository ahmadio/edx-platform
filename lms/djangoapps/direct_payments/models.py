"""
Models for direct payments
"""
import pytz
import logging
import smtplib
import csv

from django.contrib.auth.models import User
from django.db import models, transaction
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.utils.translation import ugettext as _


from xmodule.modulestore.django import modulestore
from xmodule_django.models import CourseKeyField
from course_modes.models import CourseMode
from student.models import CourseEnrollment, UNENROLL_DONE
from shoppingcart.models import OrderItem
from shoppingcart.exceptions import (
    InvalidCartItem,
    PurchasedCallbackException,
    ItemAlreadyInCartException,
    AlreadyEnrolledInCourseException,
    CourseDoesNotExistException,
    MultipleCouponsNotAllowedException,
    RegCodeAlreadyExistException,
    ItemDoesNotExistAgainstRegCodeException,
    ItemNotAllowedToRedeemRegCodeException,
    InvalidStatusToRetire,
    UnexpectedOrderItemStatus,
)

log = logging.getLogger("direct_payments")

CHARGE_STATUSES = (
    ('approved', 'approved'),
    ('pending', 'pending'),
    ('canceled', 'canceled'),
    ('rejected', 'rejected')
)

MEDIA_ROOT = settings.MEDIA_ROOT
fs = FileSystemStorage(location=MEDIA_ROOT)

#will comment it until I find what is the problem with the return value
#def get_upload_path(instance, filename):
#    """
#    return upload path
#    """
#    return u"direct_payments/%Y/%m/%d"

class Charge(models.Model):
    """
    holds charge details
    """
    user = models.ForeignKey(User, related_name='charges')
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=30)
    currency = models.CharField(default="usd", max_length=8)  # lower case ISO currency codes
    attachment = models.ImageField(upload_to="direct_payments/%Y/%m/%d", storage=fs)
    user_notes = models.TextField(default="User didn't provide notes")
    reviewer_notes = models.TextField(default="Reviewer didn't provide notes")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32, default='pending', choices=CHARGE_STATUSES)
    is_shown = models.BooleanField(default=True)
    
    def hide(self):
        """
        change is_shown to false
        """
        self.is_shown = False
        self.save()
    
    def update_status(self, status, request):
        """
        update stauts
        """
        if status == 'approved':
            self.status = status
            # create new deposit for approved charge
            d = Deposit.objects.create(user=self.user, 
                                       charge=self, 
                                       approved_by=request.user)
            b, _created = UserBalance.objects.get_or_create(user=self.user)
            current_balance_amount = b.current_balance + self.amount
            b.current_balance = current_balance_amount
            b.save()

        
        else:
            self.status = status
            
        self.save()
    def add_comment(self, content, request):
        """
        add new comment to charge
        """
        comment = Comment.objects.create(user=request.user,
                                         charge=self,
                                         content=content)
        comment.save()
        
        
class Deposit(models.Model):
    """
    Model represinting approved charges for a user
    """
    user = models.ForeignKey(User, related_name='deposits')
    charge = models.ForeignKey(Charge)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, related_name='approved_deposits')
    
    class Meta:
        unique_together = ('user', 'charge')
        
class Comment(models.Model):
    """
    holding comments on charges entries
    """
    user = models.ForeignKey(User, related_name='charge_comments')
    charge = models.ForeignKey(Charge, related_name='comments')
    content = models.TextField(default='empty comment')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class UserBalance(models.Model):
    """
    holding user current balance
    """
    user = models.ForeignKey(User, related_name='balance', unique=True)
    current_balance = models.DecimalField(default=0, decimal_places=2, max_digits=30)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    history = models.TextField(default='{}')
    
    @classmethod
    def get_user_balance(cls, user):
        """
        get current balance for user or create a new balance record if one doesn't exist
        """
        balance, created = cls.objects.get_or_create(user=user)
        
        return balance
    
    def deduct_amount(self, amount):
        """
        subtract amount from user balance
        """
        
        self.current_balance -= amount
        self.save()
    
class OnHoldPaidRegistration(OrderItem):
    """
    onhold registrations items
    """
    course_id = CourseKeyField(max_length=128, db_index=True)
    mode = models.SlugField(default=CourseMode.DEFAULT_MODE_SLUG)
    
    
    @classmethod
    def contained_in_order(cls, order, course_id):
        """
        Is the course defined by course_id contained in the order?
        """
        return course_id in [
            item.course_id
            for item in order.orderitem_set.all().select_subclasses("onholdpaidregistration")
            if isinstance(item, cls)
        ]
    
    @classmethod
    def is_on_hold(cls, user, course_id):
        """
        Is the course defined by course_id is onhold for this user
        """
        return course_id in [
            item.course_id
            for item in cls.objects.filter(user=user, course_id=course_id, status='onhold')
            if isinstance(item, cls)
        ]
    
    @classmethod
    def get_on_hold_registrations_for_user(cls, user):
        """
        return onHoldRegistrations for given user
        """
        return [item for item in cls.objects.filter(user=user, status='onhold') if isinstance(item, cls)]
    
    @classmethod
    @transaction.commit_on_success
    def add_to_order(cls, order, course_id, mode_slug=CourseMode.DEFAULT_MODE_SLUG, cost=None, currency=None):
        """
        A standardized way to create these objects, with sensible defaults filled in.
        Will update the cost if called on an order that already carries the course.

        Returns the order item
        """
        # First a bunch of sanity checks:
        # actually fetch the course to make sure it exists, use this to
        # throw errors if it doesn't.
        course = modulestore().get_course(course_id)
        if not course:
            log.error("User {} tried to add non-existent course {} to cart id {}"
                      .format(order.user.email, course_id, order.id))
            raise CourseDoesNotExistException

        if cls.contained_in_order(order, course_id):
            log.warning("User {} tried to add PaidCourseRegistration for course {}, already in cart id {}"
                        .format(order.user.email, course_id, order.id))
            raise ItemAlreadyInCartException

        if CourseEnrollment.is_enrolled(user=order.user, course_key=course_id):
            log.warning("User {} trying to add course {} to cart id {}, already registered"
                        .format(order.user.email, course_id, order.id))
            raise AlreadyEnrolledInCourseException

        ### Validations done, now proceed
        ### handle default arguments for mode_slug, cost, currency
        course_mode = CourseMode.mode_for_course(course_id, mode_slug)
        if not course_mode:
            # user could have specified a mode that's not set, in that case return the DEFAULT_MODE
            course_mode = CourseMode.DEFAULT_MODE
        if not cost:
            cost = course_mode.min_price
        if not currency:
            currency = course_mode.currency

        super(OnHoldPaidRegistration, cls).add_to_order(order, course_id, cost, currency=currency)

        item, created = cls.objects.get_or_create(order=order, user=order.user, course_id=course_id)
        item.status = order.status
        item.mode = course_mode.slug
        item.qty = 1
        item.unit_cost = cost
        item.line_desc = _(u'On Hold Registration for Course: {course_name}').format(
            course_name=course.display_name_with_default)
        item.currency = currency
        order.currency = currency
        item.report_comments = item.csv_report_comments
        order.save()
        item.save()
        log.info("User {} added On Hold course registration {} to cart: order {}"
                 .format(order.user.email, course_id, order.id))
        return item
    
    def purchased_callback(self):
        """
        When purchased, this should enroll the user in the course.  We are assuming that
        course settings for enrollment date are configured such that only if the (user.email, course_id) pair is found
        in CourseEnrollmentAllowed will the user be allowed to enroll.  Otherwise requiring payment
        would in fact be quite silly since there's a clear back door.
        """
        if not modulestore().has_course(self.course_id):
            raise PurchasedCallbackException(
                "The customer purchased Course {0}, but that course doesn't exist!".format(self.course_id))

        CourseEnrollment.enroll(user=self.user, course_key=self.course_id, mode=self.mode)

        log.info("Enrolled {0} in paid course {1}, paid ${2}"
                 .format(self.user.email, self.course_id, self.line_cost))  # pylint: disable=no-member

    
    @property
    def csv_report_comments(self):
        """
        Tries to fetch an annotation associated with the course_id from the database.  If not found, returns u"".
        Otherwise returns the annotation
        """
#        try:
#            return PaidCourseRegistrationAnnotation.objects.get(course_id=self.course_id).annotation
#        except PaidCourseRegistrationAnnotation.DoesNotExist:
#            return u""
        return u""
    
    def put_on_hold(self):
        """
        update item status to "onhold"
        """
        self.status = 'onhold'
        self.save()