# Generated by Django 3.2.2 on 2021-05-14 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_review_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='video_url',
            field=models.URLField(default=None, null=True),
        ),
    ]