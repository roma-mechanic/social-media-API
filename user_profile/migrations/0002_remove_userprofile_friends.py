# Generated by Django 4.2.5 on 2023-09-18 14:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user_profile", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="friends",
        ),
    ]