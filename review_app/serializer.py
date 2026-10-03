from rest_framework import serializers
from .models import Project,Profile


class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Project
		fields = ('creator','landing_pic','short_description','long_description')

class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ('creator','username','bio','username','p_pic')

