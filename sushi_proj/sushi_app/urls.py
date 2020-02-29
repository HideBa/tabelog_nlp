from django.urls import path
from sushi_app.views import store, analyze_exe, get_gender_popular

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
    path('keyword-sort/<str:keyword>/<slug:site>',
         store.keyword_sort, name='keyword_sort'),
    path('store-search', store.store_search, name='store_search'),
    path('area-search', store.area_search, name='area_search'),

    path('exe', analyze_exe.implement_all_process, name="exe"),
    path('top-growth-rate', store.get_top_growth_rate, name="top_growth_rate"),
    path(
        'gender-rate/is_dinner=<slug:is_dinner>/is_male=<slug:is_male>',
        get_gender_popular.get_popular_store,
        name="get_gender_popular"),
]
