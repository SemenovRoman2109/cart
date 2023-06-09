from django.shortcuts import render
from django.http import JsonResponse
from cartapp.models import *
# Create your views here.
def show_products(request):
    response = render(request,"products.html",context={"products": Product.objects.all()})
    if request.method == "POST":
        if "product_pk" not in request.COOKIES: # Якщо у користувача в куках немае product_pk (вiн не додав жоден товар у корзину)
            new_product = request.POST.get('product_pk') # Отрымуемо pk(номер) обраного товару
            response.set_cookie('product_pk',new_product) # Додаемо до кукiв нове значення 
        else: # Якщо у користувача в куках е product_pk (У нього вже були даннi у product_pk)
            new_product = request.COOKIES['product_pk'] + " " + request.POST.get('product_pk') # Додаемо старi даннi до нових i по середеннi ставимо пробiл
            response.set_cookie('product_pk',new_product) # Замiнюемо старi даннi product_pk у куках на новi

    return response

def show_cart(request):
    if "product_pk" in request.COOKIES: #Якщо у користувача е куки product_pk
        
        products_pk = request.COOKIES['product_pk'].split(" ") #Зi строки з pk(номером) замовлення робемо список роздiлюючи ix по пробiлам

        list_products = list() # Cтворюемо список продуктiв pk яких е у списку pk
        for product_pk in products_pk: #Перебираемо список pk
            list_products.append(Product.objects.get(pk=product_pk)) # Додаемо до списку обект з потрiбним pk 
        response = render(request,"cart.html",context={"products": list_products})# Формуемо html сторiнку у яку передаемо список замовленнь
    else:
        response = render(request,"cart.html",context={"products":list()})#  Формуемо html сторiнку з пустим списком замовленнь
               
    if request.method == "POST":
        if "product_pk" in request.COOKIES:
            products_pk = request.COOKIES['product_pk'].split(' ') # Додаемо старi даннi до нових i по середеннi ставимо пробiл
            pk_deleted = request.POST.get('product_pk')
                        
            if len(products_pk) > 1:
                for i in products_pk:
                    if i == str(pk_deleted):
                        products_pk.pop(products_pk.index(i))
                        break
                
                new_product = ""
                for pk in products_pk:
                    new_product = new_product + " " + pk 
                new_product = new_product[1:]
                
                list_products = list() # Cтворюемо список продуктiв pk яких е у списку pk
                for product_pk in products_pk: #Перебираемо список pk
                    list_products.append(Product.objects.get(pk=product_pk))
                    
                response = render(request,"cart.html",context={"products": list_products})
                response.set_cookie('product_pk',new_product)

            else:
                
                response = render(request,"cart.html",context={"products": list()})
                response.delete_cookie('product_pk') # Замiнюемо старi даннi product_pk у куках на новi

        
    return response # Повертаемо сторiнку кошику
