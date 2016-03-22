from django import forms
from models import *
from django.contrib.auth.models import User
from django.core.validators import validate_email, RegexValidator


class RegistrationForm(forms.Form):
	username = forms.CharField(max_length = 30,validators = [RegexValidator(r'^[0-9a-zA-Z]*$',
		message='Please enter only letters and numbers for username')])
	last_name = forms.CharField(max_length = 30, label = 'Last Name', required = True)
	first_name = forms.CharField(max_length = 30, label = 'First Name', required = True)
	email      = forms.CharField(max_length = 40, validators = [validate_email])
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


	# Customizes form validation for username field.
	#def clean_username(self):
		# Confirms that the username is not already present in the
		# User model database.
		# = self.cleaned_data.get('username')
		#if User.objects.filter(username__exact=username):
			#raise forms.ValidationError("Username is already taken.")

		# We must return the cleaned data we got from the cleaned_data
		# dictionary
		#return username

	# Customizes form validation for email field.
	def clean_username(self):
		# Confirms that the email is not already present in the
		# User model database.
		email = self.cleaned_data.get('email')
		if User.objects.filter(email__exact=email):
			raise forms.ValidationError("An account with this email address already exists")

		# We must return the cleaned data we got from the cleaned_data
		# dictionary
		return email

class EditProfileForm(forms.ModelForm):
	#last_name = forms.CharField(max_length = 30, label = 'Last Name', required = True)
	#first_name = forms.CharField(max_length = 30, label = 'First Name', required = True)

	class Meta:
		model= Profile
		fields=('last_name','first_name','age','bio',)
		#widgets = {'image':forms.FileInput()}

	image = forms.FileField(required=False, label='Change profile image')

	def clean(self):
		# Calls our parent (forms.Form) .clean function, gets a dictionary
		# of cleaned data as a result
		cleaned_data = super(EditProfileForm, self).clean()
		print cleaned_data
		# Generally return the cleaned data we got from our parent.
		return cleaned_data

#class CreateProfileForm(forms.ModelForm):
#    class Meta:
#        model = Profile
#       fields=('last_name','first_name','age','bio','image',)
#		widgets = {'image':forms.FileInput()}






