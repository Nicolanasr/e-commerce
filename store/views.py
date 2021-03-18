from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from rest_framework import serializers
from .models import Product, Category, Customer, ShippingAddress, Order, OrderItem, Coupon, User, Rating
from django.contrib.auth.models import Group
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect, response
from django.core.paginator import Paginator
from django.contrib import messages
from random import *
from .forms import CreateShippingAddress, NewProduct
from django.utils.safestring import mark_safe
import time, re
import uuid
import datetime
from datetime import timedelta
from .serializers import ProductSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
# Create your views here.

#// TODO user generated reviews
# TODO wishlist
# TODO realted items
# TODO Special offers
#* -------------------
# TODO and add them in the filter option

def index(request):
    cat = request.GET.get('cat')
    categor = None
    product_search = None

    Product.objects.select_for_update().filter(in_stock=True, qty = 0).update(in_stock=False)

    products = Product.objects.all()

    if(request.GET.get('price') == 'lowest'):
        products = Product.objects.order_by('price')

    elif(request.GET.get('price') == 'highest'):
        products = Product.objects.order_by('-price')

    if(request.GET.get('clear') != None):
        return redirect('store:index')

    if(request.GET.get('product_search')):
        if(len(request.GET.get('product_search')) != 0):
            product_search = request.GET.get('product_search')
            product = Product.objects.filter(title__contains=product_search)
            products = product

    # TODO adding pagination to products
    # paginator = Paginator(products, 2)

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    try:
        categor = Category.objects.get(id=cat)
    except:
        pass

    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, user=request.user)
    else:
        uid = request.COOKIES.get('device')
        print('i', uid)
        try:
            customer = Customer.objects.get(uid=uid)
            print(customer)
        except:
            customer = Customer(uid=uid)
            if str(customer) == 'None':
                pass
            else:
                customer.save()

    orderItems = None

    try:
        order = Order.objects.get(customer=customer, complete=False)
        orderItems = OrderItem.objects.filter(order=order)
    except:
        pass

    categories = Category.objects.all()
    if len(products) == 0:
        messages.warning(
            request, 'No products found! Clear your filters and try again')

    ctx = {'orderItems': orderItems, 'products': products, 'categories': categories,
           'cat': cat, 'categor': categor, 'ps': product_search}
    return render(request, 'store/store.html', ctx)


def cart(request):
    data = {}
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, user=request.user)
    else:
        uid = request.COOKIES.get('device')
        try:
            customer = Customer.objects.get(uid=uid)
        except:
            customer = Customer(uid=uid)
            if str(customer) == 'None':
                messages.warning(request, 'We use cookies in order to let you order items without an account so please enable cookies(and javascript) or login with your account in order to continue!')
                return redirect('store:index')
            else:
                customer.save()

    orderItems = None

    try:
        orderComplete = Order.objects.filter(customer=customer, complete=True)
        orderItemsComplete = OrderItem.objects.filter(order=orderComplete)
    except:
        orderComplete = None
        orderItemsComplete = None

    try:
        order = Order.objects.get(customer=customer, complete=False)
        orderItems = OrderItem.objects.filter(order=order)

        total = 0
        for item in orderItems:
            total = total + (item.product.price*item.quantity)

        tot = total + round(total/100*10)
        Order.objects.select_for_update().filter(id=order.id).update(total=tot)
    except:
        total = 0
        tot = 0

    # for oi in orderItems:
    #     print(oi.product.qty)

    if request.is_ajax():
        item = request.POST.get('item')
        add = request.POST.get('add')
        data['item'] = item
        data['add'] = add

        item_add = get_object_or_404(OrderItem, id=item)
        qty = item_add.quantity
        qty = qty+int(add)
        OrderItem.objects.select_for_update().filter(id=item).update(quantity=qty)
        if qty == 0:
            item_add.delete()
        order = Order.objects.get(customer=customer, complete=False)
        orderItems = OrderItem.objects.filter(order=order)
        total = 0
        for item in orderItems:
            total = total + (item.product.price*item.quantity)

        tot = total + round(total/100*10)

        Order.objects.select_for_update().filter(id=order.id).update(total=tot)
        order = Order.objects.get(customer=customer, complete=False)

        return JsonResponse(data)

    ctx = {'orderItems': orderItems, 'total': total, 'tot': tot,
           'orderComplete': orderComplete, 'orderItemsComplete': orderItemsComplete}
    return render(request, 'store/cart.html', ctx)


