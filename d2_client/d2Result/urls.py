from django.urls import path, include
urlpatterns = [
    path('survey/', include('d2Result.surveyViews.urls')),
    path('summary/', include('d2Result.summaryViews.urls')),
]