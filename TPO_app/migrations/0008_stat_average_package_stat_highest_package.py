# Generated by Django 4.0.4 on 2022-06-06 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TPO_app', '0007_stat_company_visited'),
    ]

    operations = [
        migrations.AddField(
            model_name='stat',
            name='average_package',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stat',
            name='highest_package',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
