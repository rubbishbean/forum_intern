#-*- coding:utf-8 -*-
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import re

# Create your models here.    

class TJobHunter(models.Model):
    job_hunter_id = models.IntegerField(primary_key=True)
    
    job_hunter_name = models.CharField(max_length=40)
    job_hunter_email = models.CharField(unique=True, max_length=100)
    job_hunter_password = models.CharField(max_length=45)
    job_hunter_tel = models.CharField(max_length=20, blank=True, null=True)
    job_hunter_avatar_path = models.CharField(max_length=72, blank=True, null=True)
       
    credit = models.IntegerField(blank=True,null=True)

    def __unicode__(self):
        return self.job_hunter_name



class Tag(models.Model):
    tag_name = models.CharField(max_length=20)
    search_count = models.IntegerField()
    connect_count = models.IntegerField()

    def __unicode__(self):
        return self.tag_name
    class Meta:
        ordering = ('-connect_count',)


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_obj = generic.GenericForeignKey('content_type','object_id')
    content = models.CharField(max_length=1000)
    submit_date = models.DateTimeField()
    commenter = models.CharField(max_length=40)
    toComment_id = models.IntegerField(null=True,blank=True)

    
    def __unicode__(self):
        return self.content   



class BBS(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    author_name = models.CharField(max_length=40)
    hit_count = models.IntegerField()
    comment_count = models.IntegerField()
    ranking = models.IntegerField()
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()
    tags = models.ManyToManyField(Tag)
    BBSlike_count = models.IntegerField(null=True)
    isAnonymous = models.IntegerField(null=True)
    comments = generic.GenericRelation(Comment)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-ranking']

class Answers(models.Model):
    answer_content = models.TextField()
    updated_date = models.DateTimeField()
    author_name = models.CharField(max_length=40)
    anslike_count = models.IntegerField()
    isAnonymous = models.IntegerField(null=True)
    bbs = models.ForeignKey(BBS)
    comments = generic.GenericRelation(Comment)
    is_readed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.answer_content



class anslike(models.Model):
    user_id = models.IntegerField()
    answer_id = models.IntegerField()

    def __unicode__(self):
        return self.answer_id


class Event(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    event = generic.GenericForeignKey('content_type','object_id')
    author_name = models.CharField(max_length=40)
    at_person_name = models.CharField(max_length=500)

    submit_time = models.DateTimeField(auto_now_add=True)
    is_readed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_reply =  models.BooleanField(default=False)
    is_answer =  models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s提到了%s"%(self.author_name, self.at_person_name)

    class Meta:
        ordering = ["-submit_time"]

@receiver(post_save,sender=Comment)
def at_event_creator(sender,instance,**kwargs):
    comment = instance
    person_names = re.compile('(?<=@)[\w:0-9]+', re.UNICODE)
    at_person_list = set(re.findall(person_names, comment.content))
    if at_person_list:
        for at_person in at_person_list:
            if at_person != comment.commenter:
                try:
                    event = Event(author_name = comment.commenter, event = comment, at_person_name = at_person, is_reply = True)
                    event.save()
                except:
                    pass
    elif comment.commenter != comment.content_obj.author_name:
        event = Event(author_name = comment.commenter, event = comment, at_person_name = comment.content_obj.author_name)
        event.save()


@receiver(post_save,sender=Answers)
def answer_at_event_creator(sender,instance,**kwargs):
    answer = instance
    person_names = re.compile('(?<=@)[\w:0-9]+', re.UNICODE)
    at_person_list = set(re.findall(person_names, answer.answer_content))
    if at_person_list:
        for at_person in at_person_list:
            if at_person != answer.author_name:
                try:
                    event = Event(author_name = answer.author_name, event = answer, at_person_name = at_person, is_answer = True)
                    event.save()
                except:
                    pass
    elif answer.author_name != answer.bbs.author_name:
        event = Event(author_name = answer.author_name, event = answer, at_person_name = answer.bbs.author_name,is_answer = True)
        event.save()
        







    
