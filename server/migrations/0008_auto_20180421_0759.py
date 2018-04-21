# Generated by Django 2.0.2 on 2018-04-21 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0007_auto_20180421_0739'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagname', models.CharField(default='[Undefinded]', max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='hackathon',
            name='tags',
            field=models.ManyToManyField(related_name='tag_hackathon', to='server.Tag', verbose_name='Теги'),
        ),
    ]
