from datetime import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books.serializers import BookDetailSerializer
from borrowings.models import Borrowing


class BorrowingReadSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer(read_only=True)
    user = serializers.CharField(read_only=True, source="user.email")

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "is_active",
            "book",
            "user",
        )
        read_only_fields = ("is_active", "actual_return_date")


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "expected_return_date",
        )

    def validate(self, attrs):
        data = super(BorrowingCreateSerializer, self).validate(attrs)
        Borrowing.validate_inventory(
            attrs["book"].inventory,
            ValidationError,
        )
        return data

    def create(self, validated_data):
        book = validated_data["book"]
        expected_return_date = validated_data["expected_return_date"]

        borrowing = Borrowing.objects.create(
            user=self.context["request"].user,
            book=book,
            expected_return_date=expected_return_date,
        )
        book.inventory -= 1
        book.save()
        return borrowing


class BorrowingReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id",)

    def validate(self, attrs):
        data = super(BorrowingReturnSerializer, self).validate(attrs)
        borrowing = self.instance

        if borrowing.actual_return_date:
            raise ValidationError(f"Borrowing {borrowing.id} already returned")
        return data

    def update(self, instance, validated_data):
        instance.actual_return_date = datetime.today().date()

        instance.book.inventory += 1
        instance.book.save()
        instance.is_active = False
        instance.save()
        return instance
