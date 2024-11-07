from django.db import models

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    is_answered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class UserQuestion(models.Model):
    question = models.TextField()
    faq = models.ForeignKey(FAQ, on_delete=models.SET_NULL, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return self.question



