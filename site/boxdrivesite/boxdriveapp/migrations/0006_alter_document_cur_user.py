# Generated by Django 3.2.4 on 2021-06-14 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boxdriveapp', '0005_rename_user_document_cur_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='cur_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
