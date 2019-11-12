from django.urls import path
from .views import registerView, loginView, motifyView
urlpatterns = [
    path('register/', registerView.Zregister),
    path('login/', loginView.Zlogin),
    path('modify/', motifyView.Zmodify),
]