from django.urls import path
from d2Result.surveyViews import initializationView, channelView, inclinationView, sourceDistributionView, specificView, trendView

urlpatterns = [
    path('initialization/', initializationView.Zinitialization),
    path('channel/', channelView.Zchannel),
    path('inclination/', inclinationView.Zinclination),
    path('source_distribution/', sourceDistributionView.ZsourceDistribution),
    path('specific/', specificView.Zspecific),
    path('trend/', trendView.Ztrend),
]