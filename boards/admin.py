from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Board, Topic, Post
# Register your models here.
admin.site.unregister(Group)
admin.site.register(Post)


admin.site.site_header = "Board Admin Panel"
admin.site.site_title = "Board Admin Panel"




class TopicAdmin(admin.ModelAdmin):
    fields = ['subject', 'board', 'created_by', 'views']
    list_display = ['subject', 'board', 'created_by', 'views', 'combine_subject_and_created_by']
    list_display_links = ['subject', 'board']
    list_editable = ['views']
    list_filter = ['created_by', 'subject']
    search_fields = ['subject']

    def combine_subject_and_created_by(self, obj):
        return "{} was created by {}".format(obj.subject, obj.created_by)


# admin.site.register(Topic, TopicAdmin)
admin.site.register(Board)


#################################
## $ pip install django-import-export
## Import and Ixport Topic model
# from import_export.admin import ImportExportModelAdmin
# @admin.register(Topic)
# class TopicAdmid_import_export(ImportExportModelAdmin):
#    pass
#################################