from django.urls import path

from .views import MenuTemplateView

app_name = 'menu'

urlpatterns = [
    path('menu/', MenuTemplateView.as_view(), name='main_menu'),
]
