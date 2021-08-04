from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse
from .models import Question
from .serializer import QuestionSerializer
from bs4 import BeautifulSoup
import requests
import json
from .models import Question

# Create your views here.

def index(request):
    Question1 = Question.objects.all()

    Question2 = {'Question1': Question1}
    return render(request, 'index.html', Question2)

def search(request):
    query = request.GET['query']
    Question1 = Question.objects.filter(question__icontains=query)

    Question2 = {'Question1': Question1}
    return render(request, 'search.html', Question2)

class QuestionAPI(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

def new(request):
    try:
        res = requests.get("https://stackoverflow.com/questions")

        soup = BeautifulSoup(res.text, "html.parser")

        questions = soup.select(".question-summary")
        for que in questions:
            q = que.select_one('.question-hyperlink').getText()
            vote_count = que.select_one('.vote-count-post').getText()
            views = que.select_one('.views').attrs['title']
            tags = [i.getText() for i in (que.select('.post-tag'))]

            question = Question()
            question.question = q
            question.vote_count = vote_count
            question.views = views
            question.tags = tags

            question.save()
        return HttpResponse("Latest Data Fetched from Stack Overflow")
    except:
        return HttpResponse(f"Failed")