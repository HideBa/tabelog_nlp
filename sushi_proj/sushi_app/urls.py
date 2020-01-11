from django.urls import path
from sushi_app.views import store

app_name = 'sushi_app'

urlpatterns = [
    path('store', store.list_view, name='store_list'),
]
