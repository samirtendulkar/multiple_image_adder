from django.views.generic import UpdateView, ListView, DetailView, DeleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.shortcuts import redirect
from .forms import PostForm, PostEditForm, PrepFormSet, PrepEditFormSet
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.db import transaction
from django.shortcuts import render
import datetime
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy


User = get_user_model()


'''This is the post create view'''
@login_required
def post_create(request):
    user = request.user
    x = datetime.datetime.now()
    post = Post.objects.create(user=user, title=(str(user.username) + " please complete your draft created at " + str(x.strftime("%c"))))
    return HttpResponseRedirect(reverse('posts:edit', kwargs={'slug': post.slug}))


# @login_required
# def post_create(request):
#     ImageFormSet = modelformset_factory(Prep, fields=('image', 'image_title', 'image_description'), extra=12, max_num=12,
#                                         min_num=2)
#     if request.method == "POST":
#         form = PostForm(request.POST or None, request.FILES or None)
#         formset = ImageFormSet(request.POST or None, request.FILES or None)
#         if form.is_valid() and formset.is_valid():
#             instance = form.save(commit=False)
#             instance.user = request.user
#             instance.save()
#             for index, f in enumerate(formset.cleaned_data):
#                 try:
#                     photo = Prep(sequence=index+1, post=instance, image=f['image'],
#                                  image_title=f['image_title'], image_description=f['image_description'])
#                     photo.save()
#
#                 except Exception as e:
#                     break
#             return redirect('posts:single', username=instance.user.username, slug=instance.slug)
#     else:
#         form = PostForm()
#         formset = ImageFormSet(queryset=Prep.objects.none())
#     context = {
#         'form': form,
#         'formset': formset,
#     }
#     return render(request, 'posts/post_form.html', context)


'''This is the post edit view'''
class PostPrepUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ('title', 'message', 'post_image')
    template_name = 'posts/post_edit.html'

    def get_success_url(self):
        slug = self.kwargs.get('slug')
        return reverse('posts:single', kwargs={'username': self.request.user.username, 'slug': slug})

    def get_context_data(self, **kwargs):
        data = super(PostPrepUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['prep'] = PrepEditFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['prep'] = PrepEditFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        prep = context['prep']
        with transaction.atomic():
            self.object = form.save()

            if prep.is_valid():
                prep.instance = self.object
                print(prep.instance)
                prep.save()
        return super(PostPrepUpdate, self).form_valid(form)


class Postlist(ListView):
    model = Post

    def get_queryset(self):
        completed_posts = Post.objects.filter(is_draft=False)
        queryset = completed_posts.order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(Postlist, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            context['is_draft'] = user.posts.filter(is_draft=True).count()
        return context


class PostDraftlist(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/drafts.html'

    def get_queryset(self):
        completed_posts = Post.objects.filter(is_draft=True)
        queryset = completed_posts.order_by('created_at')
        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super(PostDraftlist, self).get_context_data(**kwargs)
    #     user = self.request.user
    #     if user.is_authenticated:
    #         context['is_draft'] = user.posts.filter(is_draft=True).count()
    #     return context


class PostDetail(DetailView):
    model = Post


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs)



