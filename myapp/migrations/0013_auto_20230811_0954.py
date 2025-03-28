# Generated by Django 3.2.15 on 2023-08-11 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('myapp', '0012_rename_username_userr_uname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userr',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='myapp_userr_groups', to='auth.Group'),
        ),
        migrations.AlterField(
            model_name='userr',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='myapp_userr_permissions', to='auth.Permission'),
        ),
    ]
