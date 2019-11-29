from django.urls import path
from d2Emotional.views import uploadActionView
from d2Emotional.views.addWordView import AddWordView
from d2Emotional.views.lookWordsView import LookWordView
from d2Emotional.views.deleteWordView import DeleteWordView
from d2Emotional.views.updateWordView import UpdateWordView
from d2Emotional.views.uploadActionView import UploadView

urlpatterns = [
    path('look_words/', LookWordView.as_view()),
    path('add_one_word/', AddWordView.as_view()),
    path('delete_one_word/', DeleteWordView.as_view()),
    path('update_one_word/', UpdateWordView.as_view()),
    # path('upload_action/', uploadActionView.upload_action),
    path('upload_action/', UploadView.as_view())
]