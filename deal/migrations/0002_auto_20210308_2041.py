# Generated by Django 3.1.7 on 2021-03-08 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deals',
            name='ReceveEmail',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='deals',
            name='days',
            field=models.CharField(blank=True, choices=[('mon,tue,wed,thu,fri,sat,sun', 'Daily'), ('sat,sun', 'Weekends')], default='', max_length=100),
        ),
        migrations.AddField(
            model_name='deals',
            name='time',
            field=models.IntegerField(blank=True, choices=[(5, '5:00am'), (6, '6:00am'), (7, '7:00am'), (8, '8:00am'), (17, '5:00pm'), (21, '9:00pm'), (22, '10:00pm')], null=True),
        ),
        migrations.AlterField(
            model_name='assettypes',
            name='limit',
            field=models.IntegerField(default=10),
        ),
    ]
