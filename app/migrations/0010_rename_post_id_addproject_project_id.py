# Generated by Django 4.1.5 on 2023-02-03 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_addproject_id_alter_addproject_post_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addproject',
            old_name='post_id',
            new_name='project_id',
        ),
    ]
