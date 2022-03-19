from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from auth.views import RegisterView
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('signup/', RegisterView.as_view(), name='auth_register'),
    path('signup/', csrf_exempt(RegisterView.as_view()), name='auth_register'),
]
