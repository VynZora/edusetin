from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    
    # userviews >>>>>>>>>
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path("country/<int:pk>/", views.country_details, name="country_detail"),
    path('uni_detail/<int:pk>/', views.university_detail, name='uni_detail'),
    path("course/<int:pk>/", views.course_detail, name="course_detail"),
    path('gallery/', views.gallery, name='gallery'),


    path("add-team/", views.create_team, name="team_add"),
    path('team/', views.list_team, name='team_list'),
    path('team/<int:pk>/edit/', views.edit_team_member, name='edit_team_member'),
    path('team/<int:pk>/delete/', views.delete_team_member, name='delete_team_member'),

    #gallery
    path("list_image/", views.gallery_view, name="list_image"),
    path("gallery/category/<int:category_id>/", views.gallery_view, name="gallery_by_category"),
    path("gallery/add-category/", views.add_category, name="add_category"),
    path("add_image/", views.add_image, name="add_image"),

    #contact
    path("contact/submit/", views.contact_submit, name="contact_submit"),
    path("admin_contacts/", views.admin_contacts, name="admin_contacts"),
    path("admin/contacts/export/", views.export_contacts_excel, name="export_contacts_excel"),

    #blogs
    path('blog/<int:blog_id>/', views.blog_details, name='blog_detail'),
    path('apply-form/', views.apply_form, name='apply-form'),
    # path('country/', views.country, name='country'),
    path('country-details/', views.country_details, name='country-details'),
    

    # adminviews >>
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),

    path('countries/', views.country_list, name='country_list'),
    path('countries-create/', views.country_create, name='create_country'),
    path('countries/<int:pk>/update/', views.country_update, name='update_country'),
    path('countries/<int:pk>/delete/', views.country_delete, name='delete_country'),
    
    path('create-universities/', views.add_university, name='create-universities'),
    path('uni-list/', views.university_list, name='uni-list'),
    path("universities/update/<int:pk>/", views.update_university, name="update_university"),
    path("universities/delete/<int:pk>/", views.delete_university, name="delete_university"),

    # create cousre
    path("courses/", views.course_list, name="course_list"),
    path("add-courses/", views.course_add, name="course_add"),


    path("testimonials/", views.testimonial_list, name="testimonial_list"),
    path("add-review", views.testimonial_create, name="testimonial_create"),
    path("testimonials/<int:pk>/edit/", views.testimonial_update, name="testimonial_update"),
    path("testimonials/<int:pk>/delete/", views.testimonial_delete, name="testimonial_delete"),


    path("courses/<int:pk>/edit/", views.course_update, name="update_course"),
    path("courses/<int:pk>/delete/", views.course_delete, name="course_delete"),


    # Services
    path('service-detail/<int:pk>/', views.service_detail, name='service_detail'),
    path("services/", views.service_list, name="service_list"),
    path("add-services", views.service_create, name="service_create"),
    path("services/<int:pk>/edit/", views.service_update, name="service_update"),
    path("services/<int:pk>/delete/", views.service_delete, name="service_delete"),

    # Blogs
    path("blogs/", views.blog_list, name="blog_list"),
    path("add-blogs/", views.blog_create, name="blog_create"),
    path("blogs/<int:pk>/edit/", views.blog_update, name="blog_update"),
    path("blogs/<int:pk>/delete/", views.blog_delete, name="blog_delete"),

    path("upload-form/", views.upload_application_form, name="upload_application_form"),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'edusetin_app.views.page_404'