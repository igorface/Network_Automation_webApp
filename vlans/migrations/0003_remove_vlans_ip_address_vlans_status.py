# Generated by Django 4.0.2 on 2022-03-08 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vlans', '0002_rename_vlan_vlans'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vlans',
            name='ip_address',
        ),
        migrations.AddField(
            model_name='vlans',
            name='status',
            field=models.CharField(default='passive', max_length=15),
        ),
    ]
