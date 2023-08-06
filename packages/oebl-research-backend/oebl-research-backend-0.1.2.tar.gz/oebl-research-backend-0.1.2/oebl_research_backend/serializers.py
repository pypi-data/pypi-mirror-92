from rest_framework import serializers

from .models import ListEntry


class ListEntrySerializer(serializers.ModelSerializer):
    gnd = serializers.SerializerMethodField(method_name="get_gnd")
    firstName = serializers.CharField(source="person.first_name")
    lastName = serializers.CharField(source="person.name")
    list = serializers.SerializerMethodField(method_name="get_list")

    def get_list(self, object):
        res = {"id": object.list_id, "title": object.list.title}
        return res

    def get_gnd(self, object):
        if object.person.uris is not None:
            for uri in object.person.uris:
                if "d-nb.info" in uri:
                    return uri
        return "not specified"

    class Meta:
        model = ListEntry
        fields = [
            "id",
            "gnd",
            "list",
            "firstName",
            "lastName",
            "columns_user",
            "columns_scrape",
        ]
