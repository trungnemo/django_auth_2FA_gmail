# Generated by Django 4.2.5 on 2023-09-18 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_usertoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(db_index=True, max_length=255)),
                ('token', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='user_id',
            field=models.IntegerField(db_index=True),
        ),
    ]
