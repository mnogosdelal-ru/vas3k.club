# Generated by Django 3.2.13 on 2022-05-25 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_muted_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='membership_platform_type',
            field=models.CharField(choices=[('direct', 'Direct'), ('patreon', 'Patreon'), ('crypto', 'Crypto')], default='patreon', max_length=128),
        ),
    ]
