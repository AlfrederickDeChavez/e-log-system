# Generated by Django 4.1.7 on 2023-03-20 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_logs', '0028_renewedasset'),
    ]

    operations = [
        migrations.AddField(
            model_name='renewedasset',
            name='tracking_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]