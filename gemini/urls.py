from django.urls import path
from gemini import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:post_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_posts, name='favorites_list'),
    path('results', views.search_results, name='search_results'),
    path('livesearch/', views.live_search, name='live_search')
]
