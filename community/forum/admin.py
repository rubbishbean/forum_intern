from django.contrib import admin
from forum import models

class BBS_admin(admin.ModelAdmin):
    list_display=('title','author_name','hit_count','comment_count','created_date')
    list_filter=('created_date',)

admin.site.register(models.BBS,BBS_admin)

