import json
import six
from rest_framework import serializers
from taggit_serializer.serializers import TaggitSerializer, TagListSerializerField

from courses.models import Course


class NewTagListSerializerField(TagListSerializerField):
    def to_internal_value(self, value):
        if isinstance(value, six.string_types):
            if not value:
                value = "[]"
            try:
                if (type(value) == str):
                    if (value.__contains__('"') == True):
                        value = json.loads(value)
                    else:
                        value = value.split(',')

            except ValueError:
                self.fail('invalid_json')

        if not isinstance(value, list):
            self.fail('not_a_list', input_type=type(value).__name__)

        for s in value:
            if not isinstance(s, six.string_types):
                self.fail('not_a_str')

            self.child.run_validation(s)

        return value


class CourseSerializer(TaggitSerializer, serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(read_only=True)
    category = serializers.SerializerMethodField()
    secondary = serializers.SerializerMethodField()
    lectures = serializers.SerializerMethodField()
    tags = NewTagListSerializerField()

    class Meta:
        model = Course
        fields = [
            'title',
            'slug',
            'image',
            'image_height',
            'image_width',
            'category',
            'secondary',
            'order',
            'description',
            'price',
            'lectures',
            'active',
            'updated',
            'timestamp',
            'tags',
        ]

    def get_category(self, obj: Course):
        return obj.category.title

    def get_secondary(self, obj: Course):
        return obj.category.title

    def get_lectures(self, obj: Course):
        return obj.lecture_set.all().values()

    def create(self, validated_data):
        print(validated_data)
        tags = validated_data.pop('tags')
        print(tags)
        instance: Course = super(CourseSerializer, self).create(validated_data)
        instance.tags.add(*tags)
        # instance.tags.set(*tags)
        return instance
