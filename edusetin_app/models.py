from django.db import models
# from ckeditor.fields import RichTextField

# class Service(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     description = RichTextField()  # Rich text description of the service

#     # File uploads
#     application_form = models.FileField(
#         upload_to='services/forms/',
#         blank=True,
#         null=True,
#         help_text="Upload Application Form (PDF only)"
#     )
#     terms_and_conditions = models.FileField(
#         upload_to='services/terms/',
#         blank=True,
#         null=True,
#         help_text="Upload Terms & Conditions File"
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         verbose_name = "Service"
#         verbose_name_plural = "Services"

#     def __str__(self):
#         return self.name


# class ServiceStep(models.Model):
#     service = models.ForeignKey(Service, related_name="steps", on_delete=models.CASCADE)
#     heading = models.CharField(max_length=255)
#     description = models.TextField()  # plain text instead of RichTextField

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['id']  # Auto step numbering by order of creation

#     def __str__(self):
#         return f"{self.service.name} - Step {self.pk}: {self.heading}"
