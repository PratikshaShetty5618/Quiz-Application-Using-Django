from django import forms
from .models import *
from . import select_time_widget

class QuizCreateForm(forms.ModelForm):
	time_alloted = forms.TimeField(help_text='Enter data as Hours:Minutes:Seconds i.e. hh:mm:ss .',widget=select_time_widget.SelectTimeWidget())

	class Meta:
		model = Quiz
		fields = ['title','description','category','random_order','max_questions','answers_at_end','pass_mark','success_text','fail_text','marking','time_alloted']

class SameMarkingCreateForm(forms.ModelForm):

	class Meta:
		model = Same_Marking
		fields = ['marks','neg']

class DifferentMarkingCreateForm(forms.ModelForm):

	class Meta:
		model = Different_Marking
		fields = ['easy_marks','easy_neg','medium_marks','medium_neg','hard_marks','hard_neg']

class EasyCreateForm(forms.ModelForm):
	ANSWER_CHOICES = [
    ('1', 'Option 1'),
    ('2', 'Option 2'),
    ('3', 'Option 3'),
    ('4', 'Option 4'),
    ('5', 'Option 5'),
    ]
	answers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=ANSWER_CHOICES, required=False, initial="")

	class Meta:
		model = EasyQuestionAnwers
		fields = ['type_of_quiz','question','option_1','option_2','option_3','option_4','option_5','answer','answers']

class MediumCreateForm(forms.ModelForm):
	ANSWER_CHOICES = [
    ('1', 'Option 1'),
    ('2', 'Option 2'),
    ('3', 'Option 3'),
    ('4', 'Option 4'),
    ('5', 'Option 5'),
    ]
	answers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=ANSWER_CHOICES, required=False, initial="")

	class Meta:
		model = MediumQuestionAnwers
		fields = ['type_of_quiz','question','option_1','option_2','option_3','option_4','option_5','answer','answers']

class HardCreateForm(forms.ModelForm):
	ANSWER_CHOICES = [
    ('1', 'Option 1'),
    ('2', 'Option 2'),
    ('3', 'Option 3'),
    ('4', 'Option 4'),
    ('5', 'Option 5'),
    ]
	answers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=ANSWER_CHOICES, required=False, initial="")

	class Meta:
		model = HardQuestionAnwers
		fields = ['type_of_quiz','question','option_1','option_2','option_3','option_4','option_5','answer','answers']

class UserDetailForm(forms.ModelForm):

	class Meta:
		model = User_Detail
		fields = ['name','email']
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