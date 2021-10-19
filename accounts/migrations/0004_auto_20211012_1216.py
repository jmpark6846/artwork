# Generated by Django 3.2.8 on 2021-10-12 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_field_userprofile_job'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='job',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='', upload_to=''),
            preserve_default=False,
        ),
    ]
