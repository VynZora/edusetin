from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404,redirect
from .models import Country,University,Course,TeamMember,Testimonial,Blog,Service,Category,GalleryImage,ApplicationForm,ContactMessage
from django.core.paginator import Paginator
from .forms import CountryForm,UniversityForm,CourseForm,TeamMemberForm,TestimonialForm,BlogForm,ServiceForm,CategoryForm,GalleryImageForm,ContactMessageForm
from django.contrib import messages
import math
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# user side >>>>
def index(request):
    print(">>> Entering index view")
    countries = Country.objects.all()
    team_members = TeamMember.objects.all()
    universities = University.objects.all()
    services = Service.objects.all()
    testimonials = Testimonial.objects.all()
    blogs = Blog.objects.all()
    print(">>>>>>>>>>>>>>>>>>>>.Countries in index:", countries)
    print(">>>>>>>>>>>>>>>>>>>>.Countries in index:", team_members)
    return render(request, "index.html", {"countries": countries,"team_members":team_members,"services":services,"universities":universities,"testimonials":testimonials,"blogs":blogs} )

def country_details(request, pk):
    country = get_object_or_404(Country, pk=pk)
    countries = Country.objects.exclude(pk=pk)  # other countries
    print(">>> Country detail:", country)
    universities = country.universities.all().order_by("-created_at")


    return render(request, "country-details.html", {
        "country": country,
        "countries": countries,
        "universities": universities
    })


def university_detail(request, pk):
    university = get_object_or_404(University, id=pk)
    courses = Course.objects.filter(university=university)
    application_form = ApplicationForm.objects.last()
    
    # Calculate course groups (3 courses per slide)
    courses_per_slide = 3
    course_groups_count = math.ceil(courses.count() / courses_per_slide)
    
    context = {
        'university': university,
        'courses': courses,
        'course_groups_count': course_groups_count,
        "application_form": application_form
    }
    return render(request, 'university_detail.html', context)



def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, "course-detail.html", {"course": course})



def about(request):
    team_members = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()

    return render(request, 'about.html',{"team_members":team_members,"testimonials":testimonials})


def blog_details(request, blog_id):
    # Get the current blog post
    blog = get_object_or_404(Blog, id=blog_id)
    
    # Get recent blogs for sidebar (excluding current blog)
    recent_blogs = Blog.objects.exclude(id=blog_id).order_by('-created_at')[:5]
    
    # Get related blogs (you can customize this logic)
    related_blogs = Blog.objects.exclude(id=blog_id).order_by('-created_at')[:3]
    
    context = {
        'blog': blog,
        'recent_blogs': recent_blogs,
        'related_blogs': related_blogs,
    }
    
    return render(request, 'blog_details.html', context)

def apply_form(request):
    return render(request, 'apply-form.html')



