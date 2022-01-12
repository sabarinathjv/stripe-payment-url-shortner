# Generated by Django 4.0.1 on 2022-01-12 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('project_name', models.CharField(max_length=200)),
                ('url', models.URLField(blank=True, null=True)),
                ('amount', models.IntegerField(default=0)),
            ],
        ),
    ]
