from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('home',views.home,name='home'),
    path('search/', views.search_question, name='search_question'),
    path('sign-up',views.sign_up,name='sign_up'),
    path('create_question',views.create_question,name='create_question'),#create_post
    path('add_answer/<int:question_id>',views.add_answer,name='add_answer'),#answer_question
    path('my_posted_questions',views.my_posted_questions,name='my_posted_questions'),
    path('my_answered_questions',views.my_answered_questions,name='my_answered_questions'),
    path('view_answer/<int:question_id>',views.view_answer,name='view_answer'),
    path('delete_answer/', views.delete_answer, name='delete_answer'),
    path('update_answer/<int:question_id>',views.update_answer,name='update_answer'),
    path('update_question/<int:question_id>',views.update_question,name='update_question'),
    path('popular',views.keyword_list,name='popular'),
    path('category',views.category_list,name='category'),
    path('each_popular/<str:keyword>',views.each_popular,name='each_popular'),
    path('each_category/<int:catid>',views.each_category,name='each_category'),
]