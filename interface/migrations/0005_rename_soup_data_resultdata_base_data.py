# Generated by Django 5.0.2 on 2024-03-13 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0004_alter_resultdata_soup_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resultdata',
            old_name='soup_data',
            new_name='base_data',
        ),
    ]
