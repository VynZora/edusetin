from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Country, University, Blog, Service, CourseCategory

class EdusetinSitemap(Sitemap):
    protocol = "https"
    def get_domain(self, site=None):
        return "edusetin.com"
class StaticViewSitemap(EdusetinSitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return [
            "index",
            "about",
            "gallery",
            "index_blog",
            "course_list",
            "uni-list",
            "country_list",
            "service_list",
            "course_category_list",
            "contact_us",
            "apply_form",
        ]

    def location(self, item):
        return reverse(item)


class CountrySitemap(EdusetinSitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Country.objects.all()

    def location(self, obj):
        return reverse("country_detail", kwargs={"slug": obj.slug})


class UniversitySitemap(EdusetinSitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return University.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse("uni_detail", kwargs={"slug": obj.slug})


class CourseCategorySitemap(EdusetinSitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return CourseCategory.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse("course_category_detail", kwargs={"slug": obj.slug})


class BlogSitemap(EdusetinSitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse("blog_detail", kwargs={"slug": obj.slug})


class ServiceSitemap(EdusetinSitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Service.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse("service_detail", kwargs={"slug": obj.slug})