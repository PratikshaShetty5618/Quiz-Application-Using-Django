from django.shortcuts import render,redirect,render_to_response,get_object_or_404
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView,DetailView
from django.views.generic.base import View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import *
import random
from django.utils.timezone import utc
import math
from django.contrib import messages


# Create your views here.

def quiz_complete(request):
	context={}
	quiz = Quiz.objects.get(id=request.session['quiz'],quiz_setter = request.user)
	if quiz.ready_status:
		context['update'] = "yes"
		messages.success(request, 'Updated Quiz successfully')
	else:
		context['update'] = "no"
		messages.success(request, 'Deployed quiz successfully')
		quiz.ready_status = "True"
		quiz.save()
	context['title'] = quiz.title
	# del request.session['quiz']
	return render(request, 'quiz_complete.html', context)


def index(request):
	context = {}
	return render(request, 'index.html', context)

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('index')

class CreateQuiz1(LoginRequiredMixin,CreateView):
	form_class = QuizCreateForm
	template_name = 'create_quiz1.html'

	def form_valid(self, form):
		instance = form.save(commit = False)
		instance.time_alloted = form.cleaned_data.get('time_alloted')
		instance.quiz_setter = self.request.user
		instance.save()
		self.request.session['quiz'] = instance.pk
		messages.success(self.request, 'You have successfully initialized your quiz "' + instance.title + '"')
		return redirect('create_quiz2')


class UpdateQuiz1(LoginRequiredMixin,UpdateView):
    form_class = QuizCreateForm
    template_name = 'create_quiz1.html'
    model = Quiz
    
    def form_valid(self, form): 
        instance = form.save(commit=False)
        instance.time_alloted = form.cleaned_data.get('time_alloted')
        instance.quiz_setter = self.request.user
        instance.save()
        self.request.session['quiz'] = instance.pk
        try:

        	query = Quiz.objects.get(id=self.request.session['quiz'])
	        if 'same' == query.marking:
	        	exist_query = Same_Marking.objects.get(quiz = query)
	        	if exist_query:
	        		messages.success(self.request, 'Your initialized quiz "' + instance.title +'" has been successfully updated!')
	        		return redirect('update_quiz2', id=exist_query.pk)
	        else:
	        	exist_query = Different_Marking.objects.get(quiz = query)
	        	if exist_query:
	        		messages.success(self.request, 'Your initialized quiz "' + instance.title +'" has been successfully updated!')
	        		return redirect('update_quiz2', id=exist_query.pk)
        except:
        	messages.success(self.request, 'Your initialized quiz "' + instance.title +'" has been successfully updated!')
        	return redirect('create_quiz2')

@login_required
def create_quiz2(request):
	query = Quiz.objects.get(id=request.session['quiz'])
	if 'same' == query.marking:
		if (request.method == 'POST'):
			form = SameMarkingCreateForm(request.POST)
			if (form.is_valid()):
				instance = form.save(commit=False)
				instance.quiz = query
				instance.save()
				messages.success(request, 'You have successfully completed the marking scheme of quiz "' + query.title +'".')
				return redirect('easy_ques')
		else:
			form = SameMarkingCreateForm()
	else:
		if (request.method == 'POST'):
			form = DifferentMarkingCreateForm(request.POST)
			if (form.is_valid()):
				instance = form.save(commit=False)
				instance.quiz = query
				instance.save()
				messages.success(request, 'You have successfully completed the marking scheme of quiz "' + query.title +'".')
				return redirect('easy_ques')
		else:
			form = DifferentMarkingCreateForm()
	return render(request, 'create_quiz2.html', {'form': form})

@login_required
def update_quiz2(request, id):
	query = Quiz.objects.get(id=request.session['quiz'])
	if 'same' == query.marking:
	    instance = get_object_or_404(Same_Marking, id=id)
	    form = SameMarkingCreateForm(request.POST or None, instance=instance)
	    if form.is_valid():
	    	instance = form.save(commit=False)
	    	instance.quiz = query
	    	form.save()
	    	messages.success(request, 'You have successfully updated the marking scheme of quiz "' + query.title +'".')
	    	return redirect('easy_ques')
	else:
		instance = get_object_or_404(Different_Marking, id=id)
		form = DifferentMarkingCreateForm(request.POST or None, instance=instance)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.quiz = query
			form.save()
			messages.success(request, 'You have successfully updated the marking scheme of quiz "' + query.title +'".')
			return redirect('easy_ques')	
	return render(request, 'create_quiz2.html', {'form': form}) 

