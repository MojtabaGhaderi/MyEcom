# Generated by Django 5.0 on 2024-02-07 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProductCatalog', '0006_remove_categorymodel_lft_remove_categorymodel_rgt'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='parent',
            field=models.ManyToManyField(blank=True, null=True, related_name='children', to='ProductCatalog.categorymodel'),
        ),
    ]