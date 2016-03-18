# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tjobhunter',
            name='import_from_other',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_bachelor_degree',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_birthday',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_college',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_current_city',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_current_district',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_current_province',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_current_status',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_depict',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_last_employer',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_last_occupation',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_major',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_sex',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_specialty',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='job_hunter_start_work_year',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='product_pic1',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='product_pic2',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='product_pic3',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='product_pic4',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='product_pic5',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='product_url',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='sina_id',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='tencent_id',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='update_time',
        ),
        migrations.RemoveField(
            model_name='tjobhunter',
            name='weixin_id',
        ),
    ]
