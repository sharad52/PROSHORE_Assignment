# Generated by Django 4.1.7 on 2023-03-18 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('blog_image_url', models.URLField()),
                ('author_name', models.CharField(max_length=100)),
                ('author_image_url', models.URLField()),
                ('author_designation', models.CharField(max_length=100)),
                ('reading_time', models.TimeField()),
            ],
            options={
                'verbose_name': 'Content',
                'verbose_name_plural': 'Contents',
                'db_table': 'content',
            },
        ),
    ]
