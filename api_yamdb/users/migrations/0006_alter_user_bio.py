# Generated by Django 3.2 on 2023-03-31 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, default=0, verbose_name='О себе'),
            preserve_default=False,
        ),
    ]
