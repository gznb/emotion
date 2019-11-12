from django.urls import path
from .views import ZloginViews
urlpatterns = [
    path('login/', ZloginViews.Zlogin),
]