# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('views', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docname', models.CharField(max_length=32)),
                ('snippet', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('preference', models.IntegerField(default=-1)),
            ],
        ),
        migrations.CreateModel(
            name='ListOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rank', models.IntegerField()),
                ('document', models.ForeignKey(to='fakesearch.Document')),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('url', models.URLField()),
                ('views', models.IntegerField(default=0)),
                ('category', models.ForeignKey(to='fakesearch.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qid', models.CharField(max_length=32)),
                ('text', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='ResultList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default=b'-', max_length=128)),
                ('doclist', models.ManyToManyField(to='fakesearch.Document', through='fakesearch.ListOrder')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expertise', models.IntegerField(default=1)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='listorder',
            name='resultlist',
            field=models.ForeignKey(to='fakesearch.ResultList'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='query',
            field=models.ForeignKey(to='fakesearch.Query'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='result_listA',
            field=models.ForeignKey(related_name='listA', to='fakesearch.ResultList', null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='result_listB',
            field=models.ForeignKey(related_name='listB', to='fakesearch.ResultList', null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='user',
            field=models.ForeignKey(to='fakesearch.UserProfile'),
        ),
    ]
