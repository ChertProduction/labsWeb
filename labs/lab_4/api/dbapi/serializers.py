from rest_framework import serializers
from dbapi.models import Grammy

class ContactSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	class Meta:
		model = Grammy
		fields =['id', 'name', 'surname']