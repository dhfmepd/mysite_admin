# Generated by Django 5.0.2 on 2024-03-25 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invest', '0004_alter_note_record_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='stock_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]