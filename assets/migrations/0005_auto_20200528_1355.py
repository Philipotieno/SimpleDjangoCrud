# Generated by Django 3.0.4 on 2020-05-28 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_auto_20200517_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='head',
            name='institution',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='institution_head', to='assets.Institution'),
        ),
    ]
