from django import forms
from models import *
from django.contrib.auth.models import User
from django.core.validators import validate_email, RegexValidator
from gotravel.choice import *
from multiupload.fields import MultiFileField


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 30, label = 'Username', 
        validators = [RegexValidator(r'^[0-9a-zA-Z]*$',
        message='Please enter only letters and numbers for username')])
    last_name = forms.CharField(max_length = 30, label = 'Last Name', required = True)
    first_name = forms.CharField(max_length = 30, label = 'First Name', required = True)
    email = forms.CharField(max_length = 40, label = 'Email', validators = [validate_email])
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()
        print cleaned_data

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

    # Customizes form validation for the email field.
    def clean_email(self):
        # Confirms that the username is not already present in the
        # User model database.
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("An account using this email address has already exists.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return email

class EditProfileForm(forms.ModelForm):
    #last_name = forms.CharField(max_length = 30, label = 'Last Name', required = True)
    #first_name = forms.CharField(max_length = 30, label = 'First Name', required = True)
    #age = forms.CharField(max_length = 30, label = 'Age')
    #bio = forms.CharField(max_length = 430, label = 'Introduction')
    
    class Meta:
        model= Profile
        fields=('last_name','first_name','age','bio',)
        #widgets = {'image':forms.FileInput()}
    
    gender = forms.ChoiceField(choices = GENDER_CHOICES, label="Gender", initial='M', widget=forms.Select(), required=True)
    image = forms.FileField(label='Change profile image', required=False)

    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(EditProfileForm, self).clean()
        print cleaned_data
        # Generally return the cleaned data we got from our parent.
        return cleaned_data

class EditNoteForm(forms.ModelForm):
    
    class Meta:
        model = Note
        fields = ('note_title',)
    
    title_image = forms.FileField(label='Add a title image', required=False)

    def clean(self):
        cleaned_data = super(EditNoteForm, self).clean()
        print cleaned_data
        return cleaned_data

class EditNoteDetailForm(forms.ModelForm):
    
    class Meta:
        model = NoteDetail
        fields = ('place','content','cost',)
    
    time = forms.DateField(widget=forms.SelectDateWidget(
        empty_label=("Choose Year", "Choose Month", "Choose Day"),
    ),)
    picture = forms.FileField(label='Upload Picture', required=False)
    multiple = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)


    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(EditNoteDetailForm, self).clean()
        print cleaned_data
        # Generally return the cleaned data we got from our parent.
        return cleaned_data

class EditPlanForm(forms.ModelForm):
    
    class Meta:
        model = Plan
        fields = ('plan_title',)
    
    def clean(self):
        cleaned_data = super(EditPlanForm, self).clean()
        print cleaned_data
        return cleaned_data

class EditPlanDetailForm(forms.ModelForm):
    
    class Meta:
        model = PlanDetail
        exclude = (
            'owner',
        )

    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(EditPlanDetailForm, self).clean()
        print cleaned_data
        # Generally return the cleaned data we got from our parent.
        return cleaned_data