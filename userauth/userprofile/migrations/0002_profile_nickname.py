# Generated by Django 4.1.2 on 2022-12-08 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userprofile", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="nickname",
            field=models.CharField(default="", max_length=20),
        ),
    ]
