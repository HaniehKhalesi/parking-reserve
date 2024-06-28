from django.urls import path
from . import views
 
urlpatterns = [
    path('list_parking', views.product_list, name='p_list'),
    path('parking_<int:pk>/', views.product_detail, name='p_detail'),
    path('booking/', views.ReservationView.as_view(), name='booking'),
    path('check_out/', views.check_out, name='check_out'),
]