# Generated by Django 5.0.2 on 2024-03-25 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0002_alter_note_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='record_date',
            field=models.CharField(default=20240325, max_length=8),
            preserve_default=False,
        ),
    ]
