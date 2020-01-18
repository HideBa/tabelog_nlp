from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sushi_proj.settings import BASE_DIR

from django.core.paginator import Paginator
# from sushi_app.models import Store, LunchReview
from sushi_app.models.store_model import Store
from sushi_app.models.review_model import LunchReview, DinnerReview
from sushi_app.models.important_word_model import LunchImportantWords, DinnerImportantWords
import random
from get_important_word.analysis import Analyzer


def list_view(request):
    store_list = Store.objects.all().order_by('-id')
    paginator = Paginator(store_list, 20)  # ページ当たり20個表示

    try:
        page = int(request.GET.get('page'))
    except BaseException:
        page = 1

    stores = paginator.get_page(page)
    return render(request,
                  'sushi_app/store_list.html',
                  {'stores': stores,
                   'page': page,
                   'last_page': paginator.num_pages})


def detail_view(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    lunch_reviews = LunchReview.objects.filter(store__id__exact=store_id)
    dinner_reviews = DinnerReview.objects.filter(store__id__exact=store_id)
    try:
        page = int(request.GET.get('from_page'))
    except BaseException:
        page = 1

    # try:
    #     lunch_review = LunchReview.objects.get(store_id=store_id)

    # except BaseException:
    #     current_score = -1

    return render(request,
                  'sushi_app/store_detail.html',
                  {'store': store,
                   'page': page,
                   'lunch_reviews': lunch_reviews,
                   'dinner_reviews': dinner_reviews
                   #    'current_score': current_score
                   })


def review_lunch_view(request, store_id, lunch_review_id):
    review = get_object_or_404(LunchReview, id=lunch_review_id)
    store = get_object_or_404(Store, id=store_id)
    try:
        page = int(request.GET.get('from_page'))
    except BaseException:
        page = 1

    return render(request, 'sushi_app/lunch_review_detail.html',
                  {'store': store, 'review': review, 'page': page})


def review_dinner_view(request, store_id, dinner_review_id):
    review = get_object_or_404(DinnerReview, id=dinner_review_id)
    store = get_object_or_404(Store, id=store_id)
    try:
        page = int(request.GET.get('from_page'))
    except BaseException:
        page = 1
    print("hello--------------")
    return render(request, 'sushi_app/dinner_review_detail.html',
                  {'store': store, 'review': review, 'page': page})


def get_important_word(request, store_id):
    # 各店舗のレビューが入ったリストを格納
    # json_file = 'sushi_proj/analyze_files/dictionary.json'
    print("base dir ===== " + str(BASE_DIR))
    json_file = BASE_DIR + '/analyze_files/dictionary.json'
    # json_file = '/Users/HideBa/python/tabelog_evolution/sushi_proj/analyze_files/dictionary.json'
    dinner_reviews = DinnerReview.objects.filter(store__id__exact=store_id)
    print("dinner_reviews ======= " + str(dinner_reviews))
    dinner_reviews_list = []
    for dinner_review in dinner_reviews:
        temp = dinner_review.content
        dinner_reviews_list.append(temp)
    print("dinner_list ====== " + str(dinner_reviews_list))
    content = ''.join(dinner_reviews_list)
    analyzer = Analyzer()
    temp = analyzer.feature_analysis(content, json_file)
    print("result=========" + str(temp))
    render(request, 'sushi_app/sample.html', {'temp': temp})


# if __name__ == 'main':
#     get_important_word()
