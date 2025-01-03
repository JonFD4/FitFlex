from django.urls import path
from . import views

urlpatterns = [
    path('', views.bag_view, name='bag'),
    path('add/<item_id>', views.add_to_bag, name='add_to_bag'),
    path(
        'remove/<int:item_id>/',
        views.remove_from_bag,
        name='remove_from_bag'
    ),
]
