from django import forms
from .models import Profile,Project,Contact,vote


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['p_pic','bio','username']
		exclude = ['creator']

class BioForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = ['p_pic','creator']


class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['landing_pic','short_description','long_description','support_pic_a','support_pic_b', 'demo_url']
		exclude = ['your_vote']

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact
		fields = ['first_name','last_name','email','phone','address']
		exclude = ['creator']

class VoteForm(forms.ModelForm):
	class Meta:
		model = vote
		extra = 3
		fields = ['vote_design','vote_usability','vote_content']
		exclude = ['project','choice_text','your_vote']
