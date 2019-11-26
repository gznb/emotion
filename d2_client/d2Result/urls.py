from django.urls import path, include
from d2Result.snapshotView import SnapshotView
urlpatterns = [
    path('survey/', include('d2Result.surveyViews.urls')),
    path('summary/', include('d2Result.summaryViews.urls')),
    path('snapshot/', SnapshotView.as_view())
    # path('snapshot/', Znapshot),
]