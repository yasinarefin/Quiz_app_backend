from django.contrib import admin
from Quiz.models import Quiz, Question, Participation
# Register your models here.

class QuizAdmin(admin.ModelAdmin):
    list_display = ('quiz_id',  'name', 'total_score', 'start_time', 'end_time')

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)

class ParticipationAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user', 'score')

admin.site.register(Participation, ParticipationAdmin)
