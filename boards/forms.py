from django import forms
from .models import Topic
class NewTopicForm(forms.ModelForm):
    # init an input for the from
    message_from_django_form = forms.CharField(
        widget=forms.Textarea(attrs={'rows':5, 'placeholder':'What is on your mind?'}),
        max_length=4000,
        help_text='The max length of the text is 4000',
        label='Message' # The label would be generated automatically if we had omitted it, and it will use the name of the  input var as a label(without the underscore)
    )

    class Meta: # helper class
        model = Topic
        fields = ['subject', 'message_from_django_form']