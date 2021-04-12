# Generated by Django 3.2 on 2021-04-11 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common_account', '0002_auto_20210410_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='veer@gmail.com', max_length=255, unique=True, verbose_name='email address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.IntegerField(choices=[(1, 'ADMIN'), (2, 'MANAGER'), (3, 'EMPLOYEE')], default=2),
        ),
    ]
