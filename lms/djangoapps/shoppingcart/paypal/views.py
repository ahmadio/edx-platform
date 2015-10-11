import logging
import datetime
import decimal
import pytz
import paypalrestsdk
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.http import (HttpResponse, HttpResponseBadRequest, HttpResponseForbidden,
			HttpResponseRedirect, HttpResponseServerError, Http404)
from django.shortcuts import redirect
from edxmako.shortcuts import render_to_response
from shoppingcart.models import Order, CertificateItem
from shoppingcart.processors.helpers import get_processor_config
from shoppingcart.processors import process_postpay_callback
from shoppingcart.views import _get_verify_flow_redirect
 

log = logging.getLogger("shoppingcart")
AUDIT_LOG = logging.getLogger("audit")

@require_POST
@login_required
@ensure_csrf_cookie
def create_paypal_payment(request):
	"""
	"""

	cart = Order.get_cart_for_user(request.user)

	paypal_items = [{
        "name": "Course registration",
        "sku": "Course",
        "price": int(item.unit_cost), # used integer as Decimal object is not serializesed using paypalrestsdk
        "currency": "USD",
        "quantity": item.qty} 
        for item in cart.orderitem_set.all().select_subclasses()]




	# print 'direct floated : ',	 float(cart.total_cost)
	# print 'floated 2f : ', float("{0:.2f}".format(cart.total_cost))
	# print 'total_cost decimal : ', cart.total_cost
	callback_url = request.build_absolute_uri(
      reverse("shoppingcart.paypal.views.paypal_postpay_callback")
  )

  # print 'floated 2f : '
  # print float(cart.total_cost)
  # print 'total cost decimal : ' , cart.total_cost

	paypalrestsdk.configure({
	  'mode': get_processor_config().get('MODE', 'sandbox'),
	  'client_id': get_processor_config().get('CLIENT_ID', ''),
	  'client_secret': get_processor_config().get('CLIENT_SECRET', '')
	})

	payment = paypalrestsdk.Payment({
    "intent": "sale",

    # Payer
    # A resource representing a Payer that funds a payment
    # Payment Method as 'paypal'
    "payer": {
        "payment_method": "paypal"},

    # Redirect URLs
    "redirect_urls": {
        "return_url": callback_url,
        "cancel_url": callback_url},

    # Transaction
    # A transaction defines the contract of a
    # payment - what is the payment for and who
    # is fulfilling it.
    "transactions": [{

    		# custom params
    		"custom": str(cart.id),
    
        # ItemList
        "item_list": {
            "items": paypal_items
                },

        # Amount
        # Let's you specify a payment amount.
        "amount": {
            "total": int(cart.total_cost),
            "currency": "USD"},
        "description": "This is the payment for Syasi.org course registration."}]})
	
	# cart.start_purchase()

	# Create Payment and return status
	if payment.create():
	    # print("Payment[%s] created successfully" % (payment.id))
	    # Redirect the user to given approval url
	    for link in payment.links:
	        if link.method == "REDIRECT":
	            # Convert to str to avoid google appengine unicode issue
	            # https://github.com/paypal/rest-api-sdk-python/pull/58
	            redirect_url = str(link.href)
	            # print("Redirect for approval: %s" % (redirect_url))
	            return redirect(redirect_url)
	else:
	    print("Error while creating payment:")
	    print(payment.error)
	    return HttpResponse(payment.error)
 

@csrf_exempt
# @require_POST
def paypal_postpay_callback(request):
    """
    Receives the GET-back from processor.
    Mainly this calls the processor-specific code to check if the payment was accepted, and to record the order
    if it was, and to generate an error page.
    If successful this function should have the side effect of changing the "cart" into a full "order" in the DB.
    The cart can then render a success page which links to receipt pages.
    If unsuccessful the order will be left untouched and HTML messages giving more detailed error info will be
    returned.
    """

    result = process_postpay_callback(request)

    if result['success']:
        # See if this payment occurred as part of the verification flow process
        # If so, send the user back into the flow so they have the option
        # to continue with verification.

        # Only orders where order_items.count() == 1 might be attempting to upgrade
        attempting_upgrade = request.session.get('attempting_upgrade', False)
        if attempting_upgrade:
            if result['order'].has_items(CertificateItem):
                course_id = result['order'].orderitem_set.all().select_subclasses("certificateitem")[0].course_id
                if course_id:
                    course_enrollment = CourseEnrollment.get_enrollment(request.user, course_id)
                    if course_enrollment:
                        course_enrollment.emit_event(EVENT_NAME_USER_UPGRADED)

            request.session['attempting_upgrade'] = False

        verify_flow_redirect = _get_verify_flow_redirect(result['order'])
        if verify_flow_redirect is not None:
            return verify_flow_redirect

        # Otherwise, send the user to the receipt page
        return HttpResponseRedirect(reverse('shoppingcart.views.show_receipt', args=[result['order'].id]))
    else:
        request.session['attempting_upgrade'] = False
        return render_to_response('shoppingcart/error.html', {'order': result['order'],
                                                              'error_html': result['error_html']})