def addtocart(request, item):

    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, user=request.user)
        # product = get_object_or_404(Product, title=item)
        # order = Order.objects.filter(customer=customer, complete=False)
    else:
        uid = request.COOKIES.get('device')
        try:
            customer = Customer.objects.get(uid=uid)
        except:
            customer = Customer(uid=uid)
            if str(customer) == 'None':
                messages.warning(request, 'We use cookies in order to let you order items without an account so please enable cookies(and javascript) or login with your account in order to continue!')
                return redirect('store:index')
            else:
                customer.save()
        

    product = get_object_or_404(Product, title=item)
    order = Order.objects.filter(customer=customer, complete=False)

    if not order:
        order = Order(customer=customer)
        order.save()

    order = Order.objects.get(customer=customer, complete=False)

    try:
        orderItem = OrderItem.objects.get(product=product, order=order)
        qty = orderItem.quantity
        print(qty)
        print('---', orderItem.product.qty)
        if(int(qty) < int(orderItem.product.qty)):
            OrderItem.objects.select_for_update().filter(
                product=product, order=order).update(quantity=qty+1)
        else:
            messages.warning(request, "You can't add anymore of this Item")
            return redirect('store:index')
    except:
        item = OrderItem(product=product, order=order, quantity=1)
        item.save()

    return redirect('store:cart')


def ordercancel(request, orderid):
    order = Order.objects.get(id=orderid)
    orderItems = OrderItem.objects.filter(order=order)
    for items in orderItems:
        if items.product.qty == 0:
            Product.objects.select_for_update().filter(id=items.product.id).update(in_stock=True, qty=items.quantity)
        else:
            p = Product.objects.get(id=items.product.id)
            q = p.qty + items.quantity
            # print(q)
            Product.objects.select_for_update().filter(id=items.product.id).update(qty=q)

    if request.method == 'POST':
        try:
            if not Order.objects.filter(id=orderid):
                raise Http404('404')
            else:
                Order.objects.filter(id=orderid).delete()
                messages.warning(request, 'Your order was canceled!')
        except:
            raise Http404('404')
       
    return redirect('store:cart')


def checkout(request):
    form = CreateShippingAddress()

    errors = ''
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, user=request.user)
    else:
        uid = request.COOKIES.get('device')
        customer = Customer.objects.get(uid=uid)

    try:
        order = Order.objects.get(customer=customer, complete=False)
        if len(order.orderitem_set.all()) == 0:
            messages.error(request, 'Add Items to your cart first')
            return redirect('store:index')
    except:
        messages.error(request, 'Add Items to your cart first')
        return redirect('store:index')

    
        # print('--', items.quantity)
        # print(items.product.qty)
            
    if request.method == 'POST':
        form = CreateShippingAddress(request.POST)
        if form.is_valid():
            address1 = request.POST.get('address')
            address2 = request.POST.get('address2')
            state = request.POST.get('state')
            city = request.POST.get('city')
            address = ShippingAddress.objects.filter(
                address=address1, address2=address2, city=city, state=state)
            if len(address) > 0:
                address = address[0]
            else:
                form.save()
                address = ShippingAddress.objects.get(address=address1, address2=address2, city=city, state=state)

            transaction_id = int(
                round(datetime.datetime.timestamp(datetime.datetime.now()), 0))
            some_date = datetime.date.today()
            three_months = datetime.timedelta(2*365/12)
            eta = some_date + three_months
            
            order = Order.objects.get(customer=customer, complete=False)
            Order.objects.select_for_update().filter(customer=customer, complete=False).update(
                address=address, complete=True, transaction_id=transaction_id, deliveryDate=eta)

            
            orderItems = OrderItem.objects.filter(order=order)
            for items in orderItems:
                if items.quantity == items.product.qty:
                    p = Product.objects.get(id=items.product.id)
                    print(p.qty)
                    q = items.product.qty - items.quantity
                    print(q)
                    Product.objects.select_for_update().filter(id=items.product.id).update(in_stock=False, qty=q)
                else:
                    q = items.product.qty - items.quantity
                    Product.objects.select_for_update().filter(id=items.product.id).update(qty=q)

            try:
                name = request.POST.get('name')
                email = request.POST.get('email')
                uid = request.COOKIES.get('device')
                Customer.objects.select_for_update().filter(
                    uid=uid).update(email=email, name=name)

            except:
                pass

            order = Order.objects.get(id=order.id)
            return redirect('store:trackorder', order.transaction_id)
        else:
            errors = form.errors.values
            errors = list(errors)

    order_coupon = None
    orderItems = None
    try:
        order = Order.objects.get(customer=customer, complete=False)
        orderItems = OrderItem.objects.filter(order=order)
        order_id = order.id

        total = 0
        tot = order.totalAfterCoupon
        if order.coupon == None:
            tot = order.total
        elif order.coupon != None and order.coupon_activated == False:
            tot = order.total - order.coupon.value
            order_coupon = order.coupon
            old_coupon = order_coupon
            Order.objects.select_for_update().filter(
                id=order_id).update(coupon_activated=True)
            Order.objects.select_for_update().filter(
                id=order_id).update(totalAfterCoupon=tot)
            order = Order.objects.get(customer=customer, complete=False)
            tot = order.totalAfterCoupon
        elif order.coupon_activated == True:
            order_coupon = order.coupon
        Order.objects.select_for_update().filter(
            id=order_id).update(totalAfterCoupon=tot)

    except:
        total = 0
        tot = 0

    ctx = {'orderItems': orderItems, 'total': total, 'tot': tot,
           'form': form, 'errors': errors, 'coupon': order_coupon, 'order': order}
    return render(request, 'store/checkout.html', ctx)


