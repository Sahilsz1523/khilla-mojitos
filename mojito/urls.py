from django.urls import path
from . import views
urlpatterns = [
    path('index/', views.index, name='index'),
    path('cart/remove/<int:item_index>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='cart_view'),
    path('set-table-number/', views.set_table_number, name='set_table_number'),
    path('place-order/', views.place_order, name='place_order'),
    path('about/', views.about_us, name='about'),

]