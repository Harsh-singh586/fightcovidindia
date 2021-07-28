from rest_framework import serializers

class Geeks(object):
    def __init__(self, json_data):
        self.json_data = json_data

class GeeksSerializer(serializers.Serializer):
	hospitals = serializers.JSONField()
