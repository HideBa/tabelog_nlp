from django.urls import path
from sushi_app.views import store

app_name = 'sushi_app'

urlpatterns = [
    path(
        'store',
        store.list_view,
        name='store_list'),
    path(
        'store/<slug:store_id>',
        store.detail_view,
        name='store_detail'),
    path(
        'store/<slug:store_id>/<slug:lunch_review_id>',
        store.review_lunch_view,
        name='lunch_review_detail'),
    path(
        'store/<slug:store_id>/<slug:dinner_review_id>',
        store.review_dinner_view,
        name='dinner_review_detail'),
    path(
        'sample/<slug:store_id>',
        store.get_important_word,
        name='get_important_word'),
    path(
        'sentiment/<slug:store_id>',
        store.get_sentiment_result,
        name='get_sentiment_result'),
    path('posinega/<slug:store_id>', store.get_posinega, name='get_posinega')]
