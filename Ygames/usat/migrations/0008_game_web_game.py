# Generated by Django 5.1.4 on 2025-01-18 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usat', '0007_alter_game_file_alter_gamepic_game_gamefile'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='web_game',
            field=models.FileField(blank=True, null=True, upload_to='web_games/'),
        ),
    ]
