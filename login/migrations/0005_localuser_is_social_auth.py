# Generated by Django 4.0.3 on 2022-03-22 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_alter_localuser_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='localuser',
            name='is_social_auth',
            field=models.BooleanField(default=True),
        ),
    ]
