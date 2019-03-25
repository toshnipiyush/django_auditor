# Generated by Django 2.1 on 2019-03-25 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=251)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created On')),
                ('updated_on', models.DateTimeField(auto_now_add=True, verbose_name='Updated On')),
            ],
            options={
                'verbose_name': 'Test Model',
                'verbose_name_plural': 'Test Model',
                'db_table': 'test_model',
            },
        ),
    ]
