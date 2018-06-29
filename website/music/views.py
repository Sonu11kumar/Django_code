from django.contrib.admin.templatetags.admin_list import pagination
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth import (authenticate, login, get_user_model, logout,)
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, PostForm, UserRegistrationForm, OrderForm
from django.http import HttpResponseRedirect
from .models import Album, Post, Profile, OrderItem, Order, Product, Transaction
from django.views.generic import ListView
from datetime import timezone,datetime
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import string, random
from datetime import date
from django.urls import reverse_lazy
from django.conf import settings
#import stripe

#stripe.api.key = settings.STRIPE_SECRET_KEY


def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        context = form.save(commit=False)
        print(form.cleaned_data.get("title"))
        context.save()
        return HttpResponseRedirect(context.get_absolute_url())

    context = {
        "form": form,
    }
    return render(request, 'music/post_form.html', context)


def post_update(request, pk):
    plane = get_object_or_404(Post, id=pk)
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        plane = form.save(commit=False)
        plane.save()
        return HttpResponseRedirect(plane.get_absolute_url())
    context = {"title": plane.title, "plane": plane, "form": form, }
    return render(request, 'music/post_form.html', context)


def lists(request):
    queryset = Post.objects.all()
    queryset_ = Post.objects.all()
    paginator = Paginator(queryset, 10)
    page_request_var = "abc"
    page = request.GET.get(page_request_var)
    query = request.GET.get("q")
    try:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {"object_list": queryset, "title": "List", "page_request_var": page_request_var}

    return render(request, 'music/single.html', context)


def single(request, pk):
    plane = get_object_or_404(Post, id=pk)
    context = {"title": plane.title, "plane": plane}
    return render(request, 'music/single.html', context)


def index(request):
    all_albums = Album.objects.all()
    context = {'all_albums': all_albums}
    return render(request, 'music/index.html', context)


def details(request, album_id):
    album = Album.objects.get(pk=album_id)
    return render(request, 'music/detail.html', {'album': album})


def base(request, pk):
    plane = get_object_or_404(Post, id=pk)
    context = {"title": plane.title, "plane": plane}
    return render(request, 'music/index.html', context)


def login_sign(request):
    title = "Login"
    form1 = UserLoginForm(request.POST or None)
    if form1.is_valid():
        username = form1.cleaned_data.get("username")
        password = form1.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/music/index/")
        print(request.user.is_authenticated())
    return render(request, "music/post_form.html", {"form1": form1, "title": title})


def register_sign(request):
    title = "Register"
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        New_user = authenticate(username=user.username, password=password)
        login(request, New_user)
        return redirect("/music/lists/")

    context = {
        "form": form,
        "title": title
    }

    return render(request, "music/form.html", context)


def logout_sign(request):
    logout(request)
    #return render(request, "music/post_form.html", {})
    return redirect('music:index')


"""def search(request):
    template = 'music/paginator.html'
    query = request.GET.get("q")
    result = Person.objects.filter(Q(title_icontains=query)|Q(updated_icontains=query))
    pages = pagination(request, result, num=1)
    context = {"items": pages[0],
               "page_range": pages[1]}

    return render(request, template, context)"""


@login_required(login_url='music/login/')
def get_user_pending_order(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        return order[0]
    return 0


@login_required(login_url='music/login/')
def my_profile(request):
    my_user_profile = Profile.objects.filter(user=request.user.first())
    my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
    context = {
        'my_order': my_orders
    }
    return render(request, "music/profile.html", context)


@login_required(login_url='music/login/')
def product_list(request):
    object_list = Product.objects.all()
    filtered_orders = Order.objects.filter(owner=request.user.profile)
    current_order_products = []
    if filtered_orders.exists():
        user_order = filtered_orders[0]
        user_order_items = user_order.items.all()
        current_order_products = [product.product for product in user_order_items]

    context = {'object_list': object_list,
               'current_order_products': current_order_products}

    return render(request, 'music/product_list.html', context)


@login_required(login_url='music/login/')
def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str


@login_required(login_url='music/login/')
def add_to_cart(request, **kwargs):
    user_profile = get_object_or_404(Profile, user=request.user)
    product = Product.objects.filter(id=kwargs.get("item_id", ""))
    if product in request.user.profile.ebook.all():
           messages.info(request, "user already own this book")
           return redirect(reverse("music:product_list"))

    order_item, status = OrderItem.objects.get_or_create(product=product[0])
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        user_order.ref_code = generate_order_id()
        user_order.save()
    messages.info(request, "item added to cart")
    return redirect(reverse('music:product_list'))


#@login_required(login_url='music/login/')
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
           item_to_delete[0].delete()
    messages.info(request, "item has been deleted ")
    return redirect(reverse('music:order_summary'))


'''def delete_from_cart(request, item_id):

    item_delete = get_object_or_404(OrderItem, pk=item_id)

    try:
        if request.method == 'POST':
            form = OrderForm(request.POST, instance=item_delete)
            item_delete.delete()
            messages.success(request, 'You have successfully deleted the post')
        else:
            form = PostForm(instance=item_delete)
    except Exception as e:
        messages.warning(request, 'The post could not be deleted. Error {}'.format(e))

    context = {
        'form': form,
    }
    return render(redirect('music:product_list'), context)'''


@login_required(login_url='music/login/')
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {'order': existing_order}
    return render(request, 'music/order_summary.html', context)


@login_required(login_url='music/login/')
def checkout(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {'order': existing_order}
    return render(request, 'music/checkout.html', context)


@login_required(login_url='music/login/')
def process_payment(request, order_id):
    return redirect(reverse("music:update_records", kwargs={'order_id': order_id}))


@login_required(login_url='music/login/')
def update_transaction_records(request, order_id):
    order_to_purchase = Order.objects.filter(pk=order_id).first()
    order_to_purchase.is_ordered = True
    order_to_purchase.date_ordered = datetime.datetime.now()
    order_to_purchase.save()
    order_items = order_to_purchase.items.all()
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())
    user_profile = get_object_or_404(Profile, user=request.user)
    order_products = [item.product for item in order_items]
    user_profile.ebooks.add(*order_products)
    user_profile.save()
    #********* Add payments ***********#
    # create a transaction
    '''transaction = Transaction(profile=request.user.profile, token=token, order_id=order_to_purchase.id,
                              amount=order_to_purchase.get_cart_total( ),success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save( )
    #********* Add email to send to the customer ***********#
    messages.info(request, "Thank you! Your items have been added to your profile")
    return redirect(reverse('music:my_profile'))'''


@login_required(login_url='music/login/')
def success(request, **kwargs):
    # a view signifying the transcation was successful
    return render(request, 'music/purchase_success.html', {})