def contact_submit(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect(request.META.get("HTTP_REFERER", "/"))
    else:
        form = ContactMessageForm()
    return render(request, "university_detail.html", {"form": form})


# Admin-side list messages (custom page)
def admin_contacts(request):
    contacts = ContactMessage.objects.all().order_by("-created_at")

    # Date filter
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    if start_date and end_date:
        contacts = contacts.filter(created_at__date__range=[start_date, end_date])

    paginator = Paginator(contacts, 10)  # 10 per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "admin_pages/contact_list.html", {"contacts": page_obj})


# Export to Excel/CSV
def export_contacts_excel(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    contacts = ContactMessage.objects.all()
    if start_date and end_date:
        contacts = contacts.filter(created_at__date__range=[start_date, end_date])

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="contacts_{datetime.date.today()}.csv"'

    writer = csv.writer(response)
    writer.writerow(["Name", "Email", "Phone", "Message", "Created At"])

    for c in contacts:
        writer.writerow([c.name, c.email, c.phone, c.message, c.created_at])

    return response


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, "service_detail.html", {"service": service})


def gallery(request):
    categories = Category.objects.all()
    images = GalleryImage.objects.all()
    return render(request, "gallery.html", {
        "categories": categories,
        "images": images
    })


def admin_dashboard(request):
    return render(request, 'admin_pages/admin-dashboard.html')



def page_404(request, exception):
    return render(request, '404.html', status=404)


def country_list(request):
    countries_qs = Country.objects.all()
    paginator = Paginator(countries_qs, 6)  # 10 per page
    page_number = request.GET.get('page')
    countries = paginator.get_page(page_number)
    return render(request, "admin_pages/country_list.html", {"countries": countries})

def country_create(request):
    if request.method == "POST":
        form = CountryForm(request.POST, request.FILES)
        if form.is_valid():
            country = form.save()
            
            messages.success(request, "Country created successfully.")
            return redirect("country_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CountryForm()
    return render(request, "admin_pages/create-country.html", {"form": form})

def country_update(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == "POST":
        form = CountryForm(request.POST, request.FILES, instance=country)
        if form.is_valid():
            country = form.save()
            
            messages.success(request, "Country updated successfully.")
            return redirect("country_list")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CountryForm(instance=country)
    return render(request, "admin_pages/country_list.html", {"form": form, "country": country})

def country_delete(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == "POST":
        country.delete()
        messages.success(request, "Country deleted successfully.")
        return redirect("country_list")
    return render(request, "admin_pages/country_list.html", {"country": country})


def add_university(request):
    countries = Country.objects.all()

    if request.method == "POST":
        form = UniversityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "University added successfully!")
            return redirect('uni-list')
    else:
        form = UniversityForm()

    context = {
        'form': form,
        'countries': countries
    }
    return render(request, 'admin_pages/create_university.html', context)



def university_list(request):
    universities = University.objects.select_related("country").all()
    countries = Country.objects.all()  # for filter dropdown if needed

    paginator = Paginator(universities, 6)  # Show 10 countries per page
    page = request.GET.get('page')
    universities = paginator.get_page(page)

    context = {
        "universities": universities,
        "countries": countries,
    }
    return render(request, "admin_pages/university_list.html", context) 



# Update university
def update_university(request, pk):
    university = get_object_or_404(University, pk=pk)
    if request.method == "POST":
        form = UniversityForm(request.POST, request.FILES, instance=university)
        if form.is_valid():
            form.save()
            messages.success(request, "University updated successfully!")
            return redirect("uni-list")
    else:
        form = UniversityForm(instance=university)

    context = {"form": form, "university": university}
    return render(request, "admin_pages/update_university.html", context)


#  Delete university
def delete_university(request, pk):
    university = get_object_or_404(University, pk=pk)
    if request.method == "POST":  # confirmation before delete
        university.delete()
        messages.success(request, "University deleted successfully!")
        return redirect("uni-list")

    context = {"university": university}
    return render(request, "admin_pages/delete_university.html", context)



def course_list(request):
    courses_qs = Course.objects.select_related("university__country").all().order_by("-id")

    # paginate (10 courses per page, you can change the number)
    paginator = Paginator(courses_qs, 6)
    page_number = request.GET.get("page")
    courses = paginator.get_page(page_number)  # this gives you a Page object

    universities = University.objects.select_related("country").all()

    return render(request, "admin_pages/course_list.html", {
        "courses": courses,            # now a Page object, works with your template
        "universities": universities,
    })

# Add new course
def course_add(request):

    print("ebtererrere")
    if request.method == "POST":
        form = CourseForm(request.POST,request.FILES)
        print(form)
        if form.is_valid():
            form.save()
            return redirect("course_list")  # update with your course list url name
    else:
        form = CourseForm()
        
    universities = University.objects.select_related("country").all()

    
    return render(request, "admin_pages/course_create.html", {"form": form, "universities":universities}) 

#  Update course
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    universities = University.objects.select_related("country").all()  # Get all universities

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect("course_list")
    else:
        form = CourseForm(instance=course)

    # In case of form errors, we need to render the course_list template with the form and the universities
    courses = Course.objects.select_related("university__country").all()  # We also need to pass courses for the list
    return render(
        request,
        "admin_pages/course_list.html",
        {
            "form": form,
            "course": course,  # This is for the update modal? Actually, the template expects a queryset of courses
            "courses": courses,  # We need to pass the courses for the list
            "universities": universities,  # pass to template
        }
    )


# Delete course
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        return redirect("course_list")
    return render(request, "admin_pages/course_list.html", {"course": course})




@csrf_exempt
def ckeditor_upload(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        file_extension = os.path.splitext(upload.name)[1].lower()
        
        # Check if the uploaded file is an image or a PDF
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            folder = 'images'
        elif file_extension == '.pdf':
            folder = 'pdfs'
        else:
            return JsonResponse({'uploaded': False, 'error': 'Unsupported file type.'})

        # Save the file in the appropriate folder
        file_name = default_storage.save(f'{folder}/{upload.name}', ContentFile(upload.read()))
        file_url = default_storage.url(file_name)
        return JsonResponse({
            'uploaded': True,
            'url': file_url
        })
    
    return JsonResponse({'uploaded': False, 'error': 'No file was uploaded.'})



def list_team(request):
    """Display all team members with pagination"""
    team_members_list = TeamMember.objects.all().order_by('name')
    paginator = Paginator(team_members_list, 6)  # Show 10 per page
    page_number = request.GET.get('page')
    team_members = paginator.get_page(page_number)  # handles invalid pages automatically

    context = {
        'team_members': team_members,
        'title': 'Team Members',
    }
    return render(request, 'admin_pages/team_list.html', context)


def create_team(request):
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member added successfully!')
            return redirect('team_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = TeamMemberForm()

    return render(request, 'admin_pages/add_team.html', {'form': form})

def edit_team_member(request, pk):
    team_member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES, instance=team_member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team member updated successfully!')
            return redirect('team_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeamMemberForm(instance=team_member)
    
    return render(request, 'admin_pages/edit_team_member.html', {
        'form': form,
        'team_member': team_member
    })

def delete_team_member(request, pk):
    team_member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        team_member.delete()
        messages.success(request, 'Team member deleted successfully!')
        return redirect('team_list')
    
    return render(request, 'admin_pages/confirm_delete.html', {'team_member': team_member})



# List all testimonials
def testimonial_list(request):
    testimonials = Testimonial.objects.all()
    return render(request, "admin_pages/review_list.html", {"testimonials": testimonials})


def testimonial_list(request):
    testimonials_list = Testimonial.objects.all().order_by('name')  # or any ordering field
    paginator = Paginator(testimonials_list, 6)  # 10 testimonials per page
    page_number = request.GET.get('page')
    testimonials = paginator.get_page(page_number)  # returns a Page object

    return render(request, "admin_pages/review_list.html", {"testimonials": testimonials})

# Add testimonial
def testimonial_create(request):
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial added successfully!")
            return redirect("testimonial_list")
    else:
        form = TestimonialForm()
    return render(request, "admin_pages/create_review.html", {"form": form})

# Update testimonial
def testimonial_update(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            messages.success(request, "Testimonial updated successfully!")
            return redirect("testimonial_list")
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, "testimonials/testimonial_form.html", {"form": form, "testimonial": testimonial})

# Delete testimonial
def testimonial_delete(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == "POST":
        testimonial.delete()
        messages.success(request, "Testimonial deleted successfully!")
        return redirect("testimonial_list")
    return render(request, "testimonials/testimonial_confirm_delete.html", {"testimonial": testimonial})



# --------- Services ---------

def service_list(request):
    services_list = Service.objects.all().order_by('title') # or any field
    paginator = Paginator(services_list, 6)  # 10 services per page
    page_number = request.GET.get('page')
    services = paginator.get_page(page_number)  # returns a Page object

    return render(request, "admin_pages/service_list.html", {"services": services})

def service_create(request):
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Service added successfully!")
            return redirect("service_list")
    else:
        form = ServiceForm()
    return render(request, "admin_pages/create_service.html", {"form": form})

def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Service updated successfully!")
            return redirect("service_list")
    else:
        form = ServiceForm(instance=service)
    return render(request, "admin_pages/service_list.html", {"form": form, "service": service})

def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service.delete()
        messages.success(request, "Service deleted successfully!")
        return redirect("service_list")
    return render(request, "admin_pages/service_list.html", {"service": service})


# --------- Blogs ---------
def blog_list(request):
    blogs_qs = Blog.objects.all().order_by("-id")  # newest first

    paginator = Paginator(blogs_qs, 6)  # show 10 blogs per page
    page_number = request.GET.get("page")
    blogs = paginator.get_page(page_number)  # gives a Page object

    return render(request, "admin_pages/blog_list.html", {
        "blogs": blogs
    })

def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog added successfully!")
            return redirect("blog_list")
    else:
        form = BlogForm()
    return render(request, "admin_pages/create_blog.html", {"form": form})

def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully!")
            return redirect("blog_list")
    else:
        form = BlogForm(instance=blog)
    return render(request, "admin_pages/create_blog.html", {"form": form, "blog": blog})

def blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        blog.delete()
        messages.success(request, "Blog deleted successfully!")
        return redirect("blog_list")
    return render(request, "admin_pages/create_blog.html", {"blog": blog})



# Show all images and filter by category
def gallery_view(request, category_id=None):
    categories = Category.objects.all()
    if category_id:
        images = GalleryImage.objects.filter(category_id=category_id)
        active_category = get_object_or_404(Category, id=category_id)
    else:
        images = GalleryImage.objects.all()
        active_category = None

    return render(request, "admin_pages/image_list.html", {
        "categories": categories,
        "images": images,
        "active_category": active_category,
    })


# Add category
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'category_id': category.id,
                    'category_name': category.name
                })
            
            messages.success(request, 'Category added successfully!')
            return redirect('gallery_list')
        else:
            # AJAX response for errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Please correct the errors below.',
                    'errors': form.errors
                })
            
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CategoryForm()
    
    # For regular requests, render the template
    return render(request, 'gallery/add_image.html', {'form': form})


# Add image
def add_image(request):
    categories = Category.objects.all()
    
    if request.method == "POST":
        category_id = request.POST.get("category")
        category = Category.objects.get(id=category_id)
        files = request.FILES.getlist("images")

        for file in files:
            GalleryImage.objects.create(
                category=category,
                title=file.name,   # default title = filename
                image=file
            )
        return redirect("list_image")

    return render(request, "admin_pages/add_image.html", {"categories": categories})



def upload_application_form(request):
    if request.method == "POST":
        title = request.POST.get("title")
        pdf = request.FILES.get("pdf")

        if pdf and pdf.name.endswith(".pdf"):
            ApplicationForm.objects.create(title=title, pdf=pdf)
            return redirect("upload_application_form")  # reload page

    forms = ApplicationForm.objects.all()
    return render(request, "admin_pages/add_application_form.html", {"forms": forms})