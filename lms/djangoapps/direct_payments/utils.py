"""
Helper methods for direct payments
"""
from collections import OrderedDict, defaultdict
from datetime import datetime
import uuid

from edxmako.shortcuts import render_to_string

from xmodule.modulestore.django import modulestore
from xmodule.error_module import ErrorDescriptor

def render_direct_payments_form_html(cart):
    """
    Args:
        cart (Order): The order model representing items in the user's cart.

    Returns:
        unicode: The rendered HTML form.

    """
    total_cost = cart.total_cost
    amount = "{0:0.2f}".format(total_cost)
    params = OrderedDict()

    params['amount'] = amount
    params['currency'] = cart.currency
    params['orderNumber'] = "OrderId: {0:d}".format(cart.id)

    params['reference_number'] = cart.id

    params['locale'] = 'en'
    params['signed_date_time'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    params['transaction_uuid'] = uuid.uuid4().hex
    params['payment_method'] = 'direct_payment'

    return render_to_string('direct_payments/direct_payments_form.html', {
        'params': params,
    })

def get_on_hold_registration_pairs(on_hold_registrations):
    """
    Get the relevant set of (Course, CourseEnrollment) pairs to be displayed on
    a student's dashboard.
    """
    for registration in on_hold_registrations:
        store = modulestore()
        with store.bulk_operations(registration.course_id):
            course = store.get_course(registration.course_id)
            if course and not isinstance(course, ErrorDescriptor):

                yield (course, registration)
            else:
                log.error("User {0} registration for {2} course {1}".format(
                    user.username, enrollment.course_id, "broken" if course else "non-existent course"
                ))


