from django.contrib import admin
from django.urls import path
from app import views
from project import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name="home" ),
    path('home',views.home,name="home" ),
    path("about",views.about,name='about'),
    path("services",views.services,name='services'),
    path('vendorregister/',views.vendorregister,name="vendorreg"),
    path('customerregister',views.customerregister,name="customerreg"),
    path('login',views.login1,name="login"),
    path('vendordash',views.vendordash,name="vendordash"),
    path('customerdash',views.customerdash,name="customerdash"),
    path('addproduct',views.addproduct,name="addproduct"),
    path('viewproduct',views.view_product,name="viewproduct"),
    path('edit_product/<int:id>',views.edit_product,name="edit_product"),
    path('customer_view_product',views.customer_viewproduct,name="cus_view"),
    path("passwordreset",views.passwordreset,name='resetp'),
    path("newpassword/<str:token>/<int:id1>",views.newpassword,name='reset'),
    path("generatebill",views.generate_bill,name='generatebill'),
    path("logout",views.logout,name='logout'),
    path('complaint',views.complaint,name="complaint"),
    path('search_product',views.search_product,name='search_product'),
    path('registeredshops',views.registeredshops,name="registeredshops"),
    path('profile',views.profile,name="profile"),
    path('add_special_product',views.add_special_product,name="add_special_product"),
    path('view_spl_offers',views.view_spl_offer,name="view_offer"),
    path('display_profile',views.display_profile,name="view_profile"),
    path('cart',views.cart,name="cart"),
    path('v_special_offer',views.v_special_offer,name="v_special_offer"),
    path('view_prebooked',views.view_prebooked,name="view_prebooked"),
    path('booked_products',views.booked_products,name="booked_products")
]


