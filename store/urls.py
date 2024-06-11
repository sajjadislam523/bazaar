from django.urls import path
from .views import store, search, product_detail, submit_review

urlpatterns = [
    path('', store, name='store'),
    path('search/', search, name='search'),
    path('category/<slug:category_slug>/', store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', product_detail, name='product_detail'),
    path('submit_review/<int:product_id>/', submit_review, name='submit_review'),
]