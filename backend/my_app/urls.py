from django.urls import path

from my_app.views import NotesListView, NotesCreateAPIView, NoteUpdateAPIView, DeleteNoteAPIView, NoteDetailAPIView, \
    ChangeNoteStatusView, UpdateUserView

urlpatterns = [
    path('list/', NotesListView.as_view()),
    path('create/', NotesCreateAPIView.as_view()),
    path('update/<int:pk>/', NoteUpdateAPIView.as_view()),
    path('delete/<int:pk>/', DeleteNoteAPIView.as_view()),
    path('<int:pk>/', NoteDetailAPIView.as_view()),
    path('update_status/<int:pk>', ChangeNoteStatusView.as_view()),
    path('update_current_user/', UpdateUserView.as_view())
]