from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
import datetime as dt
from django.template import RequestContext
from review_app.forms import ProjectForm,ProfileForm,BioForm,ContactForm,VoteForm
from review_app.models import Profile,Project,Contact,vote
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from review_app.serializer import ProjectSerializer,ProfileSerializer
from review_app.permissions import IsAdminOrReadOnly,IsAuthenticatedOrReadOnly
from django.urls import reverse
from django.db.models import Sum,Count,Avg


# Create your views here.
@login_required(login_url='/accounts/login/')
def new_project(request):
	current_user = request.user

	if request.method == 'POST':
		projform = ProjectForm(request.POST, request.FILES)
		if projform.is_valid():
			print('valid!')
			landing_pic = projform.cleaned_data['landing_pic']
			short_description = projform.cleaned_data['short_description']
			long_description = projform.cleaned_data['long_description']
			support_pic_a = projform.cleaned_data['support_pic_a']
			support_pic_b = projform.cleaned_data['support_pic_b']
			demo_url = projform.cleaned_data['demo_url']
			project = Project(landing_pic=landing_pic,short_description=short_description,long_description=long_description,support_pic_a=support_pic_a,support_pic_b=support_pic_b,demo_url=demo_url)
			project.creator = current_user
			project.save()
		return redirect('home')
	else:
		projform = ProjectForm()

	title = 'Add Project'

	return render(request, 'user/upload.html',{"projform": projform,"title":title})

def search_results(request):

	if 'project' in request.GET and request.GET["project"]:
		search_term = request.GET.get("project")
		searched_projects = Project.search_by_term(search_term)
		message = f"{search_term}"

		return render(request,'projects/search_results.html',{"message":message,"projects":searched_projects})
	else:
		message = "You haven't searched for an image yet"

		return render(request,'projects/search_results.html',{"message":message})


@login_required(login_url='/accounts/login/')
def home(request):
	date = dt.date.today()
	projects = Project.objects.all()
	fprojects = Project.objects.all()[:12]

	title = 'Home'
	return render(request, 'projects/index.html', {"projects": projects,"title": title,"date":date,"fprojects":fprojects})

def profile(request,user_id):
	projects = Project.objects.filter(creator_id=user_id)
	profile = Profile.objects.filter(creator_id=user_id).last()
	contact = Contact.objects.filter(pk=user_id).first()
	current_user = request.user

	if request.method == 'POST':
		pform = ProfileForm(request.POST, request.FILES)
		if pform.is_valid():
			print('valid!')
			p_pic = pform.cleaned_data['p_pic']
			bio = pform.cleaned_data['bio']
			username = pform.cleaned_data['username']
			profile = Profile(p_pic=p_pic,bio=bio,username=username)
			profile.creator = current_user
			profile.save()
		return redirect('profile', user_id)
	else:
		pform = ProfileForm()

	title = 'Profile'

	return render(request, 'user/profile.html', {"projects": projects, "pform": pform, "profile": profile, "title": title,"contact":contact})

# def bio(request,user_id):
# 	current_user = request.user
# 	if request.method == 'POST':
# 		bioform = BioForm(request.POST)
# 		if bioform.is_valid():
# 			print('valid!')
# 			bio = bioform.cleaned_data['bio']
# 			bprofile = Profile(bio=bio)
# 			bprofile.creator = current_user
# 			bprofile.save()
# 			return redirect('profile', user_id)
# 	else:
# 		bioform = BioForm()
#
# 	title = 'Add/Update Bio'
#
# 	return render(request, 'user/bio.html', {"bioform": bioform,"title":title})

def bio(request,user_id):
	current_user = request.user
	if request.method == 'POST':
		profileform = ProfileForm(request.POST)
		if profileform.is_valid():
			print('valid!')
			username = profileform.cleaned_data['username']
			p_pic = profileform.cleaned_data['p_pic']
			bio = profileform.cleaned_data['bio']
			profile = Profile(p_pic=p_pic, bio=bio,username=username)
			profile.creator = current_user
			profile.save()
			return redirect('profile', user_id)
	else:
		profileform = ProfileForm()

	title = 'Add/Update Bio'

	return render(request, 'user/bio.html', {"profileform": profileform,"title":title})




