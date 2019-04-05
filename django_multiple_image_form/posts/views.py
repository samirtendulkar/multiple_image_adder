from django.views.generic import UpdateView, ListView, DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.shortcuts import redirect
from .forms import PostForm, PostEditForm, PrepFormSet, PrepEditFormSet
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.db import transaction
from django.shortcuts import render

User = get_user_model()


'''This is the post create view'''
def post_create(request):
    ImageFormSet = modelformset_factory(Prep, fields=('image', 'image_title', 'image_description'), extra=12, max_num=12,
                                        min_num=2)
    if request.method == "POST":
        form = PostForm(request.POST or None)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            for index, f in enumerate(formset.cleaned_data):
                try:
                    photo = Prep(sequence=index+1, post=instance, image=f['image'],
                                 image_title=f['image_title'], image_description=f['image_description'])
                    photo.save()

                except Exception as e:
                    break
            return redirect('posts:single', username=instance.user.username, slug=instance.slug)
    else:
        form = PostForm()
        formset = ImageFormSet(queryset=Prep.objects.none())
    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'posts/post_form.html', context)


'''This is the post edit view'''
class PostPrepUpdate(UpdateView):
    model = Post
    fields = ('title', 'message', 'post_image', 'group')
    template_name = 'posts/post_edit.html'

    def get_success_url(self):
        # pdb.set_trace()
        slug = self.kwargs.get('slug')
        return reverse('posts:single', kwargs={'username': self.request.user.username, 'slug': slug})

    def get_context_data(self, **kwargs):
        # pdb.set_trace()
        data = super(PostPrepUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['prep'] = PrepEditFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['prep'] = PrepEditFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        # pdb.set_trace()
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


class PostDetail(DetailView):
    model = Post