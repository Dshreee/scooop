# Generated by Django 3.0.6 on 2020-06-03 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20200603_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main',
            name='about',
            field=models.TextField(),
        ),
    ]
