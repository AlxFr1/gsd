from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic import CreateView
from django.views.generic.edit import ModelFormMixin

from blog_hillel.forms import RegisterUserForm
from blog_hillel.models import Post, Profile


class Home(TemplateView):
    template_name = "home.html"


class ProfileList(ListView):
    queryset = User.objects.all()
    template_name = "profile_list.html"


class NewPost(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Post
    success_message = 'Author successfully created'
    template_name = "post_create.html"
    fields = ('title', 'descript', 'image', 'is_posted')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Profile.objects.get(pk=self.request.user.pk)
        post.save()

        return super(NewPost, self).form_valid(form)


class PostList(ListView):
    template_name = "post_list.html"
    queryset = Post.objects.all().filter(is_posted=True)


class PostInfo(DetailView):
    template_name = "post_detail.html"
    model = Post


class PostUpdate(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Post
    template_name = 'post_create.html'
    fields = '__all__'
    success_message = 'Author successfully updated'
    success_url = reverse_lazy('post-list')
    login_url = '/admin/'


class PostDelete(LoginRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_message = 'Author successfully deleted'
    success_url = reverse_lazy('post-list')
    login_url = '/admin/'


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register_form.html'
    success_url = reverse_lazy('home')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'login_form.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
