from django.urls import path

from d2Order.views import addView, deleteView, findView, updateView

urlpatterns = [
    path('add/', addView.Zadd),
    path('update/', updateView.Zupdate),
    path('delete/', deleteView.Zdelete),
    path('find/', findView.ZfindAll)
]