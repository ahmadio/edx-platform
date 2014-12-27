from ratelimitbackend import admin
from direct_payments.models import Charge, Deposit, Comment


admin.site.register(Charge)
admin.site.register(Deposit)
admin.site.register(Comment)