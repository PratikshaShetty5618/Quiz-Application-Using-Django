from django import forms
from .models import Quiz
from . import select_time_widget

class QuizCreateForm(forms.ModelForm):
	time_limit = forms.TimeField(help_text='Enter data as Hours:Minutes:Seconds i.e. hh:mm:ss .',widget=select_time_widget.SelectTimeWidget())

	class Meta:
		model = Quiz
		fields = ['title','description','category','random_order','max_questions','answers_at_end','pass_mark','success_text','fail_text','time_limit']

# from myapp.fields import ListTextWidget

# class FormForm(forms.Form):
#    char_field_with_list = forms.CharField(required=True)

#    def __init__(self, *args, **kwargs):
#       _country_list = kwargs.pop('data_list', None)
#       super(FormForm, self).__init__(*args, **kwargs)

#     # the "name" parameter will allow you to use the same widget more than once in the same
#     # form, not setting this parameter differently will cuse all inputs display the
#     # same list.
#        self.fields['char_field_with_list'].widget = ListTextWidget(data_list=_country_list, name='country-list')