from django.shortcuts import render, redirect, get_object_or_404
from .models import FAQ, UserQuestion
from .forms import UserQuestionForm
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

def submit_question(request):
    if request.method == 'POST':
        form = UserQuestionForm(request.POST)
        if form.is_valid():
            try:
                form.save()  
                messages.success(request, 'Your question has been submitted successfully!')
                return redirect('faq_search') 
            except Exception as e:
                messages.error(request, 'An unexpected error occurred while saving your question. Please try again.')
                return HttpResponse(status=500) 
        else:
            messages.error(request, 'There was an error in the form submission. Please check your inputs.')
            return HttpResponseBadRequest("Invalid form data.")  
    else:
        form = UserQuestionForm()
    return render(request, 'faq/submit_question.html', {'form': form})


@staff_member_required
def review_questions(request):
    try:
        questions = UserQuestion.objects.filter(is_reviewed=False)
        return render(request, 'faq/review_questions.html', {'questions': questions})
    except UserQuestion.DoesNotExist:
        messages.error(request, 'No questions available for review.')
        return HttpResponseNotFound("No questions found for review.")  
    except Exception as e:
        messages.error(request, 'An unexpected error occurred. Please try again.')
        return HttpResponse(status=500) 


@staff_member_required
def answer_question(request, question_id):
    try:
        question = get_object_or_404(UserQuestion, id=question_id)
        if request.method == 'POST':
            answer = request.POST.get('answer')
            if answer:  
                try:
                    FAQ.objects.create(question=question.question, answer=answer, is_answered=True)
                    question.is_reviewed = True
                    question.save()
                    messages.success(request, 'The question has been answered successfully!')
                    return redirect('review_questions')  
                except Exception as e:
                    messages.error(request, 'An error occurred while saving the answer. Please try again.')
                    return HttpResponse(status=500)  
            else:
                messages.error(request, 'You must provide an answer.')
                return HttpResponseBadRequest("Answer cannot be empty.")  
        return render(request, 'faq/answer_questions.html', {'question': question})
    except UserQuestion.DoesNotExist:
        messages.error(request, 'The question you are trying to answer does not exist.')
        return HttpResponseNotFound("Question not found.")  
    except Exception as e:
        messages.error(request, 'An unexpected error occurred. Please try again.')
        return HttpResponse(status=500)  


@staff_member_required
def delete_question(request, question_id):
    try:
        question = get_object_or_404(UserQuestion, id=question_id)
        question.delete()
        messages.success(request, 'The question has been deleted successfully!')
        return HttpResponseRedirect(reverse('review_questions'))
    except UserQuestion.DoesNotExist:
        messages.error(request, 'The question you are trying to delete does not exist.')
        return HttpResponseNotFound("Question not found.")  
    except Exception as e:
        messages.error(request, 'An error occurred while trying to delete the question. Please try again.')
        return HttpResponse(status=500)  


@staff_member_required
def delete_faq(request, faq_id):
    try:
        faq = get_object_or_404(FAQ, id=faq_id)
        faq.delete()
        messages.success(request, 'The FAQ has been deleted successfully!')
        return redirect('faq_search')  

    except FAQ.DoesNotExist:
        messages.error(request, 'The FAQ you are trying to delete does not exist.')
        return HttpResponseNotFound("FAQ not found.")  
    
    except Exception as e:
        messages.error(request, f'An error occurred while trying to delete the FAQ. {str(e)}')
        return HttpResponse(status=500)  


def faq_search(request):
    try:
        faqs = FAQ.objects.filter(is_answered=True)
        return render(request, 'faq/faq_list.html', {'faqs': faqs})
    except FAQ.DoesNotExist:
        messages.info(request, 'No FAQs available at this time.')
        return render(request, 'faq/faq_list.html', {'faqs': []}) 
    except Exception as e:
        messages.error(request, 'An error occurred while loading the FAQs. Please try again.')
        return HttpResponse(status=500)