class CreateEasyQuiz(LoginRequiredMixin,CreateView):
	form_class = EasyCreateForm
	template_name = 'add_ques_easy.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		quiz = Quiz.objects.get(id=self.request.session['quiz'],quiz_setter = self.request.user)
		context['easy_ques'] = EasyQuestionAnwers.objects.filter(quiz=quiz)
		return context

	def form_valid(self, form):
		instance = form.save(commit = False)
		instance.quiz = Quiz.objects.get(id=self.request.session['quiz'])
		instance.save()
		messages.success(self.request, 'You have successfully added a question to the Easy Level Questions for Quiz "' + instance.quiz.title +'".')
		return redirect('easy_ques')

class UpdateEasyQuiz(LoginRequiredMixin,UpdateView):
	form_class = EasyCreateForm
	template_name = 'add_ques_easy.html'
	model = EasyQuestionAnwers

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		quiz = Quiz.objects.get(id=self.request.session['quiz'],quiz_setter = self.request.user)
		context['easy_ques'] = EasyQuestionAnwers.objects.filter(quiz=quiz)
		return context

	def form_valid(self, form): 
		instance = form.save(commit = False)
		instance.quiz = Quiz.objects.get(id=self.request.session['quiz'])
		instance.save()
		messages.success(self.request, 'You have successfully updated a question to the Easy Level Questions for Quiz "' + instance.quiz.title +'".')
		return redirect('easy_ques')

class CreateMediumQuiz(LoginRequiredMixin,CreateView):
	form_class = MediumCreateForm
	template_name = 'add_ques_medium.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		quiz = Quiz.objects.get(id=self.request.session['quiz'],quiz_setter = self.request.user)
		context['medium_ques'] = MediumQuestionAnwers.objects.filter(quiz=quiz)
		return context

	def form_valid(self, form):
		instance = form.save(commit = False)
		instance.quiz = Quiz.objects.get(id=self.request.session['quiz'])
		instance.save()
		messages.success(self.request, 'You have successfully added a question to the Medium Level Questions for Quiz "' + instance.quiz.title +'".')
		return redirect('medium_ques')

class UpdateMediumQuiz(LoginRequiredMixin,UpdateView):
    form_class = MediumCreateForm
    template_name = 'add_ques_medium.html'
    model = MediumQuestionAnwers

    def get_context_data(self, **kwargs):
    	context = super().get_context_data(**kwargs)
    	quiz = Quiz.objects.get(id=self.request.session['quiz'],quiz_setter = self.request.user)
    	context['medium_ques'] = MediumQuestionAnwers.objects.filter(quiz=quiz)
    	return context

    def form_valid(self, form):
    	instance = form.save(commit = False)
    	instance.quiz = Quiz.objects.get(id=self.request.session['quiz'])
    	instance.save()
    	messages.success(self.request, 'You have successfully updated a question to the Medium Level Questions for Quiz "' + instance.quiz.title +'".')
    	return redirect('medium_ques')

class CreateHardQuiz(LoginRequiredMixin,CreateView):
	form_class = HardCreateForm
	template_name = 'add_ques_hard.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		quiz = Quiz.objects.get(id=self.request.session['quiz'],quiz_setter = self.request.user)
		context['hard_ques'] = HardQuestionAnwers.objects.filter(quiz=quiz)
		return context

	def form_valid(self, form):
		instance = form.save(commit = False)
		instance.quiz = Quiz.objects.get(id=self.request.session['quiz'])
		instance.save()
		messages.success(self.request, 'You have successfully added a question to the Hard Level Questions for Quiz "' + instance.quiz.title +'".')
		return redirect('hard_ques')

