from django.test import TestCase
from .models import Project,Profile,vote,Contact


# Create your tests here.
class ProjectTestClass(TestCase):
	# set up
    def setUp(self):
        self.project = Project(landing_pic='https://mycloudlanding.com',short_description='This is my project',long_description='With a longer description here of what it does',support_pic_a='https://mycloudsays.com',support_pic_b='https://mycloudthis.com',demo_url='https://wearelive.com')

    # instance
    def test_instance(self):
        self.assertTrue(isinstance(self.project,Project))

    # save method
    def project_save_method(self):
        self.project.save()
        projects = Project.objects.all()
        self.assertTrue(len(projects) > 0)

	#search method
    def test_search_by_term(self):
        get_by_term = Project.objects.filter(long_description__icontains=self)
        return get_by_term


class ProfileTestClass(TestCase):

	#set up
	def setUp(self):
		self.profile = Profile(username='janja', bio='ALoha', p_pic='https://mycloudbenie.com')
		self.profile.save()

    #instance
	def test_instance(self):
		self.assertTrue(isinstance(self.profile, Profile))

    # save method
	def test_save_method(self):
		self.profile.save()
		profiles = Profile.objects.all()
		self.assertTrue(len(profiles) > 0)



class VoteTestClass(TestCase):
	# set up & save
	def setUp(self):
		self.new_project = Project(landing_pic='https://mycloudlanding.com', short_description='This is my project',
								   long_description='With a longer description here of what it does',
								   support_pic_a='https://mycloudsays.com', support_pic_b='https://mycloudthis.com',
								   demo_url='https://wearelive.com')
		self.new_project.save()

		self.new_profile = Profile(username='janja', bio='ALoha', p_pic='https://mycloudbenie.com')
		self.new_profile.save()

		self.new_vote = vote(choice_text='Some text here', your_vote=2, vote_design=9, vote_usability=7, vote_content=8,
							 project=self.new_project, profile=self.new_profile)
		self.new_vote.save()

	# instance
	def TestInstance(self):
		self.assertTrue(isinstance(self.new_vote, vote))


class ContactTestClass(TestCase):
	def setUp(self):
		self.contact = Contact(first_name='Benson', last_name='Langat', email='ben@gmail.com', phone='0712345678',
							   address='mbagathi kenya')

	def test_instance(self):
		self.assertTrue(isinstance(self.contact, Contact))

	# test the save method
	def contact_save_method(self):
		self.contact.save()
		contacts = Contact.objects.all()
		self.assertTrue(len(contacts) > 0)
