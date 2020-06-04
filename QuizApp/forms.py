from django import forms
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