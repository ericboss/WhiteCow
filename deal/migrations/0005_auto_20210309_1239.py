# Generated by Django 3.1.7 on 2021-03-09 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deal', '0004_auto_20210308_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adress',
            name='postal_code',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
