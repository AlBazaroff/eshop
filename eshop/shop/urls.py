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
     path('content/<str:type>/<int:id>/', views.get_content,
          name='get_content'),
     # ADMIN
     # Product CRUD
     path('admin/product/product_list/', views.admin_product_list,
          name='admin_product_list'),
     path('admin/product/add/', views.product_add,
          name='product_add'),
     path('admin/product/update/<int:product_id>/', views.product_update,
          name='product_update'),
     path('admin/product/remove/<int:product_id>/', views.product_delete,
          name='product_delete'),
     # Category CRUD
     path('admin/category/list/', views.admin_category_list,
          name='admin_category_list'),
     path('admin/category/add/', views.category_add,
          name='category_add'),
     path('admin/category/update/<int:category_id>/', views.category_update,
          name='category_update'),
     path('admin/category/delete/<int:category_id>/', views.category_delete,
          name='category_delete'),
     # Product content
     path('admin/product/content/add/<int:product_id>/',
          views.product_content_add, name='product_content_add'),
     path('admin/product/content/delete/<int:content_id>/',
          views.product_content_delete, name='product_content_delete'),
]