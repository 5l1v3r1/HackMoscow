# Generated by Django 2.0.4 on 2018-04-21 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0015_auto_20180421_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hackratebyuser',
            name='hack',
        ),
        migrations.RemoveField(
            model_name='hackratebyuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='HackRateByUser',
        ),
    ]
