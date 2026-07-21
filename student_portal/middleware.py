from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from .models import UserSession

class SingleSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'student'):
            try:
                db_session = UserSession.objects.get(user=request.user)
                if request.session.get('session_key') != db_session.session_key:
                    logout(request)
                    request.session.flush()
                    # Avoid redirect loop if already heading to login
                    if request.path != reverse('student_portal:login'):
                        return redirect('student_portal:login')
            except UserSession.DoesNotExist:
                pass
        return self.get_response(request)