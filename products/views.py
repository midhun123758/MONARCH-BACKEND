from django.shortcuts import render
from rest_framework.views  import APIView
from rest_framework.response import Response
from .models import Product,Category
from .serializers import ProductSerializer
from rest_framework.permissions  import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q

class ProductListViewI(APIView):
    def get(self,request):
        products=Product.objects.all()
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)

class ProductDetailView(APIView):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
class Categerory_view(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, pk):
          try:
            catogory=Category.objects.get(id=pk)
          except Category.DoesNotExist:
            return Response({"error":'category doest not excit'})
          products=Product.objects.filter(category=catogory)
          serializer=ProductSerializer(products,many=True)
          return Response({
              "category": catogory.name,
              "products": serializer.data
          })

from rest_framework.decorators import api_view

@api_view(['POST'])
def product_create(request):
    if isinstance(request.data, list):
        serializer = ProductSerializer(data=request.data, many=True)
    else:
        serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class ProductFilterView(APIView):
    def get(self, request):
        try:
            products = Product.objects.filter(is_deleted=False)

            search = request.query_params.get("search")
            if search:
                products = products.filter(
                    Q(name__icontains=search) | Q(description__icontains=search)
                )

        
            category = request.query_params.get("category")
            if category:
                products = products.filter(category_id=category)

       
            min_price = request.query_params.get("min_price")
            max_price = request.query_params.get("max_price")
            if min_price:
                products = products.filter(price__gte=min_price)
            if max_price:
                products = products.filter(price__lte=max_price)

       
            sort = request.query_params.get("sort")
            if sort == "asc":
                products = products.order_by("price")
            elif sort == "desc":
                products = products.order_by("-price")
            elif sort == "demand":
                products = products.order_by("-stock")

   
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError as ve:
            
            return Response(
                {"error": f"Invalid parameter: {ve}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Something went wrong: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
