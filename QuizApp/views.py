from django.shortcuts import render,redirect,render_to_response,get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Quiz,Same_Marking
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import QuizCreateForm

# Create your views here.

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
		instance.time_alloted = form.cleaned_data.get('time_limit')
		instance.quiz_setter = self.request.user
		instance.save()
		self.request.session['quiz'] = instance.pk
		return redirect('create_quiz2')


class UpdateQuiz1(LoginRequiredMixin,UpdateView):
    model = Quiz
    fields = ['title','description','category','random_order','max_questions','answers_at_end','pass_mark','marking','success_text','fail_text','time_alloted']
    # fields = '__all__'
    template_name = 'create_quiz1.html'
    
    def form_valid(self, form): 
        instance = form.save(commit=False)
        instance.quiz_setter = self.request.user
        self.request.session['quiz'] = instance.pk
        return redirect('create_quiz2')

class CreateQuiz2(LoginRequiredMixin,CreateView):
	model = Same_Marking
	fields = ['marks','neg']
	template_name = 'create_quiz2.html'

	def form_valid(self, form):
		instance = form.save(commit=False)
		quiz = Quiz.objects.get(id=self.request.session['quiz'])
		instance.quiz = quiz
		instance.save()
		return redirect('create_quiz2')
		
# def test(request):
#     from .forms import QuizCreateForm
    
#     if request.method == 'POST':
#         form = QuizCreateForm(request.POST)
#         if form.is_valid():
#             info = form.cleaned_data('time_limit')
#             print(info)
#     else:
#         form = QuizCreateForm()

        
#     return render(request,'create_quiz1.html',{})	


# class TestView(CreateView):
#     form_class = QuizCreateForm
#     template_name = 'create_quiz1.html'
#     success_url = reverse_lazy('create_quiz2')

#     def form_valid(self,form):
#         self.object = form.save(commit = False)
#         time = form.cleaned_data.get('time_limit')
        
#         # email = form.cleaned_data.get('email')
#         # invite_code_check = InviteCode.objects.filter(email=email,code=invite_code,status="False")
#         # if invite_code_check.exists():
#         #     invite_code_check.update(status="True")
#         #     self.object.save()
#         #     raw_password = form.cleaned_data.get('password1')
#         #     user = authenticate(username=self.object.username, password=raw_password)
#         #     login(self.request, user)
#         #     messages.success(self.request, 'Your account has been successfully created and you have been logged in!')
#         #     return redirect('index')
#         html = "<html><body>Invite Code is not proper. Please Try Again. </body></html>"
#         return HttpResponse(html)

# from myapp.forms import FormForm

# def country_form(request):
#     # instead of hardcoding a list you could make a query of a model, as long as
#     # it has a __str__() method you should be able to display it.
#     country_list = ('Mexico', 'USA', 'China', 'France')
#     form = FormForm(data_list=country_list)

#     return render(request, 'my_app/country-form.html', {
#         'form': form
#     })