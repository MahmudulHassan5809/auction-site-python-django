# Generated by Django 3.0.8 on 2020-08-13 14:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auction', '0013_auctionsession_end_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ManyToManyField(to='auction.Category')),
                ('sub_category', models.ManyToManyField(to='auction.SubCategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]