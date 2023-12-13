from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from datetime import datetime
from .filters import NewsFilter
from .forms import PostForm
from django.urls import reverse_lazy
class NewsList(ListView):
    model = Post
    ordering = 'date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 4

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     self.filterset = NewsFilter(self.request.GET, queryset)
    #     return self.filterset.qs
    #
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class PostSearch(ListView):
    model = Post
    ordering = 'date'
    template_name = 'search.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context



class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostCreate(CreateView):
    form_class = PostForm
    model = Post


    def get_template_names(self):
        if self.request.path == '/news/articles/create/':
            self.template_name = 'articles_create.html'
        else:
            self.template_name = 'post_create.html'
        return self.template_name

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/articles/create/':
            post.choice_field = 'article'
            post.save()
        return super().form_valid(form)

class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def get_template_names(self):
        if self.request.path == f'news/articles/{self.object.pk}/edit':
            self.template_name = 'articles_edit.html'
        else:
            self.template_name = 'post_edit.html'
        return self.template_name

class PostDelete(DeleteView):
    model = Post
    template_name = 'product_delete.html'
    success_url = reverse_lazy('post_list')
    context_object_name = "post"

    def get_template_names(self):
        if self.request.path == f'/news/articles/{self.object.pk}/delete':
            self.template_name = 'articles_delete.html'
        else:
            self.template_name = 'post_delete.html'
        return self.template_name

