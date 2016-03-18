# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='anslike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('user_id', models.IntegerField()),
                ('answer_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('answer_content', models.TextField()),
                ('updated_date', models.DateTimeField()),
                ('author_name', models.CharField(max_length=40)),
                ('anslike_count', models.IntegerField()),
                ('isAnonymous', models.IntegerField(null=True)),
                ('is_readed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BBS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('content', models.TextField()),
                ('author_name', models.CharField(max_length=40)),
                ('hit_count', models.IntegerField()),
                ('comment_count', models.IntegerField()),
                ('ranking', models.IntegerField()),
                ('created_date', models.DateTimeField()),
                ('updated_date', models.DateTimeField()),
                ('BBSlike_count', models.IntegerField(null=True)),
                ('isAnonymous', models.IntegerField(null=True)),
            ],
            options={
                'ordering': ['-ranking'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('content', models.CharField(max_length=1000)),
                ('submit_date', models.DateTimeField()),
                ('commenter', models.CharField(max_length=40)),
                ('toComment_id', models.IntegerField(blank=True, null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('object_id', models.PositiveIntegerField()),
                ('author_name', models.CharField(max_length=40)),
                ('at_person_name', models.CharField(max_length=500)),
                ('submit_time', models.DateTimeField(auto_now_add=True)),
                ('is_readed', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_reply', models.BooleanField(default=False)),
                ('is_answer', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['-submit_time'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('tag_name', models.CharField(max_length=20)),
                ('search_count', models.IntegerField()),
                ('connect_count', models.IntegerField()),
            ],
            options={
                'ordering': ('-connect_count',),
            },
        ),
        migrations.CreateModel(
            name='TJobHunter',
            fields=[
                ('job_hunter_id', models.IntegerField(primary_key=True, serialize=False)),
                ('sina_id', models.CharField(max_length=40, blank=True, null=True)),
                ('tencent_id', models.CharField(max_length=40, blank=True, null=True)),
                ('weixin_id', models.CharField(max_length=40, blank=True, null=True)),
                ('job_hunter_name', models.CharField(max_length=40)),
                ('job_hunter_email', models.CharField(max_length=100, unique=True)),
                ('job_hunter_password', models.CharField(max_length=45)),
                ('job_hunter_tel', models.CharField(max_length=20, blank=True, null=True)),
                ('job_hunter_bachelor_degree', models.CharField(max_length=8, blank=True, null=True)),
                ('job_hunter_start_work_year', models.CharField(max_length=20, blank=True, null=True)),
                ('job_hunter_sex', models.CharField(max_length=4, blank=True, null=True)),
                ('job_hunter_birthday', models.DateField(blank=True, null=True)),
                ('job_hunter_avatar_path', models.CharField(max_length=72, blank=True, null=True)),
                ('job_hunter_depict', models.CharField(max_length=500, blank=True, null=True)),
                ('job_hunter_current_province', models.CharField(max_length=45, blank=True, null=True)),
                ('job_hunter_current_city', models.CharField(max_length=45, blank=True, null=True)),
                ('job_hunter_current_district', models.CharField(max_length=45, blank=True, null=True)),
                ('job_hunter_current_status', models.CharField(max_length=45, blank=True, null=True)),
                ('job_hunter_major', models.CharField(max_length=45, blank=True, null=True)),
                ('job_hunter_college', models.CharField(max_length=45, blank=True, null=True)),
                ('job_hunter_last_occupation', models.CharField(max_length=45, blank=True, null=True)),
                ('job_hunter_last_employer', models.CharField(max_length=45, blank=True, null=True)),
                ('update_time', models.DateTimeField(blank=True, null=True)),
                ('import_from_other', models.IntegerField(blank=True, null=True)),
                ('job_hunter_specialty', models.CharField(max_length=100, blank=True, null=True)),
                ('product_pic1', models.CharField(max_length=72, blank=True, null=True)),
                ('product_pic2', models.CharField(max_length=72, blank=True, null=True)),
                ('product_pic3', models.CharField(max_length=72, blank=True, null=True)),
                ('product_pic4', models.CharField(max_length=72, blank=True, null=True)),
                ('product_pic5', models.CharField(max_length=72, blank=True, null=True)),
                ('product_url', models.CharField(max_length=72, blank=True, null=True)),
                ('credit', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='bbs',
            name='tags',
            field=models.ManyToManyField(to='forum.Tag'),
        ),
        migrations.AddField(
            model_name='answers',
            name='bbs',
            field=models.ForeignKey(to='forum.BBS'),
        ),
    ]
