from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response

from sso_server.services.token_service import TokenService


# Create your views here.
class UserDataView(APIView):
	"""
	получение данных пользователя по токену
	"""
	
	def get(self, request):
		"""
		accept access_token in POST request and return user's data in json format
		"""
		result = TokenService.get_user_info_by_token(request.META.get('HTTP_AUTHORIZATION'))
		return Response(result, status=HTTP_200_OK)
	

class TokenView(APIView):
	"""
	return access token to user if everything is ok
	"""
	
	def post(self, request):
		"""
		В теле запроса необходимо передать дополнительные параметры:

		grant_type=authorization_code/refresh_token

		В ответе вернётся JSON:
		{
		    "access_token": "{access_token}",
		    "token_type": "bearer",
		    "refresh_token": "{refresh_token}"
		}
		"""
		token = TokenService(request)
		
		result = token.token()
		
		if isinstance(result, dict):
			return Response(result, status=HTTP_200_OK)
		else:
			return Response({'error': 'Invalid params'}, status=HTTP_400_BAD_REQUEST)
