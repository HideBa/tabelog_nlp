from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sushi_proj.settings import BASE_DIR
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from django.core.paginator import Paginator
# from sushi_app.models import Store, LunchReview
from sushi_app.models.store_model import Store
from sushi_app.models.review_model import LunchReview, DinnerReview
from sushi_app.models.sentiment_result_model import LunchSentimentResult, DinnerSentimentResult
from sushi_app.models.important_word_model import LunchImportantWords, DinnerImportantWords
from sushi_app.models.store_summary import DinnerStoreSummary, LunchStoreSummary
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
    summaries = DinnerStoreSummary.objects.filter(store__id__exact=store_id)
    print("summary obj ==== " + str(summaries))
    summary_list = []
    for summary in summaries:
        keyword = summary.keyword
        keyword_modifier1 = summary.keyword_modifier1
        keyword_modifier2 = summary.keyword_modifier2
        keyword_modifier3 = summary.keyword_modifier3
        keyword_modifier4 = summary.keyword_modifier4
        keyword_modifier5 = summary.keyword_modifier5
        keyword_modifier6 = summary.keyword_modifier6
        summary_list.append([keyword,
                             keyword_modifier1,
                             keyword_modifier2,
                             keyword_modifier3,
                             keyword_modifier4,
                             keyword_modifier5,
                             keyword_modifier6])
    print("summary list ==== " + str(summary_list))
    sorted_summary_list = sorted(
        summary_list, reverse=True,
        key=lambda obj: obj[1][1])

    # lunch_reviews = LunchReview.objects.filter(store__id__exact=store_id)
    # dinner_reviews = DinnerReview.objects.filter(store__id__exact=store_id)
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
                   'summary_list': sorted_summary_list,
                   'page': page,
                   #    'lunch_reviews': lunch_reviews,
                   #    'dinner_reviews': dinner_reviews
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


def save_review(request, store_id):
    store = Store.objects.get(id=store_id)
    analyzer = Analyzer()
    # csv_path = BASE_DIR + "/sample_files/pretest_aozora_dinner.csv"
    # csv_path = BASE_DIR + "/sample_files/pretest_sushitsuu_dinner.csv"
    csv_path = BASE_DIR + "/sample_files/pretest_mitani_dinner.csv"
    reviews = analyzer.read_csv(csv_path)
    for review in reviews:
        try:
            max_id = DinnerReview.objects.latest('id').id
        except ObjectDoesNotExist:
            max_id = 'dr00000000'
        dinner_review_id = 'dr' + (str(int(max_id[2:]) + 1).zfill(8))
        new_data = DinnerReview.objects.create(
            id=dinner_review_id, content=review, store=store)
        # ここからしたの処理はユーザーの応答に応じてレスポンスするものではなく、システムとして常時稼働し、実行される。
    return HttpResponse("save")


def keyword_sort(request, keyword, site):
    if request.POST:
        print("postpostpost")
        site = request.POST.get('sort')
        print("value ==== " + request.POST.get('sort'))

    stores = Store.objects.filter(dinnerstoresummary__keyword=keyword).all(
    ).order_by("dinnerstoresummary__keyword_sentiment")[:30]
    print("stores ==== " + str(stores))

    if(site == "tabelog"):
        sorted_stores = sorted(stores, key=lambda store: store.tabelog_score)
        print("sorted stores === " + str(sorted_stores))
    elif(site == "retty"):
        sorted_stores = sorted(stores, key=lambda store: store.retty_score)
        print("sorted stores === " + str(sorted_stores))
    store_summary_list = []
    # ex), [[store_obj], [dinner_summary_obj]]
    for store in sorted_stores:
        list = [
            store, DinnerStoreSummary.objects.filter(
                store__id__exact=store.id).filter(
                keyword=keyword).get()]
        print("store summary === " + str(list))
        store_summary_list.append(list)
    return render(request, 'sushi_app/sorted_store_list.html',
                  {'store_summary_list': store_summary_list, 'keyword': keyword})


def store_search(request):
    if request.GET.get('search'):
        query_string = request.GET.get('search')
        if Store.objects.filter(
                Q(store_name__icontains=query_string)).exists():
            searched_store_list = Store.objects.filter(
                Q(store_name__icontains=query_string)).all()
            message = ""
        else:
            searched_store_list = []
            message = "no result"

        paginator = Paginator(searched_store_list, 20)  # ページ当たり20個表示

        try:
            page = int(request.GET.get('page'))
        except BaseException:
            page = 1

        stores = paginator.get_page(page)
        return render(request,
                      'sushi_app/store_list.html',
                      {'stores': stores,
                       'page': page,
                       'message': message,
                       'last_page': paginator.num_pages})
    else:
        return redirect('show_top_page')
# .order_by(str(site) + "_score")
