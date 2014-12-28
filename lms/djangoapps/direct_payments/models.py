"""
Models for direct payments
"""

from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

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
#            create new deposit for approved charge
            d = Deposit.objects.create(user=self.user, 
                                       charge=self, 
                                       approved_by=request.user)
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
    current_balance = models.DecimalField(default=0.0, decimal_places=2, max_digits=30)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)