# Generated by Django 4.0.1 on 2022-12-27 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tguser',
            options={'verbose_name': 'Telegram пользователь', 'verbose_name_plural': 'Telegram пользователи'},
        ),
    ]