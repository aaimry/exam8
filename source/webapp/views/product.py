from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from webapp.models import Product, Review
from webapp.forms import ProductForm, ReviewForm, ModerForm


class IndexProductView(ListView):
    template_name = 'product/index_product.html'
    model = Product
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/detail_view.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm('webapp.can_moderate_reviews'):
            context['review'] = self.object.review_product.all()
        else:
            context['review'] = self.object.review_product.all().exclude(is_moderated=False)
        return context


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'webapp.add_product'
    template_name = 'product/create.html'
    form_class = ProductForm
    model = Product
    success_url = reverse_lazy('webapp:index_product')


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'webapp.change_product'
    form_class = ProductForm
    model = Product
    template_name = 'product/product_update.html'
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.kwargs.get('pk')})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'webapp.delete_product'
    template_name = 'product/product_delete.html'
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy('webapp:index_product')
