# Generated by Django 4.1.2 on 2022-12-31 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userprofile", "0004_alter_profile_description_alter_profile_iconid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="icon",
            field=models.ImageField(
                blank=True, default="default_icon.jpg", null=True, upload_to="icons"
            ),
        ),
    ]
