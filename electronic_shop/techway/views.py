from django.shortcuts import render
from techway.moduls.api_yandex_disk import *
from django.http import HttpRequest, HttpResponse

def main_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки главной страницы.
    '''
    # lst = get_all_items('ARDOR_GAMING_RAGE_H335').json()['_embedded']['items']
    # return render(request, 'techway\\main_window.html', context={
    #     'test1' :  lst[0]['sizes'][0]['url'], 
    #     'test2' :  lst[1]['sizes'][0]['url'], 
    #     'test3' :  lst[2]['sizes'][0]['url'], 
    #     'test4' :  lst[3]['sizes'][0]['url'], 
    #     })
    if request.method == 'GET':
        return render(request, 'techway\\main_window.html')

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

def authorization_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с авторизацией.
    '''
    if request.method == 'GET':
        return render(request, 'techway\\authorization.html')

def registration_window(request: HttpRequest) -> HttpResponse:
    '''
    Представление для обработки страницы с регистрацией.
    '''
    if request.method == 'GET':
        return render(request, 'techway\\registration.html')
    
def product_window(request: HttpRequest, product_id: int) -> HttpResponse:
    '''
    Представление для обработки страницы с регистрацией.
    '''
    if request.method == 'GET':
        return render(request, 'techway\\item_page.html')