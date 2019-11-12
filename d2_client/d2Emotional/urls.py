from django.urls import path
from d2Emotional.views import lookWordsView, addWordView, deleteWordView, updateWordView

urlpatterns = [
    path('look_words/', lookWordsView.ZlookWordsView),
    path('add_one_word/', addWordView.ZaddWord),
    path('delete_one_word/', deleteWordView.ZdeleteWord),
    path('update_one_word/', updateWordView.ZupdateWord)
]