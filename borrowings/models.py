from django.conf import settings
from django.db import models, transaction
from rest_framework.exceptions import ValidationError

from books.models import Book


class Borrowing(models.Model):
    borrow_date = models.DateField()
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(null=True, blank=True)
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

    @property
    def is_active(self):
        if self.actual_return_date is None:
            return True

    class Meta:
        unique_together = ("borrow_date", "actual_return_date")

    def clean(self):
        if self.book.inventory <= 0:
            return ValidationError("Current book is out of stock")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.id:
                self.full_clean()
                self.book.inventory -= 1
                self.book.save()

            elif self.id and self.actual_return_date:
                self.book.inventory += 1
                self.book.save()
        super().save(*args, **kwargs)
