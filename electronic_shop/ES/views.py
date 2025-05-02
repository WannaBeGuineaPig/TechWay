from django.shortcuts import render

def main_window(request):
    return render(request, 'ES\\main_window.html')

def catalog_window(request):
    return render(request, 'ES\\catalog.html')

def favorite_window(request):
    return render(request, 'ES\\favorite.html')

def backet_window(request):
    return render(request, 'ES\\backet.html')

def personal_account_window(request):
    return render(request, 'ES\\personal_account.html')