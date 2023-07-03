from django.shortcuts import render,redirect,get_object_or_404
from django.http import Http404
from .forms import *
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import *
import nltk , re

# Create your views here.

def home(request):
    allQuestions = Question.objects.all().order_by('-created_at') #posts
    allQuestions = allQuestions[:10]

    # Delete
    if request.method == "POST":
        question_id = request.POST.get("question-id")
        question = Question.objects.filter(id=question_id).first()

        if question and question.author == request.user:
            question.delete() 

    return render(request,'main/home.html',{'allQuestions':allQuestions})



def search_question(request):
    if request.method == 'GET':
        keyword = request.GET.get('q')
        if keyword:
            questions = Question.objects.filter(description__icontains=keyword)
            return render(request, 'main/search_results.html', {'questions': questions,'keyword':keyword})
    return render(request, 'main/home.html')



def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request,user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request,'registration/sign_up.html',{'form':form})




@login_required(login_url='/login')
def create_question(request): #create question post
    if request.method == 'POST':
        form = PostQuestion(request.POST)
        if form.is_valid:
            question = form.save(commit=False)
            question.author = request.user
            question.category_id = get_tag(request.POST.get('title'))
            question.save()
            return redirect('/home')
    else:
        form = PostQuestion()

    return render(request,'main/create_question.html',{'form':form})




@login_required(login_url='/login')
def add_answer(request, question_id):
    my_question_object = Question.objects.get(pk=question_id)
    question_description = my_question_object.description
    
    if request.method == 'POST':
        form = PostAnswer(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.given_by = request.user 
            answer.for_question_id = question_id
            answer.save()
            return redirect('/home')
    else:
        form = PostAnswer()

    context = {
        'form':form,
        'question_description': question_description,
    }

    return render(request, 'main/add_answer.html', context)



@login_required(login_url='/login')
def my_posted_questions(request):
    my_questions = Question.objects.filter(author=request.user)
    context = {'my_questions':my_questions}

    if request.method == "POST":
        question_id = request.POST.get("question-id")
        question = Question.objects.filter(id=question_id).first()

        if question and question.author == request.user:
            question.delete()

    return render(request,'main/my_posted_questions.html',context)



@login_required(login_url='/login')
def my_answered_questions(request):
    my_answered = Answer.objects.filter(given_by=request.user)
    my_questions = []
    for answer in my_answered:
        my_questions.append(answer.for_question)

    return render(request, 'main/my_answered_questions.html', {'my_questions': my_questions , 'my_answered': my_answered})


def view_answer(request, question_id):
    answers = Answer.objects.filter(for_question_id = question_id)
    curr_question = Question.objects.get(pk=question_id)
    return render(request, 'main/view_answer.html', {'answers': answers,'curr_question':curr_question})

def delete_answer(request):
    
    if request.method == 'POST':
        answer_id = request.POST.get('answer-id')
        answer = get_object_or_404(Answer, id=answer_id, given_by=request.user)
        answer.delete()
        
    return redirect('/my_answered_questions')


@login_required(login_url='/login')
def update_answer(request, question_id):
    my_question_object = Question.objects.get(pk=question_id)
    question_description = my_question_object.description

    try:
        answer = Answer.objects.get(given_by=request.user, for_question_id=question_id)
    except Answer.DoesNotExist:
        raise Http404("Answer does not exist")

    if request.method == 'POST' and request.POST.get('method') == 'PUT':
        form = PostAnswer(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect('/my_answered_questions')
    else:
        form = PostAnswer(instance=answer)

    context = {
        'form':form,
        'question_description': question_description,
    }

    return render(request, 'main/update_answer.html', context)


@login_required(login_url='/login')
def update_question(request,question_id): 
    try:
        cur_question = Question.objects.get(author=request.user, id=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    print(cur_question)
    if request.method == 'POST' and request.POST.get('method') == 'PUT':
        form = PostQuestion(request.POST,instance=cur_question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.category_id = get_tag(request.POST.get('title'))
            question.save()
            return redirect('/my_posted_questions')
    else:
        form = PostQuestion(instance=cur_question)

    return render(request,'main/update_question.html',{'form':form})



def keyword_list(request):
    
    questions = Question.objects.all()

    data_string = ""
    for question in questions:
        data_string += question.title 

    top_keywords = extract_keywords(data_string, num_keywords=20)
    
    return render(request, 'nlp_templates/popular_q.html', {'top_keywords': top_keywords})


def each_popular(request,keyword):

    questions = Question.objects.filter(title__icontains=keyword)
    
    context = {'questions': questions ,
               'keyword':keyword}
    return render(request, 'nlp_templates/each_popular.html', context)



def category_list(request):
    return render(request, 'nlp_templates/category_q.html')


def each_category(request,catid):
    questions = Question.objects.filter(category_id=catid).order_by('-created_at')

    context = {
        'questions' : questions ,
        'catid':catid,
    }

    return render(request, 'nlp_templates/each_category.html', context)