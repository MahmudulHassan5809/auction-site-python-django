from django.urls import path
from . import views

app_name = "auction"
urlpatterns = [
    path('add-product/', views.AddProductView.as_view(), name="add_product"),
    path('ajax/load-sub-categories/', views.load_sub_categories,
         name='ajax_load_sub_categories'),
    path('ajax/load-auction-session/', views.load_auction_session,
         name='ajax_load_auction_session'),
    path('product_list/', views.ProductListView.as_view(), name="product_list"),
    path('edit-product/<int:pk>',
         views.EditProductView.as_view(), name="edit_product"),
    path('delete-product/<int:pk>',
         views.DeleteProductView.as_view(), name="delete_product"),
]
