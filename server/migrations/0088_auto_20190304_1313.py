# Generated by Django 2.1.4 on 2019-03-04 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0087_auto_20190301_1424'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='installedupdate',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='installedupdate',
            name='machine',
        ),
        migrations.RemoveField(
            model_name='pendingappleupdate',
            name='machine',
        ),
        migrations.AlterUniqueTogether(
            name='updatehistory',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='updatehistory',
            name='machine',
        ),
        migrations.AlterUniqueTogether(
            name='updatehistoryitem',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='updatehistoryitem',
            name='update_history',
        ),
        migrations.DeleteModel(
            name='InstalledUpdate',
        ),
        migrations.DeleteModel(
            name='PendingAppleUpdate',
        ),
        migrations.DeleteModel(
            name='UpdateHistory',
        ),
        migrations.DeleteModel(
            name='UpdateHistoryItem',
        ),
    ]