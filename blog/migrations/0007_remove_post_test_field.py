# Generated by Django 3.1.1 on 2020-09-20 01:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_test_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='test_field',
        ),
    ]
