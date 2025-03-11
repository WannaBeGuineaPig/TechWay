from django.shortcuts import render
from techway.moduls.api_yandex_disk import *

def main_window(request):
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
    return render(request, 'techway\\main_window.html')

def catalog_window(request):
    '''
    Представление для обработки страницы с каталогом.
    '''
    return render(request, 'techway\\catalog.html')

def favorite_window(request):
    '''
    Представление для обработки страницы с избранным.
    '''
    return render(request, 'techway\\favorite.html')

def backet_window(request):
    '''
    Представление для обработки страницы с корзиной.
    '''
    return render(request, 'techway\\backet.html')

def personal_account_window(request):
    '''
    Представление для обработки страницы с личным кабинетом.
    '''
    return render(request, 'techway\\personal_account.html')