# Generated by Django 2.0.2 on 2018-04-21 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='unknown_img.jpg', upload_to='uploads/'),
        ),
    ]
