from rest_framework import serializers
from django.utils import timezone

'''
{
    "quiz_id": "vogamarka",
    "name": "Voga QUiz",
    "description": "this is a fucking shit quiz",
    "start_time": "2022-02-24T23:55:33Z",
    "end_time": "2022-02-24T23:57:41Z",
    "status": "ended"
}
'''
class QuizSerializer(serializers.Serializer):
    quiz_id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(max_length=300)
    total_score = serializers.IntegerField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    status  = serializers.CharField(source='get_status')

'''
{
    "quiz": "amar_quiz1234",
    "question_count": 1,
    "questions": [
        {
            "type": "sc",
            "score": 1,
            "question": "what's 2 + 2",
            "options": [
                "2",
                "4",
                "5"
            ]
        }
        
    ]
}
'''
class QuestionSerializer(serializers.Serializer):
    quiz = serializers.CharField()
    question_count = serializers.IntegerField()
    questions = serializers.JSONField()

'''
{
    "quiz": "amar_quiz1234",
    "question_count": 1,
    "answers": [
        [
            45
        ],
        [
            "ff"
        ]
    ]
}
'''

class AnswerSerializer(serializers.Serializer):
    quiz = serializers.CharField()
    question_count = serializers.IntegerField()
    answers = serializers.JSONField()