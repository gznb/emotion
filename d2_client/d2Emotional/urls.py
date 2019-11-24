from django.urls import path
from d2Emotional.views import lookWordsView, addWordView, deleteWordView, updateWordView, uploadActionView

urlpatterns = [
    path('look_words/', lookWordsView.look_words),
    path('add_one_word/', addWordView.add_word),
    path('delete_one_word/', deleteWordView.delete_word),
    path('update_one_word/', updateWordView.update_word),
    path('upload_action/', uploadActionView.upload_action),
]