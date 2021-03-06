# Generated by Django 2.0.7 on 2018-07-24 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_section_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140)),
                ('slug', models.SlugField(max_length=140)),
                ('content', models.TextField()),
                ('tags', models.TextField(blank=True, null=True)),
                ('enabled', models.BooleanField(default=False)),
                ('published', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='section',
            name='model_name',
            field=models.CharField(blank=True, choices=[('POST', 'Posts')], max_length=50, null=True),
        ),
    ]
