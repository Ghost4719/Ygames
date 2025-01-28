# Generated by Django 5.1.4 on 2025-01-28 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usat', '0015_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='genre',
            field=models.CharField(choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Role_Playing', 'Role-Playing'), ('Simulation', 'Simulation'), ('Strategy', 'Strategy'), ('Sports', 'Sports'), ('Puzzle', 'Puzzle'), ('Racing', 'Racing'), ('Fighting', 'Fighting'), ('Horror', 'Horror'), ('Other', 'Other')], default='Action', max_length=12),
        ),
    ]
