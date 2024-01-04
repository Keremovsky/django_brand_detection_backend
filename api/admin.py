from django.contrib import admin
from .models import User, HistoryModel, FeedbackModel, RequestModel

admin.site.register(User)
admin.site.register(HistoryModel)
admin.site.register(FeedbackModel)
admin.site.register(RequestModel)
