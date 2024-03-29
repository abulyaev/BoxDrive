# Generated by Django 3.2.4 on 2021-06-13 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('boxdriveusersreg', '0001_initial'),
        ('boxdriveapp', '0002_alter_post_fileurl'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('file_field', models.FileField(upload_to='uploads/')),
                ('desc', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boxdriveusersreg.profile')),
            ],
        ),
    ]
