from django.db.models import F, Count
from rest_framework import viewsets

from books import permissions
from books.models import Book
from books.serializers import BookSerializer, BookListSerializers, BookDetailSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializers
        if self.action == "retrieve":
            return BookDetailSerializer
        return BookSerializer
