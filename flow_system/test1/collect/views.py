from django.shortcuts import render
from django.http import HttpResponse


from .models import Questions


def index(request):
    latest_question_list = Questions.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

# Create your views here.
