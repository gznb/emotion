from django.urls import path
from d2User.views import registerView, loginView, motifyView
# 第一个使用 CBV
from d2User.views.loginView import LoginView
from d2User.views.registerView import RegisterView
from d2User.views.motifyView import MotifyView
urlpatterns = [
    path('register/', RegisterView.as_view()),
    # path('register/', registerView.Zregister),
    # 第一个CBV url 使用
    path('login/',  LoginView.as_view()),
    path('modify/', MotifyView.as_view()),
    # path('modify/', motifyView.Zmodify),
]