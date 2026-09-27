from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Question, Choice, Submission, Enrollment


@login_required
def submit(request, course_id):
    if request.method != "POST":
        return redirect("onlinecourse:course_list")

    enrollment = get_object_or_404(
        Enrollment,
        learner__user=request.user,
        course_id=course_id
    )

    submission = Submission.objects.create(enrollment=enrollment)
    score = 0

    questions = Question.objects.filter(course_id=course_id)

    for question in questions:
        selected_ids = request.POST.getlist(str(question.id))
        correct_ids = list(
            question.choices.filter(is_correct=True).values_list("id", flat=True)
        )

        if set(map(int, selected_ids)) == set(correct_ids):
            score += question.grade

        for choice_id in selected_ids:
            choice = get_object_or_404(
                Choice,
                id=choice_id,
                question=question
            )
            submission.choices.add(choice)

    request.session["exam_score"] = score
    request.session["course_id"] = course_id

    return redirect("onlinecourse:show_exam_result")


@login_required
def show_exam_result(request):
    score = request.session.get("exam_score")
    course_id = request.session.get("course_id")

    if score is None or course_id is None:
        return HttpResponse("No exam result found. Please submit the exam first.")

    questions = Question.objects.filter(course_id=course_id)

    return render(
        request,
        "onlinecourse/exam_result_bootstrap.html",
        {
            "score": score,
            "questions": questions,
        }
    )
