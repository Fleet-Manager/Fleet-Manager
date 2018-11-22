from django.urls import path
from . import views

app_name = 'carts'
urlpatterns = [
    path('', views.home.as_view(), name='home'),
    path('import/', views.import_data.as_view(), name='import data'),
    path('viewer/', views.cart_viewer.as_view(), name='cart viewer'),
    path('groups/', views.cart_groups.as_view(), name='cart groups'),
]
