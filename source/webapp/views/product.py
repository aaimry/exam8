from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from webapp.models import Product
from webapp.forms import ProductForm


class IndexProductView(ListView):
    template_name = 'product/index_product.html'
    model = Product
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/detail_view.html'
    context_object_name = 'product'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     if self.request.user.groups.filter(name='Moderator').exists():
    #         context['reviews'] = self.object.review.all()
    #     else:
    #         context['reviews'] = self.object.review.all().exclude(is_moder=False)
    #     return context


class ProductCreateView(CreateView):
    template_name = 'product/create.html'
    form_class = ProductForm
    model = Product
    success_url = reverse_lazy('webapp:index_product')


class ProductUpdateView(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'product/product_update.html'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.kwargs.get('pk')})


class ProductDeleteView(DeleteView):
    template_name = 'product/product_delete.html'
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('webapp:index_product')
