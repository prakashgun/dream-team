from rest_framework import serializers


class CrawlInfoSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    urls = serializers.ListField(max_length=255, required=True)


class PredictSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    urls = serializers.ListField(max_length=255, required=True)
    ground = serializers.CharField(max_length=100, required=True)
    opposite_team = serializers.CharField(max_length=100, required=True)
