# Generated by Django 4.1.7 on 2023-04-02 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_user_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
