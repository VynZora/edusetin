import logging
import time
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Payment

logger = logging.getLogger(__name__)

REMINDER_DAYS_BEFORE = 2
SEND_DELAY_SECONDS = 5  # increased from 1.2 — see throttle notes below

ZOHO_THROTTLE_MARKERS = ('5.4.6', 'unusual sending activity')

def is_throttle_error(e):
    return any(m in str(e).lower() for m in ZOHO_THROTTLE_MARKERS)


def send_expiry_reminders_job():
    now = timezone.now()
    today = now.date()
    sent, skipped = 0, 0
    skip_reasons = {}

    def record_skip(reason):
        skip_reasons[reason] = skip_reasons.get(reason, 0) + 1

    # No `request` object anymore — build the URL from a setting instead
    plans_path = reverse('student_portal:plan_list')
    plans_url = f"{settings.SITE_BASE_URL}{plans_path}"

    latest_by_student = {}
    qs = (
        Payment.objects
        .filter(status=Payment.STATUS_SUCCESS, expires_at__isnull=False)
        .select_related('student__user', 'plan')
        .order_by('expires_at')
    )
    for p in qs:
        latest_by_student[p.student_id] = p

    logger.info(f"Total candidate payments to check: {len(latest_by_student)}")

    for payment in latest_by_student.values():
        if payment.last_expiry_reminder_sent == today:
            record_skip('already_sent_today')
            skipped += 1
            continue

        days_left = (payment.expires_at.date() - today).days

        if days_left > REMINDER_DAYS_BEFORE:
            record_skip('not_in_window_yet')
            skipped += 1
            continue

        student = payment.student
        email = (student.user.email or '').strip()
        if not email:
            record_skip('no_email')
            logger.warning(f"No email for student {student.id}, payment {payment.id}")
            skipped += 1
            continue

        expired = days_left < 0
        subject = (
            f"Your {payment.plan.name} subscription has expired — access paused"
            if expired else
            f"Your {payment.plan.name} subscription expires in {days_left} day(s)"
        )

        context = {
            'student_name': student.full_name,
            'plan_name': payment.plan.name,
            'expires_on': timezone.localtime(payment.expires_at).strftime('%d %b %Y'),
            'days_left': abs(days_left),
            'expired': expired,
            'plans_url': plans_url,
        }

        try:
            html_content = render_to_string('student_management/expiry_reminder.html', context)
        except Exception:
            record_skip('template_render_failed')
            logger.exception(f"Template render failed for payment {payment.id}")
            skipped += 1
            continue

        text_content = strip_tags(html_content)

        support_email = getattr(settings, 'SUPPORT_EMAIL', None)
        headers = {}
        if support_email:
            headers = {
                'List-Unsubscribe': f'<mailto:{support_email}?subject=unsubscribe>',
                'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click',
            }

        # Retry with real backoff for account-level throttle, quick retry otherwise
        last_error = None
        success = False
        for attempt in (1, 2, 3):
            try:
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                    headers=headers,
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send(fail_silently=False)
                success = True
                break
            except Exception as e:
                last_error = e
                logger.warning(
                    f"Send attempt {attempt} failed for {email} (payment {payment.id}): {e}"
                )
                if is_throttle_error(e):
                    wait = 60 * attempt
                    logger.warning(f"Zoho throttle detected, backing off {wait}s")
                    time.sleep(wait)
                elif attempt < 3:
                    time.sleep(3)

        if success:
            payment.last_expiry_reminder_sent = today
            payment.save(update_fields=['last_expiry_reminder_sent'])
            sent += 1
        else:
            record_skip(f'send_failed:{last_error.__class__.__name__}')
            logger.exception(
                f"Failed to send expiry reminder to {email} for payment {payment.id} after retries"
            )
            skipped += 1

        time.sleep(SEND_DELAY_SECONDS)

    logger.info(f"Expiry reminder run complete: sent={sent}, skipped={skipped}, reasons={skip_reasons}")

    return {
        'sent': sent,
        'skipped': skipped,
        'skip_reasons': skip_reasons,
    }