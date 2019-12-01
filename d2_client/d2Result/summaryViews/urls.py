from django.urls import path
from d2Result.summaryViews.initializationView import IniTializationView
from d2Result.summaryViews.detailedView import DetailedView
from d2Result.summaryViews.updateView import UpdateView
from d2Result.summaryViews.snapshotView import SnapshotView
from d2Result.summaryViews.exportView import ExportView

urlpatterns = [
    path('initialization/', IniTializationView.as_view()),
    path('detailed/', DetailedView.as_view()),
    path('update/', UpdateView.as_view()),
    path('snapshot/', SnapshotView.as_view()),
    path('export/', ExportView.as_view()),
]