def apply_coupon(request):
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, user=request.user)
    else:
        uid = request.COOKIES.get('device')
        customer = Customer.objects.get(uid=uid)
    if request.POST.get('coupon') != None:
        coupon_name = request.POST.get('coupon')
        order = Order.objects.get(customer=customer, complete=False)
        try:
            if order.coupon == None:
                coupon = Coupon.objects.get(coupon=coupon_name)
                if order.total > coupon.value:
                    new_total = order.total - coupon.value
                    od = Order.objects.select_for_update().filter(id=order.id).update(coupon=coupon)
                else:
                    print('you need to have an order of: $ ',
                          coupon.value, ' to be able to use this coupon')
                    messages.warning(request, 'you need to have an order of: + $ ' +
                                     str(coupon.value) + ' to be able to use this coupon')
            else:
                print('You are already using a coupon')
                messages.warning(request, 'You are already using a coupon')
        except:
            print('coupon not avaible')
            cc = Coupon.objects.filter(coupon__contains=coupon_name)
            if cc:
                messages.warning(request, 'Coupons are case sensitive')
            else:
                messages.warning(request, 'coupon not avaible')

        return redirect('store:checkout')
    return redirect('store:checkout')


def remove_coupon(request):
    if request.user.is_authenticated:
        customer = get_object_or_404(Customer, user=request.user)
    else:
        uid = request.COOKIES.get('device')
        customer = Customer.objects.get(uid=uid)

    order = Order.objects.get(customer=customer, complete=False)
    print(order.coupon)
    print(order.coupon_activated)
    total = order.totalAfterCoupon + order.coupon.value
    Order.objects.select_for_update().filter(id=order.id).update(
        coupon=None, coupon_activated=False, total=total)
    Order.objects.select_for_update().filter(
        id=order.id).update(totalAfterCoupon=None)
    return redirect('store:checkout')


def track_order(request):
    return render(request, 'store/trackorder.html')


def trackorderred(request):
    order = None
    if request.method == 'POST':
        order_track = request.POST.get('order_track')
        return redirect('store:trackorder', order_track)


def trackorder(request, order_track):
    try:
        order = Order.objects.get(transaction_id=order_track)
    except:
        messages.error(request, 'Track id invalid')
        return redirect('store:track_order')

    ctx = {'order': order}
    return render(request, 'store/track.html', ctx)


