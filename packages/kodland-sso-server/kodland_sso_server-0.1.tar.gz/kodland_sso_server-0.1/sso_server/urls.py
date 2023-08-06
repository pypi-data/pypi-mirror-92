from django.urls import path
from .views import TokenView, UserDataView

urlpatterns = [
	path('token', TokenView.as_view(), name='token'),
	path('info', UserDataView.as_view(), name='user_info')
]
