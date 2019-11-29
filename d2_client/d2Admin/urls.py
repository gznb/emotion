from django.urls import path
from d2Admin.views.ZloginViews import LoginView

urlpatterns = [
    path('login/', LoginView.as_view())
]