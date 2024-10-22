from django.contrib import admin

# Register your models here.
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
    fields = ('full_name', 'email', 'order_number', 'date', 'is_paid', 'order_total', 'grand_total')  
    list_display = ('order_number', 'full_name', 'email', 'date', 'order_total', 'grand_total', 'is_paid') 
    ordering = ('-date',) 


admin.site.register(Order, OrderAdmin)