class UpdateHardQuiz(LoginRequiredMixin,UpdateView):
	form_class = HardCreateForm
	template_name = 'add_ques_hard.html'
	model = HardQuestionAnwers

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		quiz = Quiz.objects.get(id=self.request.session['quiz'],quiz_setter = self.request.user)
		context['hard_ques'] = HardQuestionAnwers.objects.filter(quiz=quiz)
		return context

	def form_valid(self, form):
		instance = form.save(commit = False)
		instance.quiz = Quiz.objects.get(id=self.request.session['quiz'])
		instance.save()
		messages.success(self.request, 'You have successfully updated a question to the Hard Level Questions for Quiz "' + instance.quiz.title +'".')
		return redirect('hard_ques')

class CategoryList(ListView):
    template_name = 'categories.html'
    model = Category
    context_object_name = 'categories' #Context name used in template

class CategoryQuiz(View):
	def get(self,request,*args,**kwargs):
		category = Category.objects.filter(category = kwargs['category'])
		quiz = Quiz.objects.filter(category = category[0],ready_status = "True").values()
		context = {}
		context['category_quiz'] = quiz
		context['category'] = kwargs['category']
		return render(request, 'category_quiz.html', context)

class QuizDetail(View):
	def get(self,request,*args,**kwargs):
		quiz = Quiz.objects.filter(slug = kwargs['slug'])[0]
		context = {}
		context['ques_count'] = quiz_actual_question_count(quiz)
		context['quiz'] = quiz
		if quiz.marking == 'same':
			par = marks_n_level(quiz)
			total_marks,neg_marks = par[-1],par[-2]
			context['neg_marks'] = neg_marks
		else:
			par = marks_n_level(quiz)
			total_marks,easy_neg_marks,medium_neg_marks,hard_neg_marks = par[-1],par[-4],par[-3],par[-2]
			context['easy_neg_marks'] = easy_neg_marks
			context['medium_neg_marks'] = medium_neg_marks
			context['hard_neg_marks'] = hard_neg_marks
		context['pass_marks'] = total_marks * quiz.pass_mark / 100
		context['total_marks'] = total_marks
		time = quiz.time_alloted.split(':')
		context['hours'] = time[0]
		context['minutes'] = time[1]
		context['seconds'] = time[2]
		return render(request, 'quiz_detail.html', context)

def quiz_actual_question_count(quiz):
	easy_ques_count = len(EasyQuestionAnwers.objects.filter(quiz=quiz))
	medium_ques_count = len(MediumQuestionAnwers.objects.filter(quiz=quiz))
	hard_ques_count = len(HardQuestionAnwers.objects.filter(quiz=quiz))
	ques_count = easy_ques_count + medium_ques_count + hard_ques_count
	if ques_count<=quiz.max_questions:
		return ques_count
	else:
		return quiz.max_questions
	
