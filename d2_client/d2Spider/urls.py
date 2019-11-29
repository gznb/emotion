from django.urls import path
from d2Spider.views.addSpiderView import AddSpiderView
from d2Spider.views.deleteSpiderView import DeleteSpiderView
from d2Spider.views.lookSpiderView import LookSpiderView
from d2Spider.views.updateSpiderView import UpdateSpiderView

urlpatterns = [
    path('look_spiders/', LookSpiderView.as_view()),
    path('add_spider/', AddSpiderView.as_view()),
    path('delete_one_spider/', DeleteSpiderView.as_view()),
    path('update_one_spider/', UpdateSpiderView.as_view()),
]