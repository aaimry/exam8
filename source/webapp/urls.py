from django.urls import path

from webapp.views import ReviewDeleteView, ReviewUpdateView, ReviewCreateView, ModerReview
from webapp.views.product import (
    IndexProductView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView)

app_name = 'webapp'

urlpatterns = [
    path('', IndexProductView.as_view(), name='index_product'),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('prpduct/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/review/create/', ReviewCreateView.as_view(), name='review_create'),
    path('review/<int:pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('no_reviews/', ModerReview.as_view(), name='moder_reviews')
]