def marks_n_level(quiz):
	ques_count = quiz_actual_question_count(quiz)

	hard = HardQuestionAnwers.objects.filter(quiz=quiz)
	if ques_count//3 < hard.count():
		hard_count = ques_count//3
	else:
		hard_count = hard.count()

	medium = MediumQuestionAnwers.objects.filter(quiz = quiz)
	if (ques_count - hard_count)//2 < medium.count():
		medium_count = (ques_count - hard_count)//2
	else:
		medium_count = medium.count()

	easy = EasyQuestionAnwers.objects.filter(quiz = quiz)
	if (ques_count - medium_count - hard_count ) < easy.count():
		easy_count = (ques_count - medium_count - hard_count)
	else:
		easy_count = easy.count()

	while easy_count + medium_count + hard_count < ques_count:
		if medium_count != medium.count():
			if (ques_count - (easy_count + medium_count + hard_count)) <= (medium.count() - medium_count):
				medium_count +=  ques_count - (easy_count + medium_count + hard_count)
			elif ques_count - (easy_count + medium_count + hard_count) > medium.count()-medium_count:
				medium_count += medium.count()-medium_count
				if ques_count - (easy_count + medium_count + hard_count) <= hard.count()-hard_count:
					hard_count += ques_count - (easy_count + medium_count + hard_count)
				elif ques_count - (easy_count + medium_count + hard_count) > hard.count()-hard_count:
					hard_count += hard.count()
		elif hard_count != hard.count():
			if ques_count - (easy_count + medium_count + hard_count) <= hard.count()-hard_count:
				hard_count += ques_count - (easy_count + medium_count + hard_count)
			elif ques_count - (easy_count + medium_count + hard_count) > hard.count()-hard_count:
				hard_count += hard.count()

	if 'same'== quiz.marking:
		query_marks = Same_Marking.objects.get(quiz = quiz)
		marks = query_marks.marks
		neg_marks = query_marks.neg
		total_marks = ques_count * marks
		return (easy_count,medium_count,hard_count,marks,neg_marks,total_marks)
	else:
		query_marks = Different_Marking.objects.get(quiz = quiz)
		easy_marks = query_marks.easy_marks
		easy_neg_marks = query_marks.easy_neg
		medium_marks = query_marks.medium_marks
		medium_neg_marks = query_marks.medium_neg
		hard_marks = query_marks.hard_marks
		hard_neg_marks = query_marks.hard_neg
		total_marks = easy_count * easy_marks + medium_count * medium_marks + hard_count * hard_marks
		return (easy_count,medium_count,hard_count,easy_marks,medium_marks,hard_marks,easy_neg_marks,medium_neg_marks,hard_neg_marks,total_marks)

class QuizQuestions(View):
	def get(self,request,*args,**kwargs):
		try:
			request.session['id']
			quiz = Quiz.objects.filter(slug = kwargs['slug'])[0]
			context = {}

			context['ques_count'] = quiz_actual_question_count(quiz)

			if quiz.marking == 'same':
				easy_count,medium_count,hard_count,marks,neg_marks,total_marks = marks_n_level(quiz)
				context['marks'] = marks
				context['neg_marks'] = neg_marks
			else:
				easy_count,medium_count,hard_count,easy_marks,medium_marks,hard_marks,easy_neg_marks,medium_neg_marks,hard_neg_marks,total_marks = marks_n_level(quiz)
				context['easy_marks'] = easy_marks
				context['medium_marks'] = medium_marks
				context['hard_marks'] = hard_marks
				context['easy_neg_marks'] = easy_neg_marks
				context['medium_neg_marks'] = medium_neg_marks
				context['hard_neg_marks'] = hard_neg_marks
				
			ques_count = quiz_actual_question_count(quiz)

			easy_ques = random_ques_list(quiz,EasyQuestionAnwers,easy_count)
			medium_ques = random_ques_list(quiz,MediumQuestionAnwers,medium_count)
			hard_ques = random_ques_list(quiz,HardQuestionAnwers,hard_count)

			ques_merge = easy_ques + medium_ques + hard_ques
			random.shuffle(ques_merge)
			
			context['quiz'] = quiz
			context['ques'] = ques_merge
			time = quiz.time_alloted.split(':')
			context['hours'] = time[0]
			context['minutes'] = time[1]
			context['seconds'] = time[2]

			return render(request, 'quiz.html', context)
		except:
			return HttpResponse("Did you refresh or come to this page directly. \nYou need to fill details inorder to access this page. \nPlease do the needful and try again. \nYour quiz is submitted and marks would be displayed if at all you have refreshed.")

def random_ques_list(quiz,mod,count):
	query = mod.objects.filter(quiz = quiz)
	ques = []
	while(len(ques)<count):
		choice =  random.randint(0, query.count()-1)
		if query[choice] not in ques:
			ques.append(query[choice])
	return ques

