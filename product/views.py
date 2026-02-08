from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from product.models import Product, Category, Review, ProductImage
from product.serializer import ProductSerializer, CategorySerializer, ReviewSerializer, ProductImageSerializer
from django.db.models import Count
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from product.filter import ProductFilter
from rest_framework.pagination import PageNumberPagination
from product.pagination import DefaultPagination
from rest_framework.permissions import IsAdminUser, AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly
from api.permissions import IsAdminOrReadOnly, FullDjangoModelClass
from product.permissions import IsAdminOrIsAuthon
from drf_yasg.utils import swagger_auto_schema

class ProductViewSet(ModelViewSet):
    """
    - Retrive All Product
    - Create Product --> Admin Only
    - Delete Product --> admin only
    - show product list --> everyone

    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    # pagination_class = PageNumberPagination
    pagination_class = DefaultPagination
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'updated_at']
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return Product.objects.prefetch_related('images').all()

    @swagger_auto_schema( #swagger
        operation_summary='To list all product',
        operation_description='This api to list all product'
    )
    def list(self, request, *args, **kwargs):
        """Retrive all product"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(        #swagger
        operation_summary= 'To create product',
        operation_description='To Create product(Just Admin)',
        request_body= ProductSerializer,
        responses={
            201: ProductSerializer,
            400: 'Bad Request'
        }
    )
    def create(self, request, *args, **kwargs):
        """Create Product""" # this is also for swagger
        return super().create(request, *args, **kwargs)
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    # permission_classes = [FullDjangoModelClass]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     else:
    #         return [IsAdminUser()]


    """Manual Implementation"""
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     category_id = self.request.query_params.get('category_id')

    #     if category_id is not None:
    #         queryset = Product.objects.filter(category_id=category_id)
    #     return queryset

    # def destroy(self, request, *args, **kwargs):
    #     product = self.get_object()
    #     if product.stock > 10:
    #         return Response({'Message': 'You cant delete this product because stock is more then 10..!!!'})
    #     else:
    #         self.perform_destroy(product)
    #         return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        product_count = Count('products')
    ).all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]



class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrIsAuthon]

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs.get('product_pk'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {
            'product_id': self.kwargs.get('product_pk'),
        }

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_pk')
        product = Product.objects.get(pk=product_id)
        serializer.save(product=product)

""" This are store for using next time as a documentation

@api_view(['GET', 'POST'])
def view_products(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many=True, context={'request':request})
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)  # Deserializer
        # if serializer.is_valid():
        #     print(serializer.validated_data)
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
        #     return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

        # ====== Another Way =======
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ViewProducts(APIView):
    def get(self, request):
        products = Product.objects.select_related('category').all()
        serializer = ProductSerializer(products, many=True, context={'request':request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)  # Deserializer
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    # def get_queryset(self):
    #     return Product.objects.select_related('category').all()
    # def get_serializer_class(self):
    #     return ProductSerializer
    # def get_serializer_context(self):
    #     return {'request':self.request}


class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'

    # Overriding Delete Method

    # def delete(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     if product.stock > 10:
    #         return Response({'messase':'You Cannot Delete with more then 10 stock product'})
    #     else:
    #         product.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'PUT', 'DELETE'])
def view_specific_product(request, id):
    # try:
        # product = Product.objects.all().first()
        # product = Product.objects.get(pk=id)
    if request.method == 'GET':
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, context={'request':request})
        return Response(serializer.data)
    if request.method == 'PUT':
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == 'DELETE':
        product = get_object_or_404(Product, pk=id)
        copy_of_product = product
        product.delete()
        serializer = ProductSerializer(copy_of_product)
        return Response(serializer.data , status=status.HTTP_204_NO_CONTENT)
    # except Product.DoesNotExist:
    #     return Response({'messages': 'Product Does Not Exists'}, status=404)


class ViewSpecificProduct(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        copy_of_product = product
        serializer = ProductSerializer(copy_of_product)
        product.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def categories(request):
    if request.method == 'GET':
        category = Category.objects.annotate(product_count = Count('products')).all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewCategories(APIView):
    def get(self, request):
        category = Category.objects.annotate(product_count = Count('products')).all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CategoryList(ListCreateAPIView):
    queryset = Category.objects.annotate(
        product_count = Count('products')
    ).all()
    serializer_class = CategorySerializer

@api_view()
def view_specific_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

class ViewSpecificCategory(APIView):
    def get(self, request, pk):
        category = get_object_or_404(
            Category.objects.annotate(
                product_count=Count('products')
                ).all(), pk=pk
            )
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    def put(self, request, pk):
        category = get_object_or_404(
            Category.objects.annotate(
                product_count=Count('products')
                ).all(), pk=pk
            )
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self, request, pk):
        category = get_object_or_404(
            Category.objects.annotate(
                product_count=Count('products')
                ).all(), pk=pk
            )
        copy_of_category = category
        serializer = CategorySerializer(copy_of_category)
        category.delete()
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

class CategoryDetails(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.annotate(product_count = Count('products')).all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'

"""