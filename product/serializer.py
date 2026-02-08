from rest_framework import serializers
from decimal import Decimal
from product.models import Category, Product, Review, ProductImage
from users.models import User
from django.contrib.auth import get_user_model

# class CategorySerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     description = serializers.CharField()

# class ProductSerilizer(serializers.Serializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='price')
#     price_with_tax = serializers.SerializerMethodField('calculate_tax')
#     # category = serializers.PrimaryKeyRelatedField(  # toget just id or pk
#     #     queryset = Category.objects.all()
#     # )
#     # category = serializers.StringRelatedField()  #to get __str__ value
#     # category = CategorySerializer() # to get all info of category
#     category = serializers.HyperlinkedRelatedField(
#         queryset = Category.objects.all(),
#         view_name='view_specific_category'
#         )
#     def calculate_tax(self, product):
#         return round(product.price * Decimal(1.1), 2)


# use model serializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'product_count']

    product_count = serializers.IntegerField(read_only=True, help_text='Count of all products in specific category')  # "help_text" is for swagger

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id','name', 'description', 'price', 'stock', 'category','price_with_tax', 'images']

    price_with_tax = serializers.SerializerMethodField('calculate_tax')
    # category = serializers.HyperlinkedRelatedField(
    #     queryset = Category.objects.all(),
    #     view_name = 'view_specific_category'
    # )

    def calculate_tax(self, product):
        return round(product.price * Decimal(1.1), 2)

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Price Could not be negetive')
        else:
            return price


     # ==== To Override Create Method Before Save ======
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='full_name')
    class Meta:
        model = get_user_model()
        fields = ['id', 'name']

    def full_name(self, obj:User):
        return obj.get_full_name()

class ReviewSerializer(serializers.ModelSerializer):
    # first_name = User.objects.get
    user = serializers.SerializerMethodField(method_name='get_user')
    class Meta:
        model = Review
        fields=['id', 'user', 'product', 'comment', 'ratings']
        read_only_fields = ['user', 'product']

    def get_user(self, obj):
        return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