def addProduct(request):
    group = Group.objects.get(name='Sellers')
    sellers = User.objects.filter(groups=group)
    form = NewProduct()

    if request.user in sellers:
        if request.method == 'POST':
            form = NewProduct(request.POST, request.FILES)
            if form.is_valid():
                user = request.user
                title = form.cleaned_data['title']
                desc = form.cleaned_data['description']
                try:
                    products = Product.objects.get(title=title, description=desc)
                    if(len(products) > 0):
                        messages.error(request, 'Your product is very similar to this products: ' + str(products))
                        return redirect('store:addProduct')
                except:
                    pass
                # images = request.FILES.getlist('image')
                # for image in images:
                #     print(image)
                form.save()
                Product.objects.select_for_update().filter(title=title, description=desc).update(seller=user)
                return redirect('store:index')
            else:
                messages.error(request, form.errors)
                print(form.errors)

        ctx = {'form': form}

        return render(request, 'store/addProduct.html', ctx)
    else:
        messages.error(request, 'You do not have permission to access that page!')
        return redirect('store:index')

def viewProduct(request, product_id):
    product = Product.objects.get(id=product_id)
    product_info = product.info
    product_info = product_info.split('\n')
    for line in product_info:
        if line == '\r':
            product_info.remove('\r')

    total_rating_num = len(Rating.objects.filter(product_rated=product))
        
    # product_desc = product.description.split(' ')
    product_desc = re.split(' |\n', product.description)

    for word in product_desc:
        if 'script' in word:
            product_desc.remove(word)
    product_desc = ' '.join(product_desc)

    ctx = {'product': product, 'product_info': product_info, 'desc':product_desc, 'rating_max': range(1,6), 'total_rating_num': total_rating_num}
    return render(request, 'store/Product.html', ctx)

def rate_product(request):
    if request.method == 'POST':
        el_id = request.POST.get('el_id')
        val = request.POST.get('val')
        product = Product.objects.get(id=el_id)
        if request.user.is_authenticated:
            customer = get_object_or_404(Customer, user=request.user)
        else:
            uid = request.COOKIES.get('device')
            if uid == None:
                messages.warning(request, 'We use cookies in order to let you order items without an account so please enable cookies(and javascript) or login with your account in order to continue!')
                return redirect('store:index')
            else:
                try:
                    customer = Customer.objects.get(uid=uid)
                except:
                    print('nono')
                    messages.warning(request, "In order to prevent bots from rating products, your review will be noted and displayed once you purchase the item")
                    return redirect('store:index')

        obj = Rating(rating=val, product_rated=product, customer_rated=customer)
        # print(product.avg_rating)
        obj.save()

        try:
            avg = (product.ratings + int(obj.rating))
        except:
            avg = int(obj.rating)
        Product.objects.select_for_update().filter(id=el_id).update(ratings=avg)
        product = Product.objects.get(id=el_id)

        rates = Rating.objects.filter(product_rated=product)

        user_rating = Rating.objects.filter(product_rated=product, customer_rated=customer)
        times_rated = len(user_rating)

        if times_rated > 1:
            product_rating = int(product.ratings) - user_rating[0].rating
            rating = product_rating
            user_rating[0].delete()
        else:
            rating = int(product.ratings)
        avg_rating = rating/len(rates)
        Product.objects.select_for_update().filter(id=el_id).update(ratings=rating, avg_ratings=avg_rating)

        print('rating: ', rating/len(rates))
        return JsonResponse({'success':'true', 'rating':val}, safe=False)
    return JsonResponse({'success':'False'})


def api(request):
    if request.method == 'GET':
        try:
            token = Token.objects.get(user=request.user)
            return render(request, 'store/api.html', {'token': token})
        except:
            messages.warning(request, "You don't have permissions to access this webpage")
            return redirect('store:index')
    
    

@api_view(['GET'])
@authentication_classes([TokenAuthentication])  
@permission_classes([IsAuthenticated])
def productsApi(request):
    # if request.is_ajax():
    #     return JsonResponse({'success':'true'}, safe=False)
    
    if request.method == 'GET':
        # print(request.headers)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@authentication_classes([TokenAuthentication])  
@permission_classes([IsAuthenticated])
def singleProductApi(request, pk):
    try:
        products = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(products)
        return Response(serializer.data, status=status.HTTP_200_OK)



def test(request):
    # products = Product.objects.all()
    # paginator = Paginator(products, 1)

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    # ctx = {'page_obj': page_obj, 'sellers': sellers, 'form': form}
    images = request.FILES.getlist('images')
    for image in images:
        print(image)
    ctx = {}

    return render(request, 'store/test.html', ctx)
