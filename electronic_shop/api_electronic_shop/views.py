from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from python_moduls.modul_password import * 
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.db.models import F

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProductList(APIView):
    def get(self, request):
        product_list = Product.objects.all()
        
        if 'sort' not in request.GET:
            return Response(ProductSerializer(product_list, many=True).data)
        
        match(request.GET['sort']):
            case 'popular_first':
                pass

            case 'low_cost_first':
                product_list = product_list.order_by('price')

            case 'expensive_first':
                product_list = product_list.order_by('-price')

            case 'number_of_feedback':
                product_list = product_list.order_by('-rating_count')

            case 'best_feedback':
                product_list = product_list.annotate(feedback=F('rating_sum') / F('rating_count')).order_by('-feedback')

        return Response(ProductSerializer(product_list, many=True).data)

class AuthorizationRegistrationUser(APIView):
    def get(self, request, pk = None):
        if pk:
            user = get_object_or_404(User, iduser=pk)
            return Response(model_to_dict(user))

        user = get_object_or_404(User, mail=request.GET['mail'], password=hash_password(request.GET['password']))
        # user = get_object_or_404(User, mail=request.GET['mail'], password=request.GET['password'])
        return Response(model_to_dict(user))
    
    def post(self, request):
        serializer = UserSerializer(data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save(status='Активен', position='Клиент', password=hash_password(request.POST['password']))
            return Response(serializer.validated_data)

        return Response(serializer.errors, status=status.HTTP_409_CONFLICT)



# class AuthRegUpdateUser(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class UserList(generics.ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = ManufacturerSerializer

# class ProductList(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
# class SubcategoryList(generics.ListAPIView):
#     queryset = Subcategory.objects.all()
#     serializer_class = SubcategorySerializer


# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer