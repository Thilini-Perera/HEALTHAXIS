# Generated by Django 3.2.15 on 2023-07-19 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.CharField(max_length=100)),
                ('item_name', models.CharField(max_length=100)),
                ('expire_date', models.DateField()),
                ('stocks', models.IntegerField()),
            ],
        ),
    ]
