# Generated by Django 5.0.2 on 2024-03-12 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultdata',
            name='target_url',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='resultdata',
            name='user_agent',
            field=models.CharField(max_length=200),
        ),
    ]
