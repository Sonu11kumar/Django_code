from django.conf.urls import url
from . import views

app_name = 'music'

urlpatterns = [
    url(r'^lists/$', views.lists, name='lists'),
    url(r'^base/(?P<pk>\d+)/$', views.base, name='base'),
    url(r'^index/$', views.index, name='index'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^details/(?P<album_id>[0-9]+)/$', views.details, name='details'),
    # url(r'^(?P<id>\d+)/$', views.single, name='single'),
    url(r'^single/(?P<pk>\d+)/$', views.single, name='single'),
    url(r'^login/$', views.login_sign, name='login_sign'),
    url(r'^logout/$', views.logout_sign, name='logout_sign'),
    url(r'^register/$', views.register_sign, name='register_sign'),
    # url(r'^result/$', views.search, name='search'),
    #url(r'^paginator/$', views.post_list, name='post_list'),
    url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', views.add_to_cart, name="add_to_cart"),
    url(r'^order-summary/$', views.order_details, name="order_summary"),
    url(r'^success/$', views.success, name='purchase_success'),
   # url(r'^delete/(?P<item_id>[-\w]+)/$', views.delete_from_cart, name='delete_from_cart'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^payment/(?P<order_id>[-\w]+)/$', views.process_payment, name='process_payment'),
    url(r'^update-transaction/(?P<order_id>[-\w]+)/$', views.update_transaction_records,
        name='update_records'),
    url(r'^me/$', views.my_profile, name='my_profile'),
    url(r'^products/', views.product_list, name='product_list'),
    url(r'^(?P<item_id>\d+)/delete/', views.delete_from_cart, name='delete_from_cart')
]
