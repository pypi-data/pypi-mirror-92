from rest_framework import serializers


class SerializerFunctionField(serializers.Field):
    """A read-only field that get its representation from calling a function passed to
    initialization attributes. The function should take two arguments. The first one
    is the object being serializer, the second one is serializer context.

    This field is useful when you need to use same calculations
    in multiple serializers.

    For example:

        def func(obj, context=None):
                return ...  # Return the data

        class ExampleSerializer(self):
            extra_info = SerializerFunctionField(function=func)
    """
    def __init__(self, function=None, **kwargs):
        self.function = function
        kwargs['source'] = '*'
        kwargs['read_only'] = True
        super().__init__(**kwargs)

    def bind(self, field_name, parent):
        if self.function is None:
            raise AttributeError("Attribute `function` cannot be None.")
        super().bind(field_name, parent)

    def to_representation(self, value):
        return self.function(value, context=self.context)
