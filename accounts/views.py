from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from accounts.serializers import TutorSerializer, StudentSerializer,AssignmentSerializer,SubmissionSerializer
from accounts.utils import generate_access_token, generate_refresh_token
from .models import Tutor, Student,Assignment,Submission
from datetime import date


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def tutor_login(request):
    User = get_user_model()
    username = request.data.get('username')

    tutor = Tutor.objects.filter(name=username).first()
    if tutor is None:
        tutor = Tutor(name = username)
        tutor.save()

    access_token = generate_access_token(tutor, 'tutor')
    refresh_token = generate_refresh_token(tutor, 'tutor')

    response = Response()
    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
    }

    return response

@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def student_login(request):
    User = get_user_model()
    username = request.data.get('username')

    student = Student.objects.filter(name=username).first()
    if student is None:
        student = Student(name = username)
        student.save()

    access_token = generate_access_token(student, 'student')
    refresh_token = generate_refresh_token(student, 'student')

    response = Response()
    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
    }

    return response

################ Authenticated end points ###########################


@api_view(['GET'])
def student_profile(request):
    student = request.user
    serialized_student = StudentSerializer(student).data
    return Response({'user': serialized_student })


@api_view(['GET'])
def tutor_profile(request):
    tutor = request.user
    serialized_user = TutorSerializer(tutor).data
    return Response({'user': serialized_user })


@api_view(['DELETE', 'GET', 'POST', 'PUT'])
def assignment(request):
    user = request.user

    if request.method=='POST':
        # validation for student
        # only tutor can create assignment
        if isinstance(user, Student):
            raise exceptions.AuthenticationFailed('Student not allowed to create Assignment')
        else:
            discriptionData = request.data.get('description')
            deadline = request.data.get('dead_line_date')
            publishedDate = request.data.get('published_at')
            assignment_data=Assignment(discription=discriptionData,deadline_date=deadline,tutor=user,published_at=publishedDate)
            assignment_data.save()
            assignment_id=Assignment.objects.filter().last()
            stu=Student.objects.all()
            for i in stu:
                submission_data=Submission(status='pending',submission_student=i,assignment=assignment_id)
                submission_data.save()
        return Response({'success': 'assignment is created !! ' })
        
        # Create assignment
    if request.method=='GET':
        if isinstance(user, Student):
            stauts = request.GET.get('stauts')
            # TODO get filter param of Status
            if stauts== 'pending':
                submission_data=Submission.objects.filter(submission_student__id=user.id,status='pending')
                submission=SubmissionSerializer(submission_data, many = True).data
                return Response({'data ': submission })
            elif stauts== 'all':
                submission_data=Submission.objects.filter(submission_student__id=user.id)
                submission=SubmissionSerializer(submission_data, many = True).data
                return Response({'data ': submission })
            elif stauts== 'overdue':
                submission_data=Submission.objects.filter(submission_student__id=user.id,status='overdue')
                submission=SubmissionSerializer(submission_data, many = True).data
                return Response({'data ': submission })
            elif stauts== 'submited':
                submission_data=Submission.objects.filter(submission_student__id=user.id,status='submited')
                submission=SubmissionSerializer(submission_data, many = True).data
                return Response({'data ': submission })
            elif stauts!="pending" and stauts!="all" and stauts!="overdue" and stauts!="submited" and stauts!=None:
                raise exceptions.ParseError('The selected Status is not valid please use the following => pending or all or overdue or submited')
            
            submission_data=Submission.objects.filter(submission_student__id=user.id)
            submission=SubmissionSerializer(submission_data, many = True).data
            return Response({'submissions ': submission })
        if isinstance(user, Tutor):
            # TODO get filter param of PublishedAt
            publihsed_at = request.GET.get('published_at')
            today = date.today()
            if publihsed_at== 'ongoing':
                assignment_data=Assignment.objects.filter(published_at__lt=today)
            elif publihsed_at== 'schedule':
                assignment_data=Assignment.objects.filter(published_at__gt=today)
                assignments  = AssignmentSerializer(assignment_data, many = True).data
                return Response({'assigments': assignments })
            elif publihsed_at!="ongoing" and publihsed_at!="schedule" and publihsed_at!=None:
                raise exceptions.ParseError('The selected Status is not valid please use the following => schedule or ongoing')
            assignment=Assignment.objects.filter(tutor__id=user.id)
            assignments  = AssignmentSerializer(assignment, many = True).data
            return Response({'assigments': assignments })
    return Response({'success': 'true' })


@api_view(['DELETE', 'GET', 'POST', 'PUT'])
def assignment_delete(request,id):
    user = request.user
    if request.method=='DELETE':
        if isinstance(user, Student):
            raise exceptions.AuthenticationFailed('Student can not delete the assignment !!!')
        if isinstance(user, Tutor):
            assignment_data=Assignment.objects.get(id=id)
            if not assignment_data:
                raise exceptions.AuthenticationFailed('this assignment is not present !!!')
            else:
                assignment_data.delete()
    return Response({'success': 'Assignment Deleted !' })

@api_view(['PUT'])
def assignment_update(request,id):
    user = request.user
    if isinstance(user, Student):
        raise exceptions.AuthenticationFailed('Student can not Update  the assignment !!!')
    if isinstance(user, Tutor):
        assignment_data=Assignment.objects.get(id=id)
        uppdate_descrition=request.data.get('description')
        uppdate_dead_line_date=request.data.get('dead_line_date')
        if uppdate_descrition!=None:
            assignment_data.discription=uppdate_descrition
        if uppdate_dead_line_date!=None:
            assignment_data.deadline_date=uppdate_dead_line_date
        assignment_data.save()
    return Response({'success': 'Assignment updated  !' })
    

@api_view(['POST'])
def submit_assignment(request,id):
    user = request.user
    today = date.today()
    if isinstance(user, Tutor):
        raise exceptions.AuthenticationFailed('Tutor can not submit the submission!!!')
    if isinstance(user, Student):
        try:
            assignment_data=Assignment.objects.get(id=id)
        except Assignment.DoesNotExist:
            raise exceptions.ParseError('assignment not exist !!')
        today = date.today()
        if(today<assignment_data.published_at):
            return Response({'success': 'assignment is not Authorized   !' })
        else:
            try:
                submission_details=Submission.objects.get(assignment__id=assignment_data.id,submission_student__id=user.id)
            except Submission.DoesNotExist :
                raise exceptions.ParseError('assignment not exist !!')
            if(submission_details.status!='pending'):
                return Response({'error': 'Submission is already submitted  !!' })
                
            else:
                submission_remark=request.data.get('remark')
                submission_details.remark=submission_remark
                submission_details.status='submitted'
                if today>submission_details.assignment.deadline_date:
                    submission_details.status='overdue'
                submission_details.submited_date=today
                submission_details.save()
    return Response({'success': 'Assignment Submitted  !' })