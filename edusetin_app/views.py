from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def application_process_details(request):
    return render(request, 'edusetin/application-process-details.html')

def career_counselling_details(request):
    return render(request, 'edusetin/career-counselling-details.html')

def course_selection_details(request):
    return render(request, 'edusetin/course-selection-details.html')

def test_preparation_details(request):
    return render(request, 'edusetin/test-preparation-details.html')

def visa_guidance_details(request):
    return render(request, 'edusetin/visa-guidance-details.html')


def united_kingdom_details(request):
    return render(request, 'edusetin/united-kingdom-details.html')

def germany_details(request):
    return render(request, 'edusetin/germany-details.html')

def italy_details(request):
    return render(request, 'edusetin/italy-details.html')

def dubai_details(request):
    return render(request, 'edusetin/dubai-details.html')

def kyrgyzstan_details(request):
    return render(request, 'edusetin/kyrgyzstan-details.html')

# Harvard University
def harvard_details(request):
    return render(request, 'edusetin/harvard-university-details.html')

# University of Oxford
def oxford_details(request):
    return render(request, 'edusetin/oxford-university-details.html')

# University of Bologna
def bologna_details(request):
    return render(request, 'edusetin/bologna-university-details.html')

# Sapienza University of Rome
def sapienza_details(request):
    return render(request, 'edusetin/sapienza-university-details.html')

# Ludwig Maximilian University of Munich
def ludwig_details(request):
    return render(request, 'edusetin/ludwig-university-details.html')

# Asian Medical Institute
def asian_medical_institute_details(request):
    return render(request, 'edusetin/asian-medical-institute-details.html')

# Kyrgyz State Medical Academy
def kyrgyz_state_academy_details(request):
    return render(request, 'edusetin/kyrgyz-state-academy-details.html')

def business_management(request):
    return render(request, 'edusetin/business-management.html')

def engineering(request):
    return render(request, 'edusetin/engineering.html')

def health_and_medicine(request):
    return render(request, 'edusetin/health-and-medicine.html')



def blogs(request):
    return render(request, 'blogs.html')

def blog_details(request):
    return render(request, 'blog_details.html')

def apply_form(request):
    return render(request, 'apply-form.html')

def contact_us(request):
    return render(request, 'contact-us.html')



def course(request):
    return render(request, 'course.html')

def course_details(request):
    return render(request, 'course-details.html')

def service_details(request):
    return render(request, 'service-details.html')


def gallery(request):
    return render(request, 'gallery.html')


def country(request):
    return render(request, 'country.html')

def country_details(request):
    return render(request, 'country-details.html')

def admin_dashboard(request):
    return render(request, 'admin_pages/admin-dashboard.html')




def page_404(request, exception):
    return render(request, '404.html', status=404)
