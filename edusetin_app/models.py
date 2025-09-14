from django.db import models
from PIL import Image, ImageOps
from django.core.validators import MinValueValidator, MaxValueValidator


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    flag = models.ImageField(upload_to="countries/flags/")
    image = models.ImageField(upload_to="countries/images/", blank=True, null=True)  
    description = models.TextField(blank=True, null=True)  

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # First save to generate file path
        super().save(*args, **kwargs)

        # --- Resize Flag (make it small like logo 40x40) ---
        if self.flag:
            flag_path = self.flag.path
            with Image.open(flag_path) as img:
                img = img.convert("RGB")
                img = img.resize((40, 40), Image.LANCZOS)
                img.save(flag_path, quality=90)


class University(models.Model):
    country = models.ForeignKey(Country, related_name="universities", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="universities/")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.country.name})"



class Course(models.Model):
    university = models.ForeignKey(
        University, related_name="courses", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="courses/")
    description = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=100)  # e.g. "3 Years", "6 Months"
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.university.name})"
    



class TeamMember(models.Model):
    name = models.CharField(max_length=100, help_text="Full name of the team member")
    profession = models.CharField(max_length=100, help_text="Role or profession (e.g. Software Engineer)")
    image = models.ImageField(upload_to="team/", blank=True, null=True, help_text="Profile picture")
    
    # Social links (can expand later)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    github = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)
    # personal_website = models.URLField(max_length=200, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.profession}"
    


class Testimonial(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the person giving the testimonial")
    image = models.ImageField(upload_to="testimonials/", blank=True, null=True, help_text="Profile picture")
    review = models.TextField(help_text="Customer or client review")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating out of 5 stars"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} ({self.rating}⭐)"
    


# --------- Services ---------
class Service(models.Model):
    image = models.ImageField(upload_to="services/", help_text="Service image")
    title = models.CharField(max_length=200, help_text="Service title")
    description = models.TextField(help_text="Service description")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


# --------- Blogs ---------
class Blog(models.Model):
    image = models.ImageField(upload_to="blogs/", help_text="Blog cover image")
    title = models.CharField(max_length=200, help_text="Blog title")
    description = models.TextField(help_text="Blog description")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title





class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="images")
    title = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to="gallery/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"
    


class ApplicationForm(models.Model):
    title = models.CharField(max_length=150, default="Application Form")
    pdf = models.FileField(upload_to="application_forms/", help_text="Upload PDF file only")

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"