# Generated by Django 4.1.7 on 2023-03-15 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='wathclist',
            field=models.ManyToManyField(blank=True, related_name='watchers', to='auctions.listing'),
        ),
    ]