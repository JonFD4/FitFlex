from django.contrib import admin
from .models import Order, OrderLineItem


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Allows order line items to be displayed and edited
    inline with the Order model in the Django admin.
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_price',)
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    """
    Customizes the display of the Order model in the Django admin.
    """
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number', 'date', 'order_total', 'grand_total',)
    fields = (
        'first_name', 'last_name', 'email', 'user_profile', 'order_number',
        'date', 'order_total', 'grand_total', 'original_bag',
        'stripe_pid'
    )
    list_display = (
        'order_number', 'first_name', 'last_name', 'email', 'date',
        'order_total', 'grand_total',
    )
    ordering = ('-date',)


admin.site.register(Order, OrderAdmin)
