# Generated by Django 4.2.5 on 2023-09-19 15:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_profile", "0003_userprofile_first_name_userprofile_last_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="email",
            field=models.EmailField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
