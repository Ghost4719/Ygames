# Generated by Django 5.1.4 on 2025-01-18 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usat', '0008_game_web_game'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='web_game',
            new_name='game_zip',
        ),
        migrations.AddField(
            model_name='game',
            name='extracted_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
