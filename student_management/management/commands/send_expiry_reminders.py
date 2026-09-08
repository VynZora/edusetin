from django.core.management.base import BaseCommand
from student_management.reminders import send_expiry_reminders_job


class Command(BaseCommand):
    help = "Send expiry reminder emails to eligible students"

    def handle(self, *args, **options):
        result = send_expiry_reminders_job()
        self.stdout.write(self.style.SUCCESS(str(result)))