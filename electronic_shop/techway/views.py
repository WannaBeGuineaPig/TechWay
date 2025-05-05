from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse, JsonResponse
import requests
from python_moduls.add_product_data import *

URL_API = 'http://127.0.0.1:8000/api/'

def update_product_list(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        response_product_list = requests.get(URL_API + f'product_list/?sort={request.GET["sort"]}')
        product_list = calculate_feedback_and_set_image(response_product_list.json(), 'rating_sum', 'rating_count')

        render_page = render(request, 'techway\\product_previews_list.html', context={'product_list' : product_list})
        return JsonResponse({
            'result' : True,
            'product_list_page' : render_page.content.decode("utf-8")
        })
    
def main_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки главной страницы.
    '''
    if request.method == 'GET':
        response_product_list = requests.get(URL_API + 'product_list/')
        product_list = response_product_list.json()
        product_list = calculate_feedback_and_set_image(response_product_list.json(), 'rating_sum', 'rating_count')

        return render(request, 'techway\\main_window.html', context={'product_list' : product_list})

def catalog_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с каталогом.
    '''
    if request.method == 'GET':
        return render(request, 'techway\\catalog.html')

def favorite_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с избранным.
    '''
    if request.method == 'GET':
        return render(request, 'techway\\favorite.html')

def backet_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с корзиной.
    '''
    if request.method == 'GET':
        return render(request, 'techway\\backet.html')

def personal_account_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с личным кабинетом.
    '''
    if request.method == 'GET':
        return render(request, 'techway\\personal_account.html')
    
    else:
        if 'btn' in request.POST and request.POST['btn'] == 'Выйти из аккаунта':
            request.session.pop('id_user')
            return redirect('TechWay:home')
        
        elif 'btn' in request.POST and request.POST['btn'] == 'Удалить аккаунт':
            return redirect('TechWay:home')

        elif 'btn' in request.POST and request.POST['btn'] == 'История':
            return redirect('TechWay:home')

def authorization_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с авторизацией.
    '''
    if request.method == 'GET':
        return render(request, 'techway\\authorization.html')
    
    else:
        request.session['id_user'] = request.POST['id_user']
        return JsonResponse({"redirect_url": "personal_account"})

def registration_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с регистрацией.
    '''
    if request.method == 'GET':
        return render(request, 'techway\\registration.html')
    
    else:
        pass
    
def product_window(request: HttpRequest, product_id: int) -> HttpResponse:
    '''
    Представление для обработки страницы с регистрацией.
    '''
    if request.method == 'GET':
        return render(request, 'techway\\item_page.html')