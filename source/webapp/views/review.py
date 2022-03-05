from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import reverse, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from webapp.models import Review, Product
from webapp.forms import ReviewForm, ModerForm


class ReviewCreateView(LoginRequiredMixin, CreateView):
    template_name = 'review/review_create.html'
    form_class = ReviewForm
    model = Review

    def get(self, request, *args, **kwargs):
        self.kwargs['product'] = kwargs.get('pk')
        self.object = None
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.product = Product.objects.get(pk=self.kwargs.get('pk'))
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.kwargs.get('pk')})


class ReviewUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'webapp.change_review'
    form_class = ReviewForm
    model = Review
    template_name = 'review/review_update.html'
    context_object_name = 'product'

    def has_permission(self):
        review = get_object_or_404(Review, id=self.kwargs.get('pk'))
        return super().has_permission() or (self.request.user == review.author)
    def get_form_class(self):
        if self.request.user.groups.filter(name='Moderator').exists():
            self.form_class = ModerForm
        return super().get_form_class()

    def form_valid(self, form):
        self.object = form.save()
        if not self.request.user.groups.filter(name='Moderator').exists():
            self.object.is_moderated = False
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:product_detail', kwargs={'pk': self.object.product.id})


class ReviewDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'webapp.delete_review'

    def has_permission(self):
        review = get_object_or_404(Review, id=self.kwargs.get('pk'))
        return super().has_permission() or (self.request.user == review.author)

    template_name = 'review/review_delete.html'
    model = Review
    context_object_name = 'review'
    success_url = reverse_lazy('webapp:index_product')


class ModerReview(PermissionRequiredMixin, ListView):
    permission_required = 'webapp.can_moderate_reviews'
    template_name = 'review/is_modered.html'
    model = Review
    context_object_name = 'reviews'

    def get_queryset(self):
        queryset = Review.objects.filter(is_moderated=False).order_by('-update_date')
        return queryset

