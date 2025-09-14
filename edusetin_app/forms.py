from django import forms
from .models import Country,University,Course,TeamMember,Testimonial,Blog,Service,Category,GalleryImage,ContactMessage


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ["name", "flag", "image", "description"]


class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['country', 'name', 'image', 'description']
    

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "image", "description", "duration","university"]

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["name", "image", "review", "rating"]

class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['name', 'profession', 'image', 'linkedin', 'github', 'twitter']
       
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False



# --------- Service Form ---------
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["image", "title", "description"]


# --------- Blog Form ---------
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["image", "title", "description"]



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class GalleryImageForm(forms.ModelForm):  # no need
    class Meta:
        model = GalleryImage
        fields = ["category", "title", "image"]


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]