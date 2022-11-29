# Generated by Django 3.2.9 on 2021-12-27 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('display', '0002_auto_20211227_2110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='number',
        ),
        migrations.AddField(
            model_name='contact',
            name='phone',
            field=models.IntegerField(default='0', max_length=20),
        ),
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.TextField(),
        ),
    ]
