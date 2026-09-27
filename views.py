from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Course, Enrollment, Submission, Choice, Question


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    enrollment = Enrollment.objects.get(user=user, course=course)

    # Create a new Submission object referring to the enrollment
    submission = Submission.objects.create(enrollment=enrollment)

    # Collect the selected choices from the exam form
    submitted_answers = extract_answers(request)
    submission.choices.set(submitted_answers)
    submission.save()

    submission_id = submission.id

    return HttpResponseRedirect(
        reverse(
            'show_exam_result',
            args=(course.id, submission_id),
        )
    )


def extract_answers(request):
    """Extract the selected choice ids from the exam form."""
    submitted_answers = []
    for key in request.POST:
        if key.startswith('choice'):
            values = request.POST.getlist(key)
            for value in values:
                choice_id = int(value)
                submitted_answers.append(choice_id)
    return submitted_answers


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    # Get the ids of choices selected by the learner
    selected_choice_ids = submission.choices.values_list('id', flat=True)

    # Get all questions for this course
    questions = course.question_set.all()

    total_score = 0

    for question in questions:
        # Get correct choices for this question
        correct_choice_ids = set(
            question.choice_set.filter(is_correct=True).values_list('id', flat=True)
        )
        # Get choices the learner selected for this specific question
        learner_choice_ids = set(
            question.choice_set.filter(id__in=selected_choice_ids).values_list('id', flat=True)
        )

        # Mark this question correct only if the learner's selections
        # exactly match the correct choices
        if learner_choice_ids == correct_choice_ids:
            question.is_correct = True
            total_score += question.grade
        else:
            question.is_correct = False

    context = {
        'course': course,
        'submission': submission,
        'questions': questions,
        'grade': total_score,
        'selected_ids': selected_choice_ids,
    }

    return render(request, 'onlinecourse/exam_result_bonus.html', context)
