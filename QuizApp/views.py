from django.shortcuts import render

# Create your views here.

def index(request):
	context = {}
	return render(request, 'index.html', context)



# from myapp.forms import FormForm

# def country_form(request):
#     # instead of hardcoding a list you could make a query of a model, as long as
#     # it has a __str__() method you should be able to display it.
#     country_list = ('Mexico', 'USA', 'China', 'France')
#     form = FormForm(data_list=country_list)

#     return render(request, 'my_app/country-form.html', {
#         'form': form
#     })