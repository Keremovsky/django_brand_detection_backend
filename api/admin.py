from django.contrib import admin
from .models import User, HistoryModel, FeedbackModel, RequestModel
from django.utils.html import format_html

admin.site.register(User)
# admin.site.register(HistoryModel)
# admin.site.register(FeedbackModel)
# admin.site.register(RequestModel)


class RequestModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'companyName', 'country', 'website', 'twitter', 'display_image')
    search_fields = ['user__username', 'companyName', 'country']

    def display_image(self, obj):
        return format_html('<img src="{}" style="width:50px;height:50px;" />', obj.image.url)

    display_image.short_description = 'Image'

class FeedbackModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'history', 'date', 'description')
    search_fields = ['user__username', 'history__some_field', 'description']

class HistoryModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'display_image', 'resultIds', 'similarities', 'isSaved')
    list_filter = ('user', 'date', 'isSaved')
    search_fields = ('user__username', 'resultIds', 'similarities')

    def display_image(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.image.url)

    display_image.short_description = 'Image'

admin.site.register(HistoryModel, HistoryModelAdmin)
admin.site.register(RequestModel, RequestModelAdmin)
admin.site.register(FeedbackModel, FeedbackModelAdmin)
