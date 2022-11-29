import random
from traceback import print_exception
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from django.shortcuts import render, redirect
from BookHouse.settings import RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY
from display.models import *
from django.db.models import Q
from django.views.decorators.cache import cache_control
import razorpay
client = razorpay.Client(
    auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sortby(request):
    if request.user.is_anonymous:
        return redirect('/')
    if request.method == 'POST':
        search = request.POST.get('searched')
        cat_id = request.POST.get('catid')
        subcat_id = request.POST.get('subcatid')
        sort_by = request.POST.get('sorted_by')

        result = ""
        if(search != 'default'):
            result = Book.objects.filter(Q(publication=search) | Q(
                author=search) | Q(book_title=search))
            if not result:
                filter = Category.objects.get(category_name=search)
                result = Book.objects.filter(category=filter)
        elif(cat_id != '-1'):

            filter = Category.objects.filter(id=cat_id)
            result = Book.objects.filter(category_id=cat_id)
        else:
            result = Book.objects.filter(
                subcategory_id=subcat_id)

        result = result.order_by(sort_by)

        cats = Category.objects.all()  # fetching all categories
        sub_cats = SubCategory.objects.all()  # fetching all sub-catgories
        wishlist_item = Wishlist.objects.filter(user=request.user)
        cart_item = Cart.objects.filter(user=request.user)
        lists = [item.book.id for item in wishlist_item]
        list2 = [item.book.id for item in cart_item]
        context = {"value": search, "book": result, 'number': cart_item.count, "catid": cat_id, "subcatid": subcat_id,
                   "wishlists": lists, "carts": list2, 'cats': cats, 'sub_cats': sub_cats}
        # print(lists)
        # print(list2)
        return render(request, 'book_search.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def book_search(request, item=0):
    if request.user.is_anonymous:
        return redirect('/')

    if (request.method == 'POST' and item == 0):  # dashboard search function
        search = request.POST.get('search')
        subcatID = request.POST.get('subcatID')

        if not subcatID and search == '':
            return redirect('/dashboard/')
        if search:
            result = Book.objects.filter(Q(publication=search) | Q(
                author=search) | Q(book_title=search))
        if subcatID:
            result = Book.objects.filter(sub_category=subcatID)

        # result = Book.objects.raw(
        #     'select * from display_book where %s in (publication,author,book_title)', [search])
        cats = Category.objects.all()  # fetching all categories
        sub_cats = SubCategory.objects.all()  # fetching all sub-catgories
        wishlist_item = Wishlist.objects.filter(user=request.user)
        cart_item = Cart.objects.filter(user=request.user)
        lists = [item.book.id for item in wishlist_item]
        list2 = [item.book.id for item in cart_item]
        context = {"value": search, "book": result, 'number': cart_item.count,
                   "wishlists": lists, "carts": list2, 'cats': cats, 'sub_cats': sub_cats}
        # print(lists)
        # print(list2)
        return render(request, 'book_search.html', context)
    elif item != 0:  # category clicked
        filter = Category.objects.filter(id=item)
        cats = Category.objects.all()  # fetching all categories
        sub_cats = SubCategory.objects.filter(category=item)
        value = [item.category_name for item in filter]
        result = Book.objects.filter(category=item)
        # sort_by_price = result.order_by('price')
        # sort_by_author = result.order_by('author')
        # sort_by_title = result.order_by('book_title')
        wishlist_item = Wishlist.objects.filter(
            user=request.user)
        cart_item = Cart.objects.filter(user=request.user)
        lists = [item.book.id for item in wishlist_item]
        list2 = [item.book.id for item in cart_item]

        context = {"value": value[0], "book": result, "catid": item,
                   "wishlists": lists, "carts": list2, 'number': cart_item.count, 'cats': cats, "sub_cats": sub_cats}

        return render(request, 'book_search.html', context)

    elif request.method == 'GET' and item == 0:
        subcatID = request.GET.get('subcatID')
        print(subcatID)
        result = Book.objects.filter(subcategory=subcatID)
        print(result)
        cats = Category.objects.all()  # fetching all categories
        sub_cats = SubCategory.objects.all()  # fetching all sub-catgories
        wishlist_item = Wishlist.objects.filter(user=request.user)
        cart_item = Cart.objects.filter(user=request.user)
        lists = [item.book.id for item in wishlist_item]
        list2 = [item.book.id for item in cart_item]
        context = {"book": result, 'number': cart_item.count, "subcatid": subcatID,
                   "wishlists": lists, "carts": list2, 'cats': cats, 'sub_cats': sub_cats}
        return render(request, 'book_search.html', context)

    return render(request, 'book_search.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addtowishlist(request):
    if request.user.is_anonymous:
        return redirect('/')

    if(request.method == 'GET'):
        book_id = request.GET.get('book_id')
        wishlist_obj = Wishlist.objects.create(
            book_id=book_id, user_id=request.user.id)
        wishlist_obj.save()
        print('added successfully')
        return redirect('/book_search/0')

    return redirect('/book_search/0')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def showwishlist(request):
    if request.user.is_anonymous:
        return redirect('/')

    result = Wishlist.objects.filter(user=request.user).select_related('book')
    cart_item = Cart.objects.filter(user=request.user)
    #lists = [item.book.id for item in wishlist_item]
    list2 = [item.book.id for item in cart_item]
    context = {'wishlists': result, 'carts': list2, 'number': cart_item.count}

    return render(request, 'wishlist.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def removewishlistpage(request, id):
    if request.user.is_anonymous:
        return redirect('/')

    Wishlist.objects.filter(Q(user=request.user) and Q(book_id=id)).delete()

    return redirect('/showwishlist/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):
    if request.user.is_anonymous:
        return redirect('/')
    user_profile = UserProfile.objects.filter(
        user=request.user).select_related()
    cart_item = Cart.objects.filter(user=request.user).count
    context = {"profiles": user_profile, 'number': cart_item}
    return render(request, 'profile.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def removewishlist(request):
    if request.user.is_anonymous:
        return redirect('/')
    if(request.method == 'GET'):
        book_id = request.GET.get('book_id')
        Wishlist.objects.filter(Q(user=request.user)
                                and Q(book_id=book_id)).delete()
        print('deleted successfully')

        return redirect('/book_search/0')
    redirect('/book_search/0')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def showcart(request):
    if request.user.is_anonymous:
        return redirect('/')
    result = Cart.objects.filter(user=request.user).select_related('book')

    context = {'cartlist': result, 'number': result.count}
    return render(request, 'cart.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addtocart(request):
    if request.user.is_anonymous:
        return redirect('/')
    print("about to add in cart")
    if(request.method == 'GET'):
        book_id = request.GET.get('book_id')
        cart_obj = Cart.objects.create(
            book_id=book_id, user_id=request.user.id)
        cart_obj.save()
        print('added successfuly in cart')
        return redirect('/book_search/0')

    return redirect('/book_search/0')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def removecartpage(request, id):
    if request.user.is_anonymous:
        return redirect('/')
    id = int(id)

    Cart.objects.filter(Q(user=request.user) and Q(book_id=id)).delete()
    return redirect('/showcart/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def updatequantity(request):
    if request.user.is_anonymous:
        return redirect('/')

    if(request.method == 'GET'):
        bookid = request.GET.get('book_id')
        quantity = int(request.GET.get('quantity'))
        cart = Cart.objects.get(Q(user=request.user) and Q(book_id=bookid))
        quant = int(cart.quantity)
        print(quant)
        cart.quantity = quant + quantity
        cart.save()
    return redirect('/showcart/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def save_profile(request):
    if request.user.is_anonymous:
        return redirect('/')

    if(request.method == 'POST'):
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        address = request.POST.get('address')
        mobile = request.POST.get('phone')
        print(mobile)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.name = name
        user_profile.bio = bio
        user_profile.address = address
        user_profile.phone = mobile
        user_profile.save()
    print('profile saved successfully')
    return redirect('/profile/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkout(request):
    if request.user.is_anonymous:
        return redirect('/')
    if request.method == 'POST':
        amount = int(float(request.POST.get('amount'))*100)
        result = Cart.objects.filter(user=request.user).select_related('book')
        payment = client.order.create(
            {'amount': int(amount), 'currency': 'INR', 'payment_capture': '1'})
        payment_id = payment['id']
        total = amount/100
        context = {'orderlist': result, 'amount': total, 'api_key': RAZORPAY_API_KEY,
                   'payment_id': payment_id}
        return render(request, 'payment.html', context)
    return redirect('/showcart/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment(request):
    if request.user.is_anonymous:
        return redirect('/')

    if request.method == 'POST':
        amount = request.POST.get('amount')
        pay_id = request.POST.get('pay_id')
        print(amount + pay_id)
        payment = BookPayment.objects.create(
            user=request.user, amount=amount, transaction_code=pay_id, transaction_status="success")
        payment.save()
        results = Cart.objects.filter(user=request.user)
        issue_staus = Issued_Status.objects.get(status="Requested")
        print(issue_staus)
        for result in results:
            bookid = result.book
            qty = result.quantity
            userorder = BookOrder.objects.create(
                user=request.user, book=bookid, quantity=qty, issue_status=issue_staus, payment_id=payment)
            userorder.save()
            bookrequest = BookRequest.objects.create(
                user=request.user, book=bookid, quantity=qty, issue_status=issue_staus, payment_id=payment)
            bookrequest.save()
            Cart.objects.filter(user=request.user).delete()

    return render(request, 'orderplaced.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def myorders(request):
    if request.user.is_anonymous:
        return redirect('/')
    #result = BookOrder.objects.filter(user=request.user).select_related()
    result = BookOrder.objects.filter(
        user=request.user).order_by('-order_date')
    cart_item = Cart.objects.filter(user=request.user).count
    context = {'orderlist': result, 'number': cart_item}
    return render(request, 'myorder.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def pricing(request):
    if request.user.is_anonymous:
        return redirect('/')
    cart_item = Cart.objects.filter(user=request.user).count

    context = {'number': cart_item}
    return render(request, 'pricing.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def purchase(request):
    if request.user.is_anonymous:
        return redirect('/')
    if request.method == 'POST':
        amount = int(float(request.POST.get('amount'))*100)
        payment = client.order.create(
            {'amount': int(amount), 'currency': 'INR', 'payment_capture': '1'})
        payment_id = payment['id']
        total = amount/100
        month = 0
        if(total == 300):
            month = 1
        elif(total == 1100):
            month = 4
        elif(total == 3000):
            month = 12

        today = date.today()
        uptodate = today + relativedelta(months=month)
        cart_item = Cart.objects.filter(user=request.user).count
        context = {'amount': total, "month": month, 'today': today, 'uptodate': uptodate, 'api_key': RAZORPAY_API_KEY,
                   'payment_id': payment_id, 'number': cart_item}
        return render(request, 'purchase.html', context)

    return render(request, 'purchase.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def room_payment(request):
    if request.user.is_anonymous:
        return redirect('/')

    if(request.method == 'POST'):
        amount = request.POST.get('amount')
        pay_id = request.POST.get('pay_id')
        month = request.POST.get('month')
        start_date = request.POST.get('start')
        upto_date = request.POST.get('upto')

        start_date = start_date.replace('.', '')
        upto_date = upto_date.replace('.', '')
        start = datetime.strptime(start_date, '%b %d, %Y').strftime('%Y-%m-%d')
        uptodate = datetime.strptime(
            upto_date, '%b %d, %Y').strftime('%Y-%m-%d')

        block = chr(random.randint(ord('A'), ord('Z')))
        seat = random.randint(0, 9)
        payment = RoomPayment.objects.create(
            user=request.user, price=amount, month=month, start_date=start, upto_date=uptodate, payment_id=pay_id, transaction_status="success", table_block=block, seat_alloted=seat)
        payment.save()
        cart_item = Cart.objects.filter(user=request.user).count
        context = {'blocks': block, 'seat': seat, 'number': cart_item}
        return render(request, 'orderplaced.html', context)
    return redirect('/dashboard/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def roomorder(request):
    if request.user.is_anonymous:
        return redirect('/')
    object = RoomPayment.objects.filter(user=request.user)
    cart_item = Cart.objects.filter(user=request.user).count
    context = {'orderlist': object, 'number': cart_item}
    return render(request, 'roomorder.html', context)
