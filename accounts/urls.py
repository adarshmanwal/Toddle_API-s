from django.urls import path,include
from . import views
urlpatterns = [
    # Login APis
    path('tutor/login/', views.tutor_login),
    path('student/login/', views.student_login),

    # Authenticated APIs
    path('tutor/profile', views.tutor_profile),
    path('student/profile', views.student_profile),

    # Assignment
    path('assignment', views.assignment),

    #Assignment Delete
    path('assignment/delete/<int:id>', views.assignment_delete),
    path('assignment/update/<int:id>', views.assignment_update),

    #Assignment Submission By student
    path('assignment/submit/<int:id>', views.submit_assignment),
    

]