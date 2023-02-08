# Generated by Django 4.1.5 on 2023-02-02 22:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_addproject_post_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addproject',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='app.project'),
        ),
    ]
