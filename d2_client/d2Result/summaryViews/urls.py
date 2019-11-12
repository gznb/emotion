from django.urls import path
from d2Result.summaryViews import initializationView, detailedView, downloadView, updateView


urlpatterns = [
    path('initialization/', initializationView.Zinitialization),
    path('detailed/', detailedView.Zdetailed),
    path('download/', downloadView.Zdownload),
    path('update/', updateView.Zupdate),
]