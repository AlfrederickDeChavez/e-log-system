# Generated by Django 4.1.7 on 2023-03-24 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_logs', '0031_alter_eveningtask_date_alter_eveningtask_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='audit',
            name='modified_datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
