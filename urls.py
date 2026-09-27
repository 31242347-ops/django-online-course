from django.urls import path
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    # Course listing / index
    path('', views.CourseListView.as_view(), name='index'),

    # Registration and authentication
    path('registration/', views.registration_request, name='registration'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),

    # Course detail
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_details'),

    # Enrollment
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),

    # Exam submission
    path('<int:course_id>/submit/', views.submit, name='submit'),

    # Exam result
    path(
        '<int:course_id>/submission/<int:submission_id>/result/',
        views.show_exam_result,
        name='show_exam_result',
    ),
]
