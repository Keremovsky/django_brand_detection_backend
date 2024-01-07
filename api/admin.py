from django.contrib import admin
from .models import User, HistoryModel, FeedbackModel, RequestModel

admin.site.register(User)
admin.site.register(HistoryModel)
# admin.site.register(FeedbackModel)
# admin.site.register(RequestModel)

class RequestModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'companyName', 'country', 'website', 'twitter')
    search_fields = ['user__username', 'companyName', 'country']

class FeedbackModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'history', 'date', 'description')
    search_fields = ['user__username', 'history__some_field', 'description']

admin.site.register(RequestModel, RequestModelAdmin)
admin.site.register(FeedbackModel, FeedbackModelAdmin)
