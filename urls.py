from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("onlinecourse.urls")),
]
app_name = "onlinecourse"

urlpatterns = [
    path(
        "course/<int:course_id>/submit/",
        views.submit,
        name="submit"
    ),
    path(
        "exam_result/",
        views.show_exam_result,
        name="show_exam_result"
    ),
]
