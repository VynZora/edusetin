import datetime
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Payment


@shared_task
def send_plan_expiry_reminders():
    now = timezone.now()
    today = now.date()

    # Anything within 2 days of expiring, OR already expired.
    # No lower bound — we keep reminding after expiry until renewal.
    candidates = (
        Payment.objects.filter(
            status=Payment.STATUS_SUCCESS,
            expires_at__isnull=False,
            expires_at__lte=now + datetime.timedelta(days=2),
        )
        .exclude(last_expiry_reminder_sent=today)  # already emailed today
        .select_related('student__user', 'plan')
    )

    sent = 0
    for payment in candidates:
        student = payment.student

        # Has the student already taken a newer active/future plan?
        renewed = (
            student.payments.filter(status=Payment.STATUS_SUCCESS)
            .exclude(pk=payment.pk)
            .filter(expires_at__gt=payment.expires_at)
            .exists()
        )
        if renewed:
            continue

        if not student.user.email:
            continue

        _send_expiry_reminder_email(student, payment, now)

        payment.last_expiry_reminder_sent = today
        payment.save(update_fields=['last_expiry_reminder_sent'])
        sent += 1

    return f"Sent {sent} expiry reminder email(s)."


def _send_expiry_reminder_email(student, payment, now):
    days_left = (payment.expires_at - now).days
    plan_name = payment.plan.name

    if payment.expires_at <= now:
        subject = f"Your {plan_name} plan has expired"
        when_line = f"expired on {payment.expires_at.strftime('%d %b %Y')}"
    elif days_left <= 0:
        subject = f"Your {plan_name} plan expires today"
        when_line = "expires today"
    else:
        subject = f"Your {plan_name} plan expires in {days_left} day{'s' if days_left != 1 else ''}"
        when_line = f"expires in {days_left} day{'s' if days_left != 1 else ''} (on {payment.expires_at.strftime('%d %b %Y')})"

    body = (
        f"Hi {student.full_name},\n\n"
        f"Your subscription to the {plan_name} plan {when_line}.\n\n"
        f"Renew now to keep uninterrupted access to your exams and quizzes.\n\n"
        f"Thanks,\n"
        f"The Edusetin Team"
    )

    send_mail(
        subject=subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[student.user.email],
        fail_silently=True,
    )