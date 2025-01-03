from django.conf import settings
from django.db import models, transaction
from rest_framework.exceptions import ValidationError

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(
        null=True,
        blank=True
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='borrowings'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='borrowers'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "book")

    @staticmethod
    def validate_inventory(inventory, error_to_raise, ):
        if inventory == 0:
            raise error_to_raise(
                {"book":
                     "The book is out of stock."
                     " In order to create or borrow book,"
                     " there has to be at least one copy"
                 }
            )

    def clean(self):
        self.validate_inventory(
            self.book.inventory,
            error_to_raise=ValidationError
        )

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)
