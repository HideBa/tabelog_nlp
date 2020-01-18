from django.urls import path
from sushi_app.views import store

app_name = 'sushi_app'

urlpatterns = [
    path('store', store.list_view, name='store_list'),
    path('store/<slug:store_id>', store.detail_view, name='store_detail'),
    path('store/<slug:store_id>/<slug:lunch_review_id>', store.review_lunch_view, name='review_detail')
]
