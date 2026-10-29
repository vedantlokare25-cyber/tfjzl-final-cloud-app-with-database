from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

def popular_course_list(request):
    context = {}
    if request.method == 'GET':
        course_list = Course.objects.order_by('-pub_date')[:10]
        context['course_list'] = course_list
        return render(request, 'onlinecourseapp/course_list.html', context)

def course_details(request, course_id):
    context = {}
    if request.method == 'GET':
        course = get_object_or_404(Course, pk=course_id)
        context['course'] = course
        return render(request, 'onlinecourseapp/course_details_bootstrap.html', context)

def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        return HttpResponseRedirect(reverse(f'onlinecourseapp:course_details', args=(course.id,)))

def submit(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
        
        # Create a submission
        submission = Submission.objects.create(enrollment=enrollment)
        
        # Get selected choices from request.POST
        for key, value in request.POST.items():
            if key.startswith('choice_'):
                choice_id = int(value)
                choice = Choice.objects.get(pk=choice_id)
                submission.choices.add(choice)
                
        return HttpResponseRedirect(reverse('onlinecourseapp:show_exam_result', args=(course.id, submission.id)))

def show_exam_result(request, course_id, submission_id):
    context = {}
    if request.method == 'GET':
        course = get_object_or_404(Course, pk=course_id)
        submission = get_object_or_404(Submission, pk=submission_id)
        
        # Calculate score
        score = 0
        total_score = 0
        
        for question in course.question_set.all():
            total_score += question.grade
            selected_choices = submission.choices.filter(question=question)
            selected_ids = [choice.id for choice in selected_choices]
            if question.is_get_score(selected_ids):
                score += question.grade
                
        context['course'] = course
        context['submission'] = submission
        context['score'] = score
        context['total_score'] = total_score
        return render(request, 'onlinecourseapp/exam_result_bootstrap.html', context)
