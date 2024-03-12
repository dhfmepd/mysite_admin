# Generated by Django 5.0.2 on 2024-03-12 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ResultData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_agent', models.CharField(max_length=100)),
                ('target_url', models.CharField(max_length=100)),
                ('soup_data', models.TextField()),
                ('result_data', models.TextField()),
                ('receipt_date', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': '수신데이터',
            },
        ),
    ]
