# Generated by Django 3.2.8 on 2021-10-12 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_userprofile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='file',
            field=models.ImageField(upload_to='profile/'),
        ),
    ]