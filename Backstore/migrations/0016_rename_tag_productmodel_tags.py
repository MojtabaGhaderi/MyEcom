# Generated by Django 5.0.6 on 2024-05-31 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Backstore', '0015_tagsmodel_rename_numbers_productmodel_quantity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productmodel',
            old_name='tag',
            new_name='tags',
        ),
    ]
