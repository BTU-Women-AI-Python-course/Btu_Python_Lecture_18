from rest_framework import serializers

from product.models import Product, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    category_count = serializers.SerializerMethodField()
    tag_count = serializers.SerializerMethodField()

    @staticmethod
    def get_tag_count(product: Product):
        return product.tags.count()

    @staticmethod
    def get_category_count(product: Product):
        return product.categories.count()

    class Meta:
        model = Product
        fields = '__all__'


class MutateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class CreateProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)

    @staticmethod
    def validate_title(value):
        if len(value) > 9:
            raise serializers.ValidationError("Title must be less than 9 characters")
        return value

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        categories = validated_data.pop('categories')
        product = Product.objects.create(**validated_data)
        for category in categories:
            category = Category.objects.create(**category)
            product.categories.add(category)
        return product


class DynamicFieldsSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super(DynamicFieldsSerializer, self).__init__(*args, **kwargs)
        if fields:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ProductDynamicFieldsSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Product
        fields = '__all__'
