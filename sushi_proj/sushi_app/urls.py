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
    path(
        'store/<slug:store_id>/<slug:lunch_review_id>',
        store.review_lunch_view,
        name='lunch_review_detail'),
    path(
        'store/<slug:store_id>/<slug:dinner_review_id>',
        store.review_dinner_view,
        name='dinner_review_detail'),
    path('keyword-sort/<str:keyword>/<slug:site>',
         store.keyword_sort, name='keyword_sort'),
    path('store-search', store.store_search, name='store_search'),
    path('area-search', store.area_search, name='area_search'),
    # path('keyword-sort/<slug:keyword>/<slug:ranksite>',
    #      store.keyword_sort, name='keyword_sort')
    # path(
    #     'important/<slug:store_id>',
    #     store.get_important_word,
    #     name='get_important_word'),
    # path(
    #     'sentiment/<slug:store_id>',
    #     store.get_sentiment_result,
    #     name='get_sentiment_result'),
    # path('posinega/<slug:store_id>', store.get_posinega, name='get_posinega'),
    # path('savecsv/<slug:store_id>', store.save_review, name="save_review"),
    path('exe', analyze_exe.implement_all_process, name="exe"),
    path('top-growth-rate', store.get_top_growth_rate, name="top_growth_rate"),
    path(
        'gender-rate',
        get_gender_popular.get_popular_store,
        name="get_gender_popular"),
]
