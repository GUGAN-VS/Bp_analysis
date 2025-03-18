from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from api.models import BPRecord

class HospitalAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username and password:
            # Check if the username is a valid hospital name
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)

                # Admin login logic
                if user.check_password(password) and user.is_superuser:
                    return user

                # Caretaker login logic
                if BPRecord.objects.filter(patient_id=password).exists():
                    return user

            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
