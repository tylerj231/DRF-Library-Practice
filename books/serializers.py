from rest_framework import serializers

from books.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "title",
            "author",
            "cover",
            "inventory",
        )


class BookListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "inventory",
            "cover"
        )


class BookDetailSerializer(BookListSerializers):
    class Meta:
        model = Book
        fields = BookListSerializers.Meta.fields + ("cover",)
