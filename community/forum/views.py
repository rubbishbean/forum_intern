#-*- coding:utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.db.models import Q
from forum.models import *
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
import datetime,time
import hashlib
from itertools import chain
import json

import os
import community.settings

# Create your views here.

def index(request):
    updateValue()
    user = getCurrentUser(request)
    answer_num = 0
    question_num = 0
    news_num = 0
    
    if user != None:
        userInfo = getUserInfo(user)
        answer_num = userInfo['ans_num']
        question_num = userInfo['q_num']
        news_num = userInfo['news_num']
        
    hotlist = getRank()
    return render_to_response('hottopic.html',{'user':user,
                                               'hotlist':hotlist,
                                               'answer_num':answer_num,
                                               'question_num':question_num,
                                               'news_num':news_num,},context_instance=RequestContext(request))

def detail(request):
    curIndex = 3 #默认值为3，默认显示三条回答
    bbsId = int(request.GET.get('bbsId','0'))
    bbs = BBS.objects.get(id=bbsId)
    user = getCurrentUser(request)
    num_answers = bbs.answers_set.count()
    endIndex = num_answers
    ans_content = ''
    ansid = 0
    anonymous = 0
    try:
        onclickType = str(request.GET.get('onclickType',''))
    except ValueError:
        onclickType = ''

    if onclickType != '' and num_answers > 3:
        loadinfo = load(request,num_answers)
        curIndex = loadinfo['curIndex']
        endIndex = loadinfo['endIndex']
        
    else:
        bbs.hit_count = bbs.hit_count+1
        bbs.comment_count = num_answers
        bbs.ranking = num_answers*3+ bbs.hit_count
        bbs.save()

    if num_answers <= 3:
        bbs_answers = bbs.answers_set.all()
    else:
        bbs_answers = bbs.answers_set.all()[0:curIndex]

    answer_num = 0
    question_num = 0
    news_num = 0

    if user != None:
        userInfo = getUserInfo(user)
        answer_num = userInfo['ans_num']
        question_num = userInfo['q_num']
        news_num = userInfo['news_num']

    if int(request.GET.get('edit_ans','0')) == 1:
        ansid = int(request.GET.get('ans_id','0'))
        ans_content = Answers.objects.get(id=ansid)
        anonymous = ans_content.isAnonymous
        
    
    return render_to_response('question.html',{'bbs_obj':bbs,
                                               'user':user,
                                               'answers':bbs_answers,
                                               'num_answers':num_answers,
                                               'curIndex':curIndex,
                                               'endIndex':endIndex,
                                               'answer_num':answer_num,
                                               'question_num':question_num,
                                               'ans_content':ans_content,
                                               'ansid':ansid,
                                               'anonymous':anonymous,
                                               'news_num':news_num,},
                              context_instance=RequestContext(request))


def sub_answer(request):
    bbsId = request.POST.get('bbs_id')
    bbs = BBS.objects.get(id=bbsId)
    bbs.updated_date = datetime.datetime.now()
    bbs.save()
    get_answer = request.POST.get('answer_content')
    username = request.session.get('current_user',None)
    anonymous = int(request.POST.get('anonymous','0'))

    bbs.answers_set.create(
        answer_content = get_answer,
        updated_date = datetime.datetime.now(),
        author_name = username,
        anslike_count = 0,
        isAnonymous = anonymous,
        )
    
    return HttpResponseRedirect('/detail/?bbsId=%s' %bbsId)

def sub_comment(request):
    bbsId = request.POST.get('bbs_id')
    get_comment = request.POST.get('comment_content')
    username = request.session.get('current_user',None)
    toComment_id = int(request.POST.get('com_id'))
    answer_id = int(request.POST.get('ans_id'))
    if answer_id == 0:
        bbs = BBS.objects.get(id=bbsId)
        Comment.objects.create(
            content_obj = bbs,
            content = get_comment,
            commenter = username,
            toComment_id = toComment_id,
            submit_date = datetime.datetime.now(),
            )
    else:
        answer = Answers.objects.get(id = request.POST.get('ans_id'))
        Comment.objects.create(
            content_obj = answer,
            content = get_comment,
            commenter = username,
            toComment_id = toComment_id,
            submit_date = datetime.datetime.now(),
            )
        
    
    
    return HttpResponseRedirect('/detail/?bbsId=%s' %bbsId)

    