def quiz_submit(request,slug):
   if request.method == 'GET':
       ## access you data by playing around with the request.POST object
       quiz = Quiz.objects.get(slug = slug)
       answers = request.GET.getlist('answers[]')
       marks = request.GET.getlist('marks[]')
       neg_marks = request.GET.getlist('neg_marks[]')
       user_answers = request.GET.getlist('user_answers[]')
       ques_count = quiz_actual_question_count(quiz)
       achieved_marks = 0
       for i in range(0,ques_count):
       	if not (user_answers[i] == "0" or user_answers[i] == "[]"):
       		print(user_answers[i],answers[i])
	       	if answers[i] == user_answers[i]:
	       		achieved_marks+=int(marks[i])
	       	else:
	       		achieved_marks-=int(neg_marks[i])
       context = {}
       context['achieved_marks'] = achieved_marks
       total_marks = marks_n_level(quiz)[-1]
       pass_marks = total_marks * quiz.pass_mark / 100
       context['pass_marks'] = pass_marks
       context['total_marks'] = total_marks
       if achieved_marks >= pass_marks:
       	result = "pass"
       	context['result'] = "Pass"
       	context['words'] = quiz.success_text
       else:
       	result = "fail"
       	context['result'] = "Fail"
       	context['words'] = quiz.fail_text

       instance = get_object_or_404(User_Detail, id=request.session['id'])
       instance.status = result
       instance.quiz = quiz
       instance.marks_obtained = achieved_marks
       instance.save()
       del request.session['id']
       messages.success(request, 'You have successfully submitted the quiz.')
       return render(request,'temp.html',context)

   elif request.method == 'POST':
       return HttpResponse("There's some problem whle submission. Do try again later!!!")

def user_detail(request,slug):
	if (request.method == 'POST'):
		form = UserDetailForm(request.POST)
		if (form.is_valid()):
			instance = form.save(commit=False)
			quiz = Quiz.objects.get(slug = slug)
			instance.quiz = quiz
			users = User_Detail.objects.all()
			flag = False
			context = {}
			context['quiz'] = quiz
			for user in users:
				if user.email == instance.email and user.quiz == instance.quiz:
					if user.status == "pass":
						flag = True
						context['status'] = user.status
						context['marks_obtained'] = user.marks_obtained
						return render(request,'attempt_restriction.html',context)
					else:
						seconds = get_time_diff(user.attempted_at)
						months = seconds / 2.628e+6
						if months >= 3:
							instance = get_object_or_404(User_Detail, id=user.id)
							break
						else:
							flag=True
							months_remaining = math.modf(3 - months)
							days_remaining = math.modf(months_remaining[0]*30.4167)
							hours_remaining = math.modf(days_remaining[0]*24)
							minutes_remaining = math.modf(hours_remaining[0]*60)
							seconds_remaining = math.modf(minutes_remaining[0] * 60)
							context['status'] = user.status
							context['months_remaining'] = int(months_remaining[1])
							context['days_remaining'] = int(days_remaining[1])
							context['hours_remaining'] = int(hours_remaining[1])
							context['minutes_remaining'] = int(minutes_remaining[1])
							context['seconds_remaining'] = int(seconds_remaining[1])
							context['marks_obtained'] = user.marks_obtained
							return render(request,'attempt_restriction.html',context)
			if not flag:
				instance.save()
				request.session['id'] = instance.id
				return redirect('quiz_ques',slug=quiz.slug)
	else:
		form = UserDetailForm()
	return render(request, 'user_detail.html', {'form': form})

def get_time_diff(attempted_at):
    if attempted_at:
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        timediff = now - attempted_at
        return timediff.total_seconds()

class QuizListView(LoginRequiredMixin,ListView):
    template_name = 'created_quiz_list.html'
    model = Quiz
    context_object_name = 'quizzes' #Context name used in template

    def get_queryset(self): #To show contacts associated to logged in user only and not all
        quizzes = super().get_queryset()
        return quizzes.filter(quiz_setter=self.request.user)

class QuizDeleteView(LoginRequiredMixin,DeleteView):
    model = Quiz
    template_name = 'delete_quiz.html'
    success_url = reverse_lazy('quiz_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your quiz has been successfully deleted!')
        return super().delete(self, request, *args, **kwargs)


# from myapp.forms import FormForm

# def country_form(request):
#     # instead of hardcoding a list you could make a query of a model, as long as
#     # it has a __str__() method you should be able to display it.
#     country_list = ('Mexico', 'USA', 'China', 'France')
#     form = FormForm(data_list=country_list)

#     return render(request, 'my_app/country-form.html', {
#         'form': form
#     })