def project(request,project_id):
	total = vote.objects.filter(project__id=project_id).aggregate(TOTAL=Sum('your_vote'))['TOTAL']
	total_votes = vote.objects.filter(project__id=project_id).annotate(num_votes=Count('your_vote'))
	# last_vote = vote.objects.filter('id')
	# last_vote = vote.objects.filter(project__id=project_id).latest('published')
	# try:
	# average = vote.objects.filter(project__id=project_id).aggregate(Avg('your_vote'))
	design_av = vote.objects.filter(project__id=project_id).aggregate(Avg('vote_design'))
	usability_av = vote.objects.filter(project__id=project_id).aggregate(Avg('vote_usability'))
	content_av = vote.objects.filter(project__id=project_id).aggregate(Avg('vote_content'))
	votes = vote.objects.filter(project__id=project_id)
	project = Project.objects.get(id=project_id)
	# votes = vote.objects.filter(project_id=project_id)
	# votes = vote.objects.get(project_id=project_id)

	# except DoesNotExist:
	# 	raise Http404()

	current_user = request.user
	if request.method == 'POST':
		voteform = VoteForm(request.POST)
		if voteform.is_valid():
			print('valid!')
			vote_design = voteform.cleaned_data['vote_design']
			vote_usability = voteform.cleaned_data['vote_usability']
			vote_content = voteform.cleaned_data['vote_content']
			project_vote = vote(vote_design=vote_design,vote_usability=vote_usability,vote_content=vote_content)
			project_vote.project = project
			project_vote.save()
		return redirect('project',project_id)
	else:
		voteform = VoteForm()

	# votes = project.vote.all()
	# print(votes)
	# print(average)
	# print(last_vote)

	title = 'Project'

	try:
		selected_choice = project.vote_set.get(pk=request.POST['vote'])
	except (KeyError, vote.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'projects/project.html', {
			'project': project,
			'error_message': "You didn't select a choice.","voteform":voteform,"total":total,"total_votes":total_votes,"design_av":design_av,"usability_av":usability_av,"content_av":content_av,"votes":votes})
	else:
		selected_choice.vote_design += 1
		selected_choice.vote_usability += 1
		selected_choice.vote_content += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('project', args=(project.id,)),{"voteform":voteform})

def vote_project(request,project_id):
	project = get_object_or_404(Project, pk=project_id)

# def review(request,user_id):
# 	review = Project.objects.get(pk=1)
#
# 	# Up vote to the object
# 	upvotes = review.votes.up(user_id)
#
# 	# Down vote to the object
# 	downvotes = review.votes.down(user_id)
#
# 	# Removes a vote from the object
# 	delete_votes = review.votes.delete(user_id)
#
# 	# Check if the user already voted (up) the object
# 	check_votes = review.votes.exists(user_id)
#
# 	# Check if the user already voted (down) the object
# 	# import UP, DOWN from vote.models
# 	review.votes.exists(user_id, action=DOWN)
#
# 	# Returns the number of votes for the object
# 	review.votes.count()
#
# 	# Returns a list of users who voted and their voting date
# 	review.votes.user_ids()
#
# 	# Returns all instances voted by user
# 	Project.votes.all(user_id)


@login_required(login_url='/accounts/login')
def api(request):
	date = dt.date.today()
	title = 'API'

	return render(request,'api/api.html',{"date":date,"title":title})

def contact(request,user_id):
	current_user = request.user
	if request.method == 'POST':
		contform = ContactForm(request.POST)
		if contform.is_valid():
			print('valid!')
			first_name = contform.cleaned_data['first_name']
			last_name = contform.cleaned_data['last_name']
			email = contform.cleaned_data['email']
			phone = contform.cleaned_data['phone']
			address = contform.cleaned_data['address']
			pcontact = Contact(first_name=first_name,last_name=last_name,email=email,phone=phone,address=address)
			pcontact.creator = current_user
			pcontact.save()
		return redirect('profile', user_id)
	else:
		contform = ContactForm()

	title = 'Contact Info'

	return render(request, 'user/contact.html', {"contform": contform,"title":title})


class ProjectList(APIView):
	permission_classes = (IsAdminOrReadOnly,IsAuthenticatedOrReadOnly)
	def get(self,request,format=None):
		all_projects = Project.objects.all()
		serializers = ProjectSerializer(all_projects,many=True)
		return Response(serializers.data)

class ProfileList(APIView):
	permission_classes = (IsAdminOrReadOnly, IsAuthenticatedOrReadOnly)
	def get(self,request,format=None):
		all_profiles = Profile.objects.all()
		serialzers = ProfileSerializer(all_profiles, many=True)
		return Response(serialzers.data)
