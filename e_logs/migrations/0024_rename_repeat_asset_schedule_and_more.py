# Generated by Django 4.1.7 on 2023-03-13 03:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('e_logs', '0023_asset_repeat_audit_repeat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='repeat',
            new_name='schedule',
        ),
        migrations.RenameField(
            model_name='audit',
            old_name='repeat',
            new_name='schedule',
        ),
    ]