from django.db import models

from django.db.models.fields import DateField

class Tutor(models.Model):
    is_authenticated='true'
    name=models.CharField(max_length=50)

class Student(models.Model):
    is_authenticated='true'
    name=models.CharField(max_length=50)

class Assignment(models.Model):
    tutor=models.ForeignKey(Tutor,on_delete=models.CASCADE)
    discription=models.CharField(max_length=100)
    published_at=models.DateField()
    deadline_date=models.DateField()
    


class Submission(models.Model):
    submission_student=models.ForeignKey(Student,on_delete=models.CASCADE)
    assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE)
    status=models.CharField(max_length=50,default='pending')
    remark=models.CharField(max_length=100)
    submited_date=DateField(null=True)