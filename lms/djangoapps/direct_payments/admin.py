from ratelimitbackend import admin
from direct_payments.models import Charge, Deposit, Comment, OnHoldPaidRegistration, UserBalance


admin.site.register(Charge)
admin.site.register(Deposit)
admin.site.register(Comment)
admin.site.register(OnHoldPaidRegistration)
admin.site.register(UserBalance)