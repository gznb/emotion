from django.urls import path
from d2Result.summaryViews import initializationView, detailedView, downloadView, updateView
from d2Result.summaryViews.initializationView import IniTializationView
from d2Result.summaryViews.detailedView import DetailedView
from d2Result.summaryViews.updateView import UpdateView

urlpatterns = [
    path('initialization/', IniTializationView.as_view()),
    # path('initialization/', initializationView.Zinitialization),
    path('detailed/', DetailedView.as_view()),
    # path('detailed/', detailedView.Zdetailed),
    path('download/', downloadView.Zdownload),
    path('update/', UpdateView.as_view())
    # path('update/', updateView.Zupdate),
]