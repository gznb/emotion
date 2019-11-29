from django.urls import path
from d2Order.views.addView import AddOrderView
from d2Order.views.deleteView import DeleteOrderView
from d2Order.views.findView import FindAllOrderView
from d2Order.views.updateView import UpdateOrderView

urlpatterns = [
    path('add/', AddOrderView.as_view()),
    path('update/', UpdateOrderView.as_view()),
    path('delete/', DeleteOrderView.as_view()),
    path('find/', FindAllOrderView.as_view())
]
