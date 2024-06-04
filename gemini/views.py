from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.decorators import login_required

from gemini.models import Post, Favorited

# Create your views here.


def index(request):
    context = {}
    return render(request, 'gemini/index.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'gemini/post_list.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-date_created')[:20]


class PostDetailView(DetailView):
    model = Post
    template_name = 'gemini/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_favorite'] = Favorited.objects.filter(user=self.request.user, post=self.object).exists()
        return context


@login_required
@require_POST
def toggle_favorite(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        try:
            Favorited.objects.get(user=request.user, post=post).delete()
            is_favorite = False
        except Favorited.DoesNotExist:
            Favorited.objects.create(user=request.user, post=post)
            is_favorite = True
        return JsonResponse({'is_favorite': is_favorite})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required
def favorite_posts(request):
    fav_posts = Favorited.objects.filter(user=request.user).order_by('-date_added')
    context = {'fav_posts': fav_posts}
    return render(request, 'gemini/favorite_posts.html', context)


@require_GET
def search_results(request):
    # having issues with input data in sqlite
    # should work properly with postgresql
    query = request.GET.get('q', '')
    results = []
    count = 0

    if query and len(query) >= 3:
        results = Post.objects.filter(title_ru__icontains=query)
        count = results.count()
        message = f'Search results for {query} ({count})'
    else:
        message = 'Query is too short. Please enter at least 3 characters.'
    return render(request, 'gemini/search_results.html', {'results': results, 'message': message})


@require_POST
def live_search(request):
    query_word = request.POST.get('query')
    results = Post.objects.filter(title_ru__icontains=query_word)
    data = []
    for result in results[:5]:
        item = {'pk': result.pk, 'title_ru': result.title_ru}
        data.append(item)

    result_count = results.count()
    show_more = result_count > 5
    return JsonResponse({'data': data, 'show_more': show_more, 'result_count': result_count}, safe=False)