def acc_login(request):
    username = request.POST['user']
    password = request.POST.get('password','')
    user = TJobHunter.objects.get(job_hunter_email = username)
    md5pass = hashlib.md5(password.encode("utf8")).hexdigest() #密码md5加密后验证
    bbs_list = BBS.objects.all()
    if md5pass.lower() == user.job_hunter_password.lower():
        request.session['current_user']= user.job_hunter_name
        #auth.login(request,user)
        return HttpResponseRedirect("/")
        
    else:
        return render_to_response('login.html',{'err':'登录名或密码错误',},context_instance=RequestContext(request))

def logout_view(request):
    del request.session['current_user']
    return HttpResponse("<h4>成功退出</h4><br><a href='/'>点击回到主页</a>")

def Login(request):
    return render_to_response('login.html',context_instance=RequestContext(request))

def publish(request):
    user = getCurrentUser(request)

    answer_num = 0
    question_num = 0
    news_num = 0
    if user != None:
        userInfo = getUserInfo(user)
        answer_num = userInfo['ans_num']
        question_num = userInfo['q_num']
        news_num = userInfo['news_num']
        
    return render_to_response('askquestion.html',{'user':user,
                                                  'answer_num':answer_num,
                                                  'question_num':question_num,
                                                  'news_num':news_num,},context_instance=RequestContext(request))

def submit(request):
    username = request.session.get('current_user',None)
    user = getCurrentUser(request)
    bbs_content = request.POST.get('content','')
    bbs_title = request.POST.get('question_title','')
    anonymous = int(request.POST.get('anonymous','0'))
    tags = request.POST.get('question_tag','').strip().split(' ')

    answer_num = 0
    question_num = 0
    news_num = 0
    if user != None:
        userInfo = getUserInfo(user)
        answer_num = userInfo['ans_num']
        question_num = userInfo['q_num']
        news_num = userInfo['news_num']
        
    if request.POST.get('question_tag','') == '':
        return render_to_response('askquestion.html',{'err':'标签不能为空',
                                                      'user':user,
                                                      'answer_num':answer_num,
                                                      'question_num':question_num,
                                                      'news_num':news_num,},context_instance=RequestContext(request))
    else:
        timenow = datetime.datetime.now()
        newBBS = BBS.objects.create(
            title = bbs_title,
            content = bbs_content,
            author_name = username,
            hit_count = 0,
            comment_count = 0,
            ranking = 0,
            created_date = timenow,
            updated_date = timenow,
            isAnonymous = anonymous,
            )
        for t in tags:
            if t != ' ':
                if len(Tag.objects.filter(tag_name = t)) == 0:
                    newTag=Tag.objects.create(
                        tag_name = t,
                        search_count = 0,
                        connect_count = 0,
                        )
                    newBBS.tags.add(newTag)
                else:
                    newBBS.tags.add(Tag.objects.get(tag_name = t))
        if len(bbs_content) > 100:
            user.credit += 5
        elif len(bbs_content) <= 100:
            user.credit += 2
        user.save()
        return HttpResponseRedirect('/')


def bbs_edit(request,bbsId):
    user = getCurrentUser(request)

    answer_num = 0
    question_num = 0
    news_num = 0
    if user != None:
        userInfo = getUserInfo(user)
        answer_num = userInfo['ans_num']
        question_num = userInfo['q_num']
        news_num = userInfo['news_num']
        
    bbs = BBS.objects.get(id=bbsId)
    tags = bbs.tags.all()
    tag_to_str = ''
    for t in tags:
        tag_to_str += t.tag_name
        tag_to_str += ' '
    tag_to_str = tag_to_str.rstrip()
    return render_to_response('edit.html',{'bbs':bbs,
                                           'tags':tag_to_str,
                                           'user':user,
                                           'answer_num':answer_num,
                                           'question_num':question_num,
                                           'news_num':news_num,},context_instance=RequestContext(request))

