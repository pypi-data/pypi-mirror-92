from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
import jwt
from .backends import TokenAuth
from sso_client.services.get_token_by_refresh import GetTokenByRefresh


class CheckTokenMiddleware(MiddlewareMixin):
	"""
	обновление пары access/refresh токенов, если срок действия токена истек
	"""
	def process_response(self, request, response):
		if request.COOKIES.get('access', False):
			token = jwt.decode(request.COOKIES.get('access'), 'access_secret', algorithms=['HS256'])

			# если access token протух
			if token.get('exp') - int(datetime.now().strftime('%Y%m%d')) <= 0:
				if request.COOKIES.get('refresh', False):
					token = GetTokenByRefresh.get_token(request.COOKIES.get('refresh'))
					response.set_cookie('access', token.get('access_token'))
					response.set_cookie('refresh', token.get('refresh_token'))

		return response


class AuthMiddleware(MiddlewareMixin):
	"""
	авторизация по токену
	"""
	def process_request(self, request) -> None:
		if request.COOKIES.get('access', False):
			user = TokenAuth.authenticate(request=request)
			if user:
				request.user = request._cached_user = user
