from django.urls import path
from d2Result.surveyViews.initializationView import InitView
from d2Result.surveyViews.trendView import TrendView
from d2Result.surveyViews.inclinationView import InclinaView
from d2Result.surveyViews.sourceDistributionView import SourceDistributeView
from d2Result.surveyViews.channelView import ChannelView
from d2Result.surveyViews.specificView import SpecificView

urlpatterns = [
    path('initialization/', InitView.as_view()),
    # path('initialization/', initializationView.Zinitialization),
    # path('channel/', channelView.Zchannel),
    path('channel/', ChannelView.as_view()),
    # path('inclination/', inclinationView.Zinclination),
    path('inclination/', InclinaView.as_view()),
    # path('source_distribution/', sourceDistributionView.ZsourceDistribution),
    path('source_distribution/', SourceDistributeView.as_view()),
    # path('specific/', specificView.Zspecific),
    # path('trend/', trendView.trend),
    path('specific/', SpecificView.as_view()),
    path('trend/', TrendView.as_view())
]