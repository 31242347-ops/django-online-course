from django.db import models


class Question(models.Model):
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE
    )
    question_text = models.TextField()
    grade = models.IntegerField(default=1)
    is_multi_select = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        "Enrollment",
        on_delete=models.CASCADE
    )
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return str(self.enrollment)
