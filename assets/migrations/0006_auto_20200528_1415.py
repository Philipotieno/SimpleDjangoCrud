# Generated by Django 3.0.4 on 2020-05-28 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_auto_20200528_1355'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='name',
            new_name='report_name',
        ),
    ]