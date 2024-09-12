from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from my_app.models import Note
from my_app.serializes import NoteSerializer, NotesCreateSerialize
from users.models import User
from users.serializers import UserSerializer


# Create your views here.

# class NotesListView(APIView):
#     def post(self, request, pk):
#         # if request.data.get('username'):
#         #     username = request.data['username']#если отправить FormData
#         # username = request.POST['username']#если отправить JSON
#         note = Note.objects.get(id=pk)
#         note_serializer = NoteSerializer(note, data=request.data)
#         if note_serializer.is_valid():
#             note_serializer.save()
#             # note = Note.objects.create(**note_serializer.data)
#             # note = NoteSerializer(note)
#             return Response(note.data)
#         return Response({'Detail': 'Wrong data'}, status=422)
#
#     def get(self, request):
#         notes = Note.objects.all()
#
#         notes_serializer = NoteSerializer(notes, many=True)
#         return Response(notes_serializer.data)
#


class NotesListView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class NotesCreateAPIView(CreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NotesCreateSerialize


class NoteUpdateAPIView(UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class DeleteNoteAPIView(DestroyAPIView):
    queryset = Note.objects.all()

class NoteDetailAPIView(RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class ChangeNoteStatusView(APIView):
    @extend_schema(
        responses={204: NoteSerializer},
        methods=["POST"]
    )
    def post(self, request, pk):
        note = Note.objects.get(id=pk)
        note.status = True
        note.save()
        serialized_note = NoteSerializer(note)
        return Response(serialized_note.data, status=status.HTTP_202_ACCEPTED)

class UpdateUserView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user