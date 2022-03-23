from django.urls import path
from auth.views import RegisterView, CustomAuthToken


urlpatterns = [
    path('token/', CustomAuthToken.as_view(), name='token_obtain_pair'),
    path('signup/', RegisterView.as_view(), name='auth_register'),
]
