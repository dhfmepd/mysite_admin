# Generated by Django 5.0.2 on 2024-03-13 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0002_alter_resultdata_target_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultdata',
            name='func_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]