# Generated by Django 4.0.1 on 2022-12-27 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bot', '0004_alter_tguser_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tguser',
            options={'verbose_name': 'TG User', 'verbose_name_plural': 'TG Users'},
        ),
        migrations.AlterField(
            model_name='tguser',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tguser',
            name='username',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='TG USERNAME'),
        ),
        migrations.AlterField(
            model_name='tguser',
            name='verification_code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