def bbs_edit_done(request,bbsId):
    answer_num = 0
    question_num = 0
    news_num = 0
    if user != None:
        userInfo = getUserInfo(user)
        answer_num = userInfo['ans_num']
        question_num = userInfo['q_num']
        news_num = userInfo['news_num']
        
    if request.POST.get('question_tag','') == '':
        return render_to_response('askquestion.html',{'err':'标签不能为空',
                                                      'user':user,
                                                      'answer_num':answer_num,
                                                      'question_num':question_num,
                                                      'news_num':news_num,},context_instance=RequestContext(request))
    else:
        new_bbs_title = request.POST.get('question_title','')
        new_content = request.POST['content']
        anonymous = int(request.POST.get('anonymous','0'))
        updated_date = datetime.datetime.now()
        bbs = BBS.objects.get(id=bbsId)
        bbs.title = new_bbs_title
        bbs.content = new_content
        bbs.updated_date = updated_date
        bbs.isAnonymous = anonymous
        tags = request.POST.get('question_tag','').strip().split(' ')
        for t in tags:
            if t != ' ':
                if len(Tag.objects.filter(tag_name = t)) == 0:
                    newTag=Tag.objects.create(
                        tag_name = t,
                        search_count = 0,
                        connect_count = 0,
                        )
                    bbs.tags.add(newTag)
                else:
                    bbs.tags.add(Tag.objects.get(tag_name = t))
        
        bbs.save()
    
    return HttpResponseRedirect("/")

def answer_edit(request):
    bbsId = int(request.GET.get('bbsId','0'))
    new_answer = request.POST.get('answer_content')
    ansId = int(request.GET.get('ansId','0'))
    anonymous = int(request.POST.get('anonymous','0'))
    answer = Answers.objects.get(id=ansId)
    answer.answer_content = new_answer
    answer.updated_date = datetime.datetime.now()
    answer.isAnonymous = anonymous
    answer.save()

    return HttpResponseRedirect('/detail/?bbsId=%s#lower-answer-form' %bbsId)


def user_ask(request):
    user = getCurrentUser(request)
    username = user.job_hunter_name
    all_question = BBS.objects.filter(author_name = username )

    answer_num = 0
    question_num = 0
    news_num = 0
    if user != None:
        userInfo = getUserInfo(user)
        answer_num = userInfo['ans_num']
        question_num = userInfo['q_num']
        news_num = userInfo['news_num']
        
    return render_to_response('userask.html',{'user':user,
                                              'answer_num':answer_num,
                                              'question_num':question_num,
                                              'question_list':all_question,
                                              'news_num':news_num,},context_instance=RequestContext(request))

def user_answer(request):
    user = getCurrentUser(request)
    username = user.job_hunter_name
    all_answer = Answers.objects.filter(author_name = username )

    answer_num = 0
    question_num = 0
    news_num = 0
    if user != None:
        userInfo = getUserInfo(user)
        answer_num = userInfo['ans_num']
        question_num = userInfo['q_num']
        news_num = userInfo['news_num']
        
    return render_to_response('useranswer.html',{'user':user,
                                                 'answer_num':answer_num,
                                                 'question_num':question_num,
                                                 'answer_list':all_answer,
                                                 'news_num':news_num,},context_instance=RequestContext(request))
def user_news(request):
    user = getCurrentUser(request)
    username = user.job_hunter_name
    results = Event.objects.filter(at_person_name = username, is_deleted=False)
    unread_count = Event.objects.filter(at_person_name = username, is_deleted=False, is_readed = False).count()

    answer_num = 0
    question_num = 0
    news_num = 0
    if user != None:
        userInfo = getUserInfo(user)
        answer_num = userInfo['ans_num']
        question_num = userInfo['q_num']
        news_num = userInfo['news_num']
        
    return render_to_response('usernews.html',{'user':user,
                                              'answer_num':answer_num,
                                              'question_num':question_num,
                                              'results':results,
                                              'unread_count':unread_count,
                                               'news_num':news_num,},context_instance=RequestContext(request))
    

