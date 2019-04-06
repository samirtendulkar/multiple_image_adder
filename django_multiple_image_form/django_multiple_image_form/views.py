from django.shortcuts import render, redirect
from .forms import UserCreateForm
from django.views.generic import TemplateView
from posts.models import Post


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            return redirect('all')
    else:
        form = UserCreateForm()
    context = {'form': form}
    return render(request, 'signup.html', context)

# Create your views here.


class Homepage(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)
        context['post_list'] = Post.objects.all()
        return context

