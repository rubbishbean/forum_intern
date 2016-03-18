from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^$','forum.views.index'),
    url(r'^detail/$','forum.views.detail'),
    url(r'^publish/$','forum.views.publish'),
    url(r'^submit/$','forum.views.submit'),
    url(r'^login/$','forum.views.Login'),
    url(r'acc_login/$','forum.views.acc_login'),
    url(r'logout/$','forum.views.logout_view'),
    url(r'^bbs_edit/(\d+)/$','forum.views.bbs_edit'),
    url(r'^bbs_editdone/(\d+)/$','forum.views.bbs_edit_done'),
    url(r'^sub_answer/$','forum.views.sub_answer'),
    url(r'^sub_comment/$','forum.views.sub_comment'),
    url(r'^sub_comment_tobbs/$','forum.views.sub_comment_tobbs'),
    url(r'^user_ask/$','forum.views.user_ask'),
    url(r'^user_answer/$','forum.views.user_answer'),
    url(r'^user_news/$','forum.views.user_news'),
    url(r'^like_ans/$','forum.views.like_answer'),
    url(r'^topic/$','forum.views.topic'),
    url(r'^answer_edit/$','forum.views.answer_edit'),
    url(r'^topic_detail/(\d+)/$','forum.views.topic_detail'),
    url(r'^search_keyword/$','forum.views.search_keyword'),
    url(r'^read_news/$','forum.views.read_news'),
]