def like_answer(request):
    user = getCurrentUser(request)
    bbsId = int(request.GET.get('bbs_id','0'))
    answerId = int(request.GET.get('ans_id','0'))
    answer = Answers.objects.get(id=answerId)
    toUser = TJobHunter.objects.get(job_hunter_name =answer.author_name )
    likeobject = anslike.objects.filter(answer_id = answerId).filter(user_id = user.job_hunter_id)
    if len(likeobject) != 0:
        likeobject.delete()
        if answer.anslike_count != 0:
            answer.anslike_count -= 1
            answer.save()
            toUser.credit -= 2
            toUser.save()
    else:
        anslike.objects.create(
            user_id = user.job_hunter_id,
            answer_id = answerId,
            )
        answer.anslike_count += 1
        answer.save()
        toUser.credit += 2
        toUser.save()

    return HttpResponseRedirect('/detail/?bbsId=%s' %bbsId)

def topic(request):
    user = getCurrentUser(request)

    answer_num = 0
    question_num = 0
    news_num = 0
    if user != None:
        userInfo = getUserInfo(user)
        answer_num = userInfo['ans_num']
        question_num = userInfo['q_num']
        news_num = userInfo['news_num']
    
    all_tags = Tag.objects.all()
    for t in all_tags:
        t.connect_count = t.bbs_set.count()
        t.save()
    all_tags = Tag.objects.all().order_by('-connect_count')

    return render_to_response('topic.html',{'user':user,
                                            'answer_num':answer_num,
                                            'question_num':question_num,
                                            'tag_list':all_tags,
                                            'news_num':news_num,},context_instance=RequestContext(request))


def topic_detail(request,tagId):
    user = getCurrentUser(request)

    answer_num = 0
    question_num = 0
    news_num = 0
    if user != None:
        userInfo = getUserInfo(user)
        answer_num = userInfo['ans_num']
        question_num = userInfo['q_num']
        news_num = userInfo['news_num']

    tag = Tag.objects.get(id=tagId)
    bbs_list = tag.bbs_set.all().order_by('-updated_date')

    return render_to_response('topicdetail.html',{'bbs_list':bbs_list,
                                                  'tag':tag,
                                                  'user':user,
                                                  'answer_num':answer_num,
                                                  'question_num':question_num,
                                                  'news_num':new_nums,},context_instance=RequestContext(request))

def search_keyword(request):
    user = getCurrentUser(request)
    answer_num = 0
    question_num = 0
    news_num = 0
    if user != None:
        userInfo = getUserInfo(user)
        answer_num = userInfo['ans_num']
        question_num = userInfo['q_num']
        news_num = userInfo['news_num']
        
    keyword = request.POST.get('keyword')
    bbs_result = BBS.objects.filter(Q(title__icontains = keyword)|
                                    Q(content__icontains = keyword))
    tag_result = Tag.objects.filter(tag_name__icontains = keyword)
    return render_to_response('searchresult.html',{'bbs_list':bbs_result,
                                                   'tag_list':tag_result,
                                                   'keyword':keyword,
                                                   'user':user,
                                                   'answer_num':answer_num,
                                                   'question_num':question_num,
                                                   'news_num':news_num,},context_instance=RequestContext(request))

def read_news(request):
    newsId = int(request.GET.get('newsId','0'))
    bbsId = int(request.GET.get('bbsId','0'))
    try:
        news = Event.objects.get(id=newsId)
        news.is_readed = True
        news.save()
    except:
        return HttpResponseRedirect('/?newId-%s' %newsId)
    return HttpResponseRedirect('/detail/?bbsId=%s' %bbsId)
    


#helper method
def getCurrentUser(request):
    username = request.session.get('current_user',None)
    if username is not None:
        user = TJobHunter.objects.get(job_hunter_name =username )
    else:
        user = None
    return user

def updateValue():
    bbs_list = BBS.objects.all()
    for bbs in bbs_list:
        num_answers = bbs.answers_set.count()
        num_hit = bbs.hit_count
        bbs.ranking = num_answers*3+ int(num_hit/2)
        bbs.save()
    return

def getRank():
    bbs_list = BBS.objects.all().order_by('-ranking')
    ret_bbs_list = []
    for b in bbs_list:
        if len(ret_bbs_list) < 10:
            ret_bbs_list.append(b)
    return ret_bbs_list

def getUserInfo(user):
    username = user.job_hunter_name
    all_answers = Answers.objects.filter(author_name = username)
    answer_num = all_answers.count()
    all_questions = BBS.objects.filter(author_name = username)
    question_num = all_questions.count()
    news_num = Event.objects.filter(at_person_name = username, is_deleted=False, is_readed = False).count()
    return {'ans_num':answer_num,'q_num':question_num,'news_num':news_num,}

    


