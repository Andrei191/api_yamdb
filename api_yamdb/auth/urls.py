from django.urls import path
from auth.views import registration, CustomAuthToken


urlpatterns = [
    path('token/', CustomAuthToken.as_view(), name='token_obtain_pair'),
    path('signup/', registration),
]
