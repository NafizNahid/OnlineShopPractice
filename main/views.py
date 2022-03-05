from django.shortcuts import render
from django.http import HttpResponse
from .models import MainCarousel, OfferCarousel, Categories, Captions, Product , Contact, Cont_info, Dynamic_Product, Order, OrderUpdate
import json
from math import ceil

def index(request) : 
    main_images_collection = MainCarousel.objects.values('image')
    main_images = {item['image'] for item in main_images_collection}
    offer_images_collection = OfferCarousel.objects.values('image')
    offer_images = {item['image'] for item in offer_images_collection}
    category_images_collection = Categories.objects.values('image')
    category_images = {item['image'] for item in category_images_collection}
    # Try doing the same with the above cases 
    categories_collection = Categories.objects.all()
    categories = {item for item in categories_collection}

    dynamicProds = []
    productCaptions = Dynamic_Product.objects.values('caption', 'id')
    captions_collection = Captions.objects.all()
    captions = {item for item in captions_collection}
    # captions = {item['caption'] for item in productCaptions}  # useful!
    # for caption in captions :
    #     prods = Dynamic_Product.objects.filter(caption=caption)
    #     dynamicProds.append(prods)
    
    for caption in captions :
        prods = [Dynamic_Product.objects.filter(caption=caption), caption]
        dynamicProds.append(prods)

    print(dynamicProds)

    params = {
        'main_images' : main_images, 
        'offer_images' : offer_images, 
        'category_images': category_images, 
        'categories' : categories, 
        'captions' : captions,
        'dynamicProds' : dynamicProds
    }

    return render(request, 'main/index.html', params)


def about(request) :
    return HttpResponse("About us")


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates":updates, "itemsJson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'main/tracker.html')


def search(request) :
    return HttpResponse("search")


def contact(request):
    
    thank=False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank=True
    
    emails_collection = Cont_info.objects.values('email')
    emails = {item['email'] for item in emails_collection}
    
    phones_collection = Cont_info.objects.values('phone')
    phones = {item['phone'] for item in phones_collection}
    
    addresses_collection = Cont_info.objects.values('address')
    addresses = {item['address'] for item in addresses_collection}
    
    pages_collection = Cont_info.objects.values('page')
    pages = {item['page'] for item in pages_collection}
    
    return render(request, 'main/contact.html', {'thank':thank, 'emails':emails, 'phones':phones, 'pages': pages,'addresses':addresses})


def checkout(request) :
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')  
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, amount=amount, email=email, address=address, city=city, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        print(items_json)
        return render(request, 'main/checkout.html', {'thank':thank, 'id': id})
    return render(request, 'main/checkout.html')


def category_view(request, id) :
    category = Categories.objects.filter(id=id)[0]
    products = Product.objects.filter(category=category) 
    params = {'category' : category, 'products' : products}
    return render(request, 'main/category_view.html', params)


def caption_view(request, id) :
    caption = Captions.objects.filter(id=id)[0]
    products = Dynamic_Product.objects.filter(caption=caption)
    params = {'caption' : caption, 'products' : products}
    return render(request, 'main/caption_view.html', params)


def product_view(request, id) :
    product = Product.objects.filter(id=id)[0]
    return render(request, 'main/product_view.html', {'product' : product})

# tried with code instead of id
# def product_view(request, code) :
#     product = Product.objects.filter(code=code)[0]
#     return render(request, 'main/product_view.html', {'product' : product})


def dynamic_product_view(request, id) :
    product = Dynamic_Product.objects.filter(id=id)[0]
    return render(request, 'main/product_view.html', {'product' : product})