def load(request,allIndex):
    try:
        curIndex = int(request.GET.get('curIndex','1'))
        endIndex = int(request.GET.get('endIndex','1'))
        onclickType = str(request.GET.get('onclickType',''))
    except ValueError:
        curIndex = 1
        endIndex = 1
        onclickType = ''

    if onclickType == 'more':
        if (allIndex - curIndex)>= 3:
            curIndex += 3
        else:
            curIndex = allIndex
    elif onclickType == 'fold':
        curIndex = 3

    if curIndex == 1 and endIndex == 1:
        endIndex = allIndex
        curIndex = 3
    return {'curIndex':curIndex,'endIndex':endIndex}
        


##############################
'''
ALLOW_SUFFIX =['.jpg','.png','.jpeg','.gif','.doc','.pdf','.txt','.wps']

def create_dir():
    today = datetime.datetime.today()
    dir_name = '/up/bbs/%d/%d/%d' %(today.year,today.month,today.day)
    if not os.path.exists(mofangoa.settings.MEDIA_ROOT + dir_name):
        os.makedirs(community.settings.MEDIA_ROOT + dir_name)
    return dir_name

def upload_image(request):
    dir_name = create_dir()
    if 'HTTP_CONTENT_DISPOSITION' in request.META:#chrome/firefox Xheditor使用的是Html5方式上传
        disposition = request.META['HTTP_CONTENT_DISPOSITION']
        image_name_suffix = disposition[ disposition.rindex('.') : disposition.rindex('"') ]
        data = request.body #request.raw_post_data#已过时

        return write_data(data,image_name_suffix,dir_name,True)
    else:#普通上传，ie
        if 'filedata' in request.FILES:
            image_name = request.FILES["filedata"].name
            image_name_suffix = image_name[image_name.rindex('.') : ]
            return write_data(request.FILES["filedata"],image_name_suffix,dir_name,False)
        else:
            return HttpResponse(json.dumps({'err':'未选择文件','msg':''},ensure_ascii = False))

#保存图片
def write_data(data,image_name_suffix,dir_name,html5,isurl=0):
    if image_name_suffix in ALLOW_SUFFIX:
            image_name = str(int(time.time()))+image_name_suffix
            try:
                destination=open(community.settings.MEDIA_ROOT + dir_name+'/'+ image_name,'wb')
                if html5:
                    destination.write(data)#写文件流
                else:
                    for c in data.chunks():
                        destination.write(c)
                if isurl==0:
                    return HttpResponse(json.dumps({'err':'','msg':'/smedia'+dir_name+'/'+image_name}))
                else:
                    return '/smedia'+dir_name+'/'+image_name
                    
            except Exception,e:
                return HttpResponse(sjson.dumps({'err':e.message,'msg':''},ensure_ascii = False))
    else:
        return HttpResponse(json.dumps({'err':'上传格式不准确!只支持jpg,png,jpeg,gif','msg':''},ensure_ascii = False))


#处理剪切板,外部图片 上传与保存
def upload_remoteImg(request):
    data= request.POST.get('urls','')
    if data:
        dir_name = create_dir()
        if data[:10]=='data:image':
            image_name_suffix = '.'+data[data.index('/')+1 : data.index(';') ]
            data = data[data.index('base64,')+7:]
            return HttpResponse(write_data(base64.b64decode(data),image_name_suffix,dir_name,True,1))
        else:
            #外部图片
            if data.find('|')>0:
                #多图复制
                t=''
                for a in data.split('|'):
                    image_name_suffix = a[ a.rindex('.') :]
                    image_content = urllib.urlopen(a).read()
                    f=write_data(image_content,image_name_suffix,dir_name,True,1)
                    if t=='':
                        t=f
                    else:
                        t='%s|%s'%(t,f)
                return HttpResponse(t)
            else:
                #单图
                image_name_suffix = data[ data.rindex('.') :]
                data = urllib.urlopen(data).read()
                return HttpResponse(write_data(data,image_name_suffix,dir_name,True,1))
    else:
        return HttpResponse('no')
        '''
