from rest_framework import serializers


class CrawlInfoSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    url = serializers.CharField(max_length=255, required=True)

