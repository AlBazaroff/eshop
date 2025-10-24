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
     path('product/admin/product_list/', views.admin_product_list,
          name='admin_product_list'),
     # edit products
     path('product/add/', views.product_add,
          name='product_add'),
     path('product/update/<int:product_id>/', views.product_update,
          name='product_update'),
     path('product/remove/<int:product_id>/', views.product_remove,
          name='product_remove'),
     # category add
     path('category/add', views.category_add,
          name='category_add'),
]