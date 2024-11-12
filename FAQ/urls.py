from django.urls import path
from . import views

urlpatterns = [
    path('faq/submit/', views.submit_question, name='submit_question'),
    path('faq/review/', views.review_questions, name='review_questions'),
    path(
        'faq/answer/<int:question_id>/',
        views.answer_question,
        name='faq_answer'
    ),
    path(
        'faq/delete/<int:question_id>/',
        views.delete_question,
        name='delete_question'
    ),
    path(
        'faq/delete/faq/<int:faq_id>/',
        views.delete_faq,
        name='delete_faq'
    ),
    path(
        'faq/edit/<int:faq_id>/',
        views.edit_faq,
        name='edit_faq'),
    path('faq/', views.faq_search, name='faq_search'),
]
