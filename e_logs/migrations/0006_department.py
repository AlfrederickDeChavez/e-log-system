# Generated by Django 4.1.6 on 2023-02-16 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_logs', '0005_alter_bulletin_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=200)),
                ('client', models.CharField(max_length=100)),
                ('affected_system', models.CharField(max_length=255)),
                ('attended_by', models.CharField(max_length=200)),
                ('date', models.DateField(auto_now_add=True)),
                ('time_reported', models.TimeField()),
                ('time_resolved', models.TimeField()),
                ('problem', models.TextField()),
                ('action', models.TextField()),
                ('status', models.CharField(max_length=200)),
                ('recommendation', models.TextField()),
            ],
        ),
    ]
