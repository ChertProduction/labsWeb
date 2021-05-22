import logging
from json import dumps, loads
from django.shortcuts import render
from django.template import RequestContext

from dbapi.serializers import ContactSerializer
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django.http import HttpRequest
import redis
from django.conf import settings
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from dbapi.models import Grammy


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
logger = logging.getLogger('django')
redis_access = redis.Redis('redis', port=6379, db=15)
redis_access.ttl(CACHE_TTL)


# получение данных из бд
def index(request):
    people = Grammy.objects.all()
    return render(request, "index.html", {"people": people})
 
class ContactView(APIView):

	def put(self, request):
		data = loads(request.body)
		serializer = ContactSerializer(data=data)
		if not serializer.is_valid():
			return Response(status=400)
		Grammy(**serializer.data).save()
		return Response(status=201)

	def delete(self, request):
		data = loads(request.body)
		orm = Grammy.objects.all()
		obj = orm.get(pk=data['id'])
		obj.delete()
		redis_access.delete(data['id'])
		return Response(status=200)

	def post(self, request):
		data = loads(request.body)
		print(data)
		serializer = ContactSerializer(data=data)
		print(serializer)
		if not serializer.is_valid():
			return Response(status=400)
		model = Grammy(**serializer.data)
		model.pk = serializer.data['id']
		model.save()
		redis_access.delete(model.pk)
		return Response(status=200)


	def get(self, request: Request):
		id = request.query_params.get('id', None)
		if id is None:
			return Response(status=400)
		else:
			logger.info(f'[Grammy] getting record with id = {id}')
			cached = redis_access.get(id)

			if cached:
				logger.info(f'[Grammy] got record with id = {id} from redis')
				cached = loads(cached)
				return Response(cached)

			logger.info(f'[Grammy] had to query record with id = {id} from db')
			orm = Grammy.objects.all()				
			obj = orm.get(pk=id)
			data = obj.__dict__

			serializer = ContactSerializer(data=data)
			if not serializer.is_valid():
				return Response(status=400)
			data = serializer.data

			redis_access.set(id, dumps(data))

			return Response(data)

routes = [
	path('api/contacts/', ContactView.as_view())
]