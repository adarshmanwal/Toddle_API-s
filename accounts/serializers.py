from django.db import models
from rest_framework import serializers
from accounts.models import Assignment, Submission, Tutor


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ('__all__')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ('__all__')

class AssignmentSerializer(serializers.ModelSerializer):
    tutor=TutorSerializer(read_only=True)
    
    class Meta:
        model = Assignment
        fields = ('__all__')

class SubmissionSerializer(serializers.ModelSerializer):
    assignment=AssignmentSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ('__all__')