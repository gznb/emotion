from django.urls import path
from .views import lookSpiderView, addSpiderView, deleteSpiderView, updateSpiderView
urlpatterns = [
    path('look_spiders/', lookSpiderView.ZlookSpider),
    path('add_spider/', addSpiderView.ZaddSpider),
    path('delete_one_spider/', deleteSpiderView.ZdeleteSpider),
    path('update_one_spider/', updateSpiderView.ZupdateSpider),
]