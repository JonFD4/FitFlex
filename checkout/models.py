import uuid
from django.db import models
from django.db.models import Sum
from datetime import datetime
from fitflexproduct.models import WorkoutProgram as Product
from decimal import Decimal

class Order(models.Model):
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=15, unique=True, null=False, editable=False)
    is_paid = models.BooleanField(default=False)

    def generate_order_number(self):
        """
        Generate a random, unique order number for purchase identification.
        """
        current_date = datetime.now().strftime('%Y%m%d')  
        unique_id = uuid.uuid4().hex[:6].upper()  
        return f'{current_date}-{unique_id}'

    def update_total(self):
        """
        Update the grand_total as new items are added. 
        Since it's a digital product, no delivery cost is needed.
        """
        print(f"Calculated order total: {self.order_total}")
        self.grand_total = self.lineitems.aggregate(Sum('lineitem_price'))['lineitem_price__sum'] or 0.00
        current_date = datetime.now()
        if current_date.month == 10:  
            discount_percentage = 20  
            discount_amount = (discount_percentage / Decimal('100.00')) * self.grand_total
            self.order_total = self.grand_total - discount_amount
        else:
            self.order_total = self.grand_total
        self.save()  

    def save(self, *args, **kwargs):
        """ Only set the order number if it hasn't been set yet """
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)  

    def __str__(self):
        return f"Order {self.id} - {self.email}"

class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, related_name='lineitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    lineitem_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.product.name} in order {self.order.id}'
