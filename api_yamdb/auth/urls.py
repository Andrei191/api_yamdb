from django.urls import path
from auth.views import RegisterView, CustomAuthToken
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('token/', CustomAuthToken.as_view(), name='token_obtain_pair'),
    path('signup/', csrf_exempt(RegisterView.as_view()), name='auth_register'),
]