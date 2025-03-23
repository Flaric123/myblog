from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Article, Comment
from .forms import CommentForm
from django.shortcuts import redirect
from django.contrib import messages

class HomeView(ListView):
    model = Article
    template_name = "home.html"
    context_object_name = "articles"
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Article.objects.filter(title__icontains=query)
        return Article.objects.all()

class ArticleDetailView(DetailView):
    model = Article
    template_name = "article_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST, user=request.user)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            if request.user.is_authenticated:
                comment.user = request.user
            else:
                comment.guest_name = form.cleaned_data.get('guest_name')
            comment.save()
            messages.success(request, "Комментарий успешно оставлен!")
            return redirect('article_detail', pk=self.object.pk)
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "article_detail.html"

    def form_valid(self, form):
        form.instance.article = Article.objects.get(id=self.kwargs["article_id"])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("article_detail", kwargs={"pk": self.kwargs["article_id"]})
