# Generated by Django 3.2.4 on 2022-03-06 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_captions'),
    ]

    operations = [
        migrations.AddField(
            model_name='cont_info',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
    ]