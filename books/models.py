from django.core.validators import MaxValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = ("Hard",)
        SOFT = ("Soft",)

    title = models.CharField(
        max_length=100,
    )
    author = models.CharField(
        max_length=100,
    )
    cover = models.CharField(
        max_length=50,
        choices=CoverChoices.choices,
    )
    inventory = models.IntegerField(validators=[MaxValueValidator(100)])

    class Meta:
        unique_together = ("title", "author")

    def __str__(self):
        return f"{self.title} | {self.author}"

    def clean(self):
        if self.inventory <= 0:
            raise ValidationError(
                {
                    "inventory": "The book is out of stock."
                    " In order to create or borrow book,"
                    " there has to be at least one copy"
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
