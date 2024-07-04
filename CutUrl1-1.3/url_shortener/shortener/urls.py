from django.urls import path
from .views import home, redirect_to_original, user_urls, edit_url, delete_url

urlpatterns = [
    path('', home, name='home'),
    path('edit/<str:short_code>/', edit_url, name='edit_url'),
    path('delete/<str:short_code>/', delete_url, name='delete_url'),
    path('my_urls/', user_urls, name='user_urls'),
    path('<str:short_code>/', redirect_to_original, name='redirect'),

]


