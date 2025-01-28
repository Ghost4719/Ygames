# Generated by Django 5.1.4 on 2025-01-25 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usat', '0013_delete_custommodel_game_background_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='bg_style',
            field=models.ImageField(blank=True, null=True, upload_to='game_stylebgs/'),
        ),
        migrations.AlterField(
            model_name='game',
            name='font_family',
            field=models.CharField(default='lato', max_length=255),
        ),
    ]
