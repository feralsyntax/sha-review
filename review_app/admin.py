from django.contrib import admin
from review_app.models import Project,vote

# Register your models here.
admin.site.site_header = 'shaReview Admin'
admin.site.site_title = 'shaReview Admin Platform'
admin.site.index_title = 'Welcome to your shaReview Admin Platform'


class voteInLine(admin.TabularInline):
	model = vote
	extra = 3

class ProjectAdmin(admin.ModelAdmin):
	fieldsets = [(None,{'fields':['creator','landing_pic','short_description','long_description','support_pic_a','support_pic_b']}),]
	inlines = [voteInLine]

admin.site.register(Project,ProjectAdmin)