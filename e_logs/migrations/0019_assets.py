# Generated by Django 4.1.7 on 2023-03-06 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_logs', '0018_alter_morningtask_date_alter_morningtask_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('supplier', models.CharField(max_length=200)),
                ('purchase_date', models.DateField()),
                ('expiration', models.DateField()),
                ('isAlerted', models.BooleanField()),
            ],
        ),
    ]
