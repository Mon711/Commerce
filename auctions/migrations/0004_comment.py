# Generated by Django 4.1.7 on 2023-03-14 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_listing_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('itemID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemID', to='auctions.listing')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
