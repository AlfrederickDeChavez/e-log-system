# Generated by Django 4.1.7 on 2023-03-22 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_logs', '0029_renewedasset_tracking_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='audit',
            name='asset_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='audit',
            name='status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
