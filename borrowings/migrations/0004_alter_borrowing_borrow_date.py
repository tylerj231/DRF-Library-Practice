# Generated by Django 5.1.4 on 2025-01-03 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("borrowings", "0003_borrowing_is_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="borrowing",
            name="borrow_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
