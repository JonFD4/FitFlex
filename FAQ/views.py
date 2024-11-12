from django.shortcuts import render, redirect, get_object_or_404
from .models import FAQ, UserQuestion
from .forms import FAQForm, UserQuestionForm
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
                messages.success(request, 'Your question has been submitted.')
                return redirect('faq_search')
            except Exception:
                messages.error(request, 'An error in saving your question.')
                return HttpResponse(status=500)
        else:
            messages.error(request, 'Form submission error. Check inputs.')
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
        messages.error(request, 'No questions for review.')
        return HttpResponseNotFound("No questions found.")
    except Exception:
        messages.error(request, 'Unexpected error. Try again.')
        return HttpResponse(status=500)


@staff_member_required
def answer_question(request, question_id):
    try:
        question = get_object_or_404(UserQuestion, id=question_id)
        if request.method == 'POST':
            answer = request.POST.get('answer')
            if answer:
                try:
                    FAQ.objects.create(
                        question=question.question,
                        answer=answer,
                        is_answered=True
                    )
                    question.is_reviewed = True
                    question.save()
                    messages.success(request, 'Question answered successfully')
                    return redirect('review_questions')
                except Exception:
                    messages.error(request, 'Error while saving the answer.')
                    return HttpResponse(status=500)
            else:
                messages.error(request, 'Answer cannot be empty.')
                return HttpResponseBadRequest("Answer required.")
        return render(request, 'faq/answer_questions.html', {'question': question})
    except UserQuestion.DoesNotExist:
        messages.error(request, 'Question not found.')
        return HttpResponseNotFound("Question not found.")
    except Exception:
        messages.error(request, 'Unexpected error. Try again.')
        return HttpResponse(status=500)


@staff_member_required
def delete_question(request, question_id):
    try:
        question = get_object_or_404(UserQuestion, id=question_id)
        question.delete()
        messages.success(request, 'Question deleted successfully!')
        return HttpResponseRedirect(reverse('review_questions'))
    except UserQuestion.DoesNotExist:
        messages.error(request, 'Question not found.')
        return HttpResponseNotFound("Question not found.")
    except Exception:
        messages.error(request, 'Error while deleting the question.')
        return HttpResponse(status=500)


@staff_member_required
def edit_faq(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ updated successfully!')
            return redirect('faq_search')
        else:
            messages.error(request, 'Error updating FAQ. Please check the input.')
            return HttpResponseBadRequest("Invalid form data.")
    else:
        form = FAQForm(instance=faq)
    return render(request, 'faq/edit_faq.html', {'form': form, 'faq': faq})


@staff_member_required
def delete_faq(request, faq_id):
    try:
        faq = get_object_or_404(FAQ, id=faq_id)
        faq.delete()
        messages.success(request, 'FAQ deleted successfully!')
        return redirect('faq_search')

    except FAQ.DoesNotExist:
        messages.error(request, 'FAQ not found.')
        return HttpResponseNotFound("FAQ not found.")

    except Exception:
        messages.error(request, 'Error while deleting FAQ.')
        return HttpResponse(status=500)


def faq_search(request):
    try:
        faqs = FAQ.objects.filter(is_answered=True)
        return render(request, 'faq/faq_list.html', {'faqs': faqs})
    except FAQ.DoesNotExist:
        messages.info(request, 'No FAQs available.')
        return render(request, 'faq/faq_list.html', {'faqs': []})
    except Exception:
        messages.error(request, 'Error loading FAQs. Try again.')
        return HttpResponse(status=500)
