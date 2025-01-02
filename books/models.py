from django.db import models

class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "Hard",
        SOFT = "Soft",

    title = models.CharField(max_length=100,)
    author = models.CharField(max_length=100,)
    cover = models.CharField(max_length=50, choices=CoverChoices.choices,)
    inventory = models.IntegerField()

    class Meta:
        unique_together = ('title', 'author')

    def __str__(self):
        return f"{self.title} | {self.author}"