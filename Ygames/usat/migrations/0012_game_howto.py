# Generated by Django 5.1.4 on 2025-01-23 16:58

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usat', '0011_remove_game_web_game_game_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='howto',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
