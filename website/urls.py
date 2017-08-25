from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from medical import views

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^medical/home/',views.home,name='home'),
    url(r'^medical/products/(?P<prod_id>[0-9]+)/$',views.product,name='medical_prod'),
    url(r'^medical/products/(?P<prod_id>[0-9]+)$',views.add_cart,name='medical_cart_add'),
    url(r'^medical/product-add/$',views.add_product,name='medical_product_add'),
    url(r'^medical/employee-add/$',views.add_employee,name='employee_add'),
    url(r'^medical/products-checkout/$',views.products_checkout,name='products-checkout'),
    url(r'^medical/customer-details/$',views.customer_detail,name='customer-details'),
    url(r'^medical/products-buy/$',views.products_buy,name='products-buy'),
    url(r'^login/$', views.login_user),
    url(r'^$', views.login_user),
    url(r'^logout/$', views.logout_user),
	url(r'^notifications/$',views.notification_all,name = 'index_notific'),
    url(r'^medical/demand-supply/$',views.demand_supply,name='demand-supply'),
    url(r'^medical/demand-supply/(?P<prod_id>[0-9]+)$',views.add_demand_cart,name='demand-supply-cart'),
    url(r'^medical/demand-checkout/$',views.demand_checkout,name='demand-checkout'),
    url(r'^medical/demand-buy/$',views.demand_buy,name='demand-buy'),
    url(r'^medical/select-supplier/$',views.select_supplier,name='select_supplier'),
    url(r'^medical/profile-update/$',views.update_profile),
    url(r'^medical/all-suppliers/$',views.all_suppliers),

)
