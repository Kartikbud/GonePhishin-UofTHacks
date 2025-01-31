# Generated by Django 4.0 on 2025-01-18 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CallLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('call_log', models.TextField()),
                ('confidence_level', models.IntegerField()),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
