# Generated by Django 4.1.7 on 2023-03-09 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_logs', '0021_remove_asset_isalerted_asset_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('supplier', models.CharField(max_length=200)),
                ('purchase_date', models.DateField()),
                ('expiration', models.DateField()),
                ('action', models.CharField(max_length=200)),
                ('author', models.CharField(blank=True, max_length=200, null=True)),
                ('modified_date', models.DateField(auto_now_add=True, null=True)),
                ('modified_time', models.TimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='asset',
            name='status',
            field=models.CharField(max_length=50),
        ),
    ]
