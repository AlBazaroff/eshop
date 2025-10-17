from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
     path('', views.product_list, name='product_list'),
     # for define category
     path('<slug:category_slug>', views.product_list,
          name='product_list_by_category'),
     path('<int:id>/<slug:slug>/', views.product_detail,
          name='product_detail'),
     path('search/<str:name>/', views.product_search,
          name='product_search'),

     # admin
     path('admin/product_list/', views.admin_product_list,
          name='admin_product_list'),
     # edit products
     path('product/add/', views.admin_product_add,
          name='product_add'),
     path('product/<int:id>/update', views.admin_product_update,
          name='product_update'),
]