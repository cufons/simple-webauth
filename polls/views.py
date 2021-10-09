from polls.models import Question
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def index(request):
    lastest_question_list = Question.objects.order_by('-pub_date')
    template = loader.get_template('index.html')

    context = {
        'lastest_question_list' : lastest_question_list
    }

    return HttpResponse(template.render(context, request))