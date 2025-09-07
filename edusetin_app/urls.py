from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),

    # edusetin
    path('test-preparation-details/', views.test_preparation_details, name='test_preparation_details'),
    path('visa-guidance-details/', views.visa_guidance_details, name='visa_guidance_details'),
    path('application-process-details/', views.application_process_details, name='application_process_details'),
    path('course-selection-details/', views.course_selection_details, name='course_selection_details'),
    path('career-counselling-details/', views.career_counselling_details, name='career_counselling_details'),

    path('united-kingdom/', views.united_kingdom_details, name='united_kingdom_details'),
    path('germany/', views.germany_details, name='germany_details'),
    path('italy/', views.italy_details, name='italy_details'),
    path('dubai/', views.dubai_details, name='dubai_details'),
    path('kyrgyzstan/', views.kyrgyzstan_details, name='kyrgyzstan_details'),

    path('harvard-university/', views.harvard_details, name='harvard_details'),
    path('oxford-university/', views.oxford_details, name='oxford_details'),
    path('bologna-university/', views.bologna_details, name='bologna_details'),
    path('sapienza-university/', views.sapienza_details, name='sapienza_details'),
    path('ludwig-university/', views.ludwig_details, name='ludwig_details'),
    path('asian-medical-institute/', views.asian_medical_institute_details, name='asian_medical_institute_details'),
    path('kyrgyz-state-academy/', views.kyrgyz_state_academy_details, name='kyrgyz_state_academy_details'),

    path('business-management/', views.business_management, name='business_management_details'),
    path('engineering/', views.engineering, name='engineering_details'),
    path('health-and-medicine/', views.health_and_medicine, name='health_medicine_details'),





    path('blogs/', views.blogs, name='blogs'),
    path('blog_details/', views.blog_details, name='blog_details'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('apply-form/', views.apply_form, name='apply-form'),
    path('country/', views.country, name='country'),
    path('country-details/', views.country_details, name='country-details'),
    path('course/', views.course, name='course'),
    path('gallery/', views.gallery, name='gallery'),
    path('course-details/', views.course_details, name='course-details'),
    path('service-details/', views.service_details, name='service-details'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'edusetin_app.views.page_404'