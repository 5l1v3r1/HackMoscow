# Generated by Django 2.0.2 on 2018-04-22 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20180422_0322'),
    ]

    operations = [
        migrations.AddField(
            model_name='hackathon',
            name='avatar',
            field=models.ImageField(default='unknown_img.jpg', upload_to='uploads/'),
        ),
    ]