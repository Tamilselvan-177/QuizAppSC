from django.contrib import admin
from .models import Topic, Question, QuizAttempt, UserResponse
# Register your models her


admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(QuizAttempt)
admin.site.register(UserResponse)