from django.contrib.auth.forms import UserCreationForm

from shop.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
