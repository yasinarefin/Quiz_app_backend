from rest_framework.response import  Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
import json
from Quiz.serializers import *
from Quiz.models import Quiz, Question, Participation
from django.utils import timezone
from Authentication import security_tools
from decimal import *

# /quiz/view/<str:status>
@api_view(['GET'])
def show_quiz(request, cur_status):
    token = request.headers['Authorization']
    if security_tools.authenticate(token) == None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method =='GET':
        if cur_status == 'upcoming': # get list of upcoming quizzes
            quizzes = Quiz.objects.filter(start_time__gte=timezone.now(), end_time__gte = timezone.now())
            q_ser = QuizSerializer(quizzes, many=True)
            return Response(q_ser.data, status=status.HTTP_200_OK)
        elif cur_status == 'running':
            quizzes = Quiz.objects.filter(start_time__lte=timezone.now(), end_time__gte = timezone.now())
            q_ser = QuizSerializer(quizzes, many=True)
            return Response(q_ser.data, status=status.HTTP_200_OK)
        elif cur_status == 'all':
            quizzes = Quiz.objects.all()
            q_ser = QuizSerializer(quizzes, many=True)
            return Response(q_ser.data, status=status.HTTP_200_OK)
        elif cur_status == 'ended':
            quizzes = Quiz.objects.filter(end_time__lt = timezone.now())
            q_ser = QuizSerializer(quizzes, many=True)
            return Response(q_ser.data, status=status.HTTP_200_OK)
        else:
            return Response({'error' : 'invalid query'}, status=status.HTTP_400_BAD_REQUEST)

#/quiz/questions/
# get list of questions with quiz id
# include header Authorization and QuizID with the id of the  quiz
@api_view(['GET'])
def questions(request):
    token = request.headers['Authorization']
    if security_tools.authenticate(token) == None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    quiz_id = request.headers['QuizID']
    try:
        quiz = Quiz.objects.get(quiz_id=quiz_id)
        
        # check if quiz has started or not.
        if quiz.get_status == 'upcoming':
            return Response({'error': 'quiz has not started  yet!'}, status=status.HTTP_403_FORBIDDEN)

        question = Question.objects.get(quiz=quiz)
        question_ser = QuestionSerializer(question)
        return  Response(question_ser.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

# get quiz answer  after the  quiz is finished
# include header QuizID with the id of the  quiz
@api_view(['GET'])
def answers(request):
    token = request.headers['Authorization']
    if security_tools.authenticate(token) == None:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    quiz_id = request.headers['QuizID']
    
    try:
        quiz = Quiz.objects.get(quiz_id=quiz_id)
        
        if quiz.get_status != 'ended':
            return Response({'error':'answers are not published yet!'}, 
            status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        question = Question.objects.get(quiz=quiz)
        question_ser = AnswerSerializer(question)
        return  Response(question_ser.data, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
'''  
{
    "quiz_id": "amar_quiz1234r",
    "question_no":1
    "answer":[]
}
'''
@api_view(['POST'])
def participate(request):
    
    if request.method == 'POST':
        token = request.headers['Authorization']
        user = security_tools.authenticate(token)
        if user == None:
            return Response({'message':'not logged in!'},status=status.HTTP_401_UNAUTHORIZED)

        body = request.data
        quiz_id = body['quiz_id']
        question_no = body['question_no']
        answer = body['answer']

        # check if quiz is running
        quiz_obj = Quiz.objects.get(quiz_id=quiz_id)
        if quiz_obj.get_status != 'running':
            return  Response({'message':'quiz is not running'}, status=status.HTTP_410_GONE)

        questions = Question.objects.get(quiz=quiz_id)
        
        print(questions.answers)
        q_count = questions.question_count

        
        # if there is no participation already
        try:
            Participation.objects.get(user=user, quiz=quiz_obj)
        except:
            Participation.objects.create(user=user, quiz=quiz_obj,
             answers=[[] for i in range(q_count)], score=0)
        



        # answer  validaton
        if question_no >= q_count:
            return Response({'message':'out of range'}, status=status.HTTP_404_NOT_FOUND)


        
        
        # check if answer is already submitted
        participation = Participation.objects.get(user=user, quiz=Quiz.objects.get(quiz_id=quiz_id))
        if len(participation.answers[question_no]) != 0:
            return Response({'message':'already submitted'}, status=status.HTTP_406_NOT_ACCEPTABLE)

       
        # data validation check 
        question = questions.questions[question_no]
        print(question)
        options = question['options']
        points = question['score']

        
        if question['type'] == 'sc':
            ok = all(isinstance(x, int) for x in answer)
            ok2 = max(answer) < len(options) and min(answer) >= 0
            if ok == False or ok2 == False:
                return Response({'message':'invalid type'}, status=status.HTTP_400_BAD_REQUEST)
            
        elif question['type'] =='mc':
            ok = all(isinstance(x, int) for x in answer)
            ok2 = max(answer) < len(options) and min(answer) >= 0
            if ok == False or ok2 == False:
                return Response({'message':'invalid'}, status=status.HTTP_400_BAD_REQUEST)
        elif question['type'] == 'inp':
            ok = all(isinstance(x, str) for x in answer)
            if ok == False:
                return Response({'message':'invalid'}, status=status.HTTP_400_BAD_REQUEST)
        # add points
        user_points = 0
        corr_answer = questions.answers[question_no]
        print(corr_answer)
        print(answer)
        print(points)
        if question['type'] == 'sc':
            if len(corr_answer) == len(answer) and set(corr_answer) == set(answer):
                user_points += points
        
        if question['type'] == 'mc':
            wrong_sel = 0
            for i in answer:
                print(i)
                if i not in corr_answer:
                    wrong_sel += 1
            user_points += Decimal(points / 2**wrong_sel)

        if question['type'] == 'inp':
            print(answer)
            if answer[0] in corr_answer:
                user_points += points
        

        print('sss', user_points)

        
        participation.answers[question_no] = answer
        participation.score += user_points
        participation.save()

        return Response({'message':'submitted'}, status=status.HTTP_200_OK)

# get participation status 
# include header Authorization and QuizID 

@api_view(['GET'])
def participation_status(request):
    token = request.headers['Authorization']
    user = security_tools.authenticate(token)
    if user == None:
        return Response({'message':'not logged in!'},status=status.HTTP_401_UNAUTHORIZED)

    quiz_id = request.headers['QuizID']
    try:
        participation_obj = Participation.objects.get(user=user, quiz=Quiz.objects.get(quiz_id=quiz_id))
        obj_ser = ParticipationSerializer(participation_obj)
        return Response(obj_ser.data, status= status.HTTP_200_OK)
    except:
        pass
    return Response({'message':'invalid data'}, status= status.HTTP_400_BAD_REQUEST)
