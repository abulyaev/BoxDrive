# Generated by Django 3.1.6 on 2021-06-14 14:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('boxdriveapp', '0007_alter_document_cur_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='upload_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
