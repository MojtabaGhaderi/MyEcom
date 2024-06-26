# Generated by Django 5.0 on 2024-02-11 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Backstore', '0008_remove_productmodel_category_alter_productmodel_tag_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='likes',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='productmodel',
            name='sold_counts',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='productmodel',
            name='special_offer',
            field=models.BooleanField(default=False),
        ),
    ]
