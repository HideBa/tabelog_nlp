from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from sushi_proj.settings import BASE_DIR
from django.core.exceptions import ObjectDoesNotExist

from django.core.paginator import Paginator
# from sushi_app.models import Store, LunchReview
from sushi_app.models.store_model import Store
from sushi_app.models.review_model import LunchReview, DinnerReview
from sushi_app.models.sentiment_result_model import LunchSentimentResult, DinnerSentimentResult
from sushi_app.models.important_word_model import LunchImportantWords, DinnerImportantWords
from sushi_app.models.store_summary import DinnerStoreSummary, LunchStoreSummary
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
                   'summary_list': summary_list,
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


def save_review(request, store_id):
    store = Store.objects.get(id=store_id)
    analyzer = Analyzer()
    csv_path = BASE_DIR + "/sample_files/pretest_aozora_dinner.csv"
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


def get_important_word(request, store_id):
    print("========")
    # 各店舗のレビューが入ったリストを格納
    print("base dir ===== " + str(BASE_DIR))
    json_file = BASE_DIR + '/analyze_files/dictionary.json'
    dinner_reviews = DinnerReview.objects.filter(store__id__exact=store_id)
    dinner_reviews_list = []
    for dinner_review in dinner_reviews:
        temp = dinner_review.content
        dinner_reviews_list.append(temp)
    content = ''.join(dinner_reviews_list)
    analyzer = Analyzer()
    temp = analyzer.feature_analysis(content, json_file)
    store = get_object_or_404(Store, id=store_id)
    for t in temp:
        try:
            max_id = DinnerImportantWords.objects.latest('id').id
        except ObjectDoesNotExist:
            max_id = 'DI00000'

        dinner_important_words_id = 'DI' + (str(int(max_id[2:]) + 1).zfill(5))

        # 例：['赤酢', 0, ['強い', 0], ['あっさり', 0], ['すっぱい', 0]]
        key_words = t[0]
        key_words_nums = t[1]
        keyword_modifier1 = t[2]
        keyword_modifier2 = t[3]
        keyword_modifier3 = t[4]
        new_data = DinnerImportantWords.objects.create(
            id=dinner_important_words_id,
            store=store,
            key_words=key_words,
            key_words_nums=key_words_nums,
            keyword_modifier1=keyword_modifier1,
            keyword_modifier2=keyword_modifier2,
            keyword_modifier3=keyword_modifier3)
        print("saved data ==== " + str(new_data))

    return render(request, 'sushi_app/sample.html', {'temp': temp})

# 感情値を取得


def get_sentiment_result(request, store_id):
    dinner_reviews = DinnerReview.objects.filter(
        store__id__exact=store_id)  # review object
    store = get_object_or_404(Store, id=store_id)  # ストアオブジェクト
    key = 'AIzaSyCIl8F1e8D7mLIs0jhgp4Z3U4KWI76pcvE'
    analyzer = Analyzer()
    for dinner_review in dinner_reviews:
        text = dinner_review.content
        sentiment_result = analyzer.gcp_analyzer(text, key)
        for elem in sentiment_result:
            try:
                max_id = DinnerSentimentResult.objects.latest('id').id
            except ObjectDoesNotExist:
                max_id = 'DSR0000000000'
            dinner_sentiment_result_id = 'DSR' + \
                (str(int(max_id[3:]) + 1).zfill(10))
            sentense = elem[0]
            magnitude = elem[1]
            sentiment = elem[2]
            review = dinner_review
            new_data = DinnerSentimentResult.objects.create(
                id=dinner_sentiment_result_id,
                sentense=sentense,
                sentiment=sentiment,
                magnitude=magnitude,
                review=review,
                store=store)
            print("new data === " + str(new_data))
    return HttpResponse('hello')

# 以下でポジネガを取得


def get_posinega(request, store_id):
    store = get_object_or_404(Store, id=store_id)
    sentiment_result_objects = DinnerSentimentResult.objects.filter(
        store__id__exact=store_id)
    json_file = BASE_DIR + '/analyze_files/dictionary.json'
    parse_list = []  # (ex):[["まぐろが美味しいです", 0.3, 0.7], ["hoge", 0.3, 0.5]]
    for sentiment_result_object in sentiment_result_objects:
        text = sentiment_result_object.sentense
        sentiment = sentiment_result_object.sentiment
        magnitude = sentiment_result_object.magnitude
        sentiment_list = [text, magnitude, sentiment]
        print("parse_list === " + str(sentiment_list))
        parse_list.append(sentiment_list)
    analyzer = Analyzer()
    # ["まぐろ":[["うまい", 0.2, 0.5]["くさい", 0.5, -0.2]]
    posi_nega_result = analyzer.get_posinega(
        parse_list, json_file)  # {("まぐろ", "おいしい"): posi_point}
#  {'赤酢': [['強い', 0.0, 0.0], ['あっさり', 0.0, 0.0], ['すっぱい', 0.0, 0.0]], '握り': [['大きい', 0.48999999999999994, 0.0], ['小さい', 0.0, 0.0], ['創作', 0.0, 0.0]], 'シャリ': [['大きい', 0.0, 0.0], ['小さい', 0.0, 0.0], ['パラパラ', 0.0, 0.0], ['塩気', 0.0, 0.0], ['甘い', 0.0, 0.0], ['熟成', 0.0, 0.0]]})
    print("====" + str(posi_nega_result))
    for keyword in posi_nega_result:
        try:
            max_id = DinnerStoreSummary.objects.latest('id').id
        except ObjectDoesNotExist:
            max_id = 'DSS0000000000'
        dinner_store_id = 'DSS' + \
            (str(int(max_id[3:]) + 1).zfill(10))
        print("keyword ==== " + str(keyword))
        # 赤酢
        print("modifier ===== " + str(posi_nega_result[keyword]))
        # [['強い', 0.0, 0.0], ['あっさり', 0.0, 0.0], ['すっぱい', 0.0, 0.0]]
        # for modifier_list in posi_nega_result[keyword]:
        if len(posi_nega_result[keyword]) >= 1:
            keyword_modifier1 = posi_nega_result[keyword][0]
        else:
            keyword_modifier1 = []
        if len(posi_nega_result[keyword]) >= 2:
            keyword_modifier2 = posi_nega_result[keyword][1]
        else:
            keyword_modifier2 = []
        if len(posi_nega_result[keyword]) >= 3:
            keyword_modifier3 = posi_nega_result[keyword][2]
        else:
            keyword_modifier3 = []
        if len(posi_nega_result[keyword]) >= 4:
            keyword_modifier4 = posi_nega_result[keyword][3]
        else:
            keyword_modifier4 = []
        if len(posi_nega_result[keyword]) >= 5:
            keyword_modifier5 = posi_nega_result[keyword][4]
        else:
            keyword_modifier5 = []
        if len(posi_nega_result[keyword]) >= 6:
            keyword_modifier6 = posi_nega_result[keyword][5]
        else:
            keyword_modifier6 = []
        new_data = DinnerStoreSummary.objects.create(
            id=dinner_store_id,
            store=store,
            keyword=keyword,
            keyword_modifier1=keyword_modifier1,
            keyword_modifier2=keyword_modifier2,
            keyword_modifier3=keyword_modifier3,
            keyword_modifier4=keyword_modifier4,
            keyword_modifier5=keyword_modifier5,
            keyword_modifier6=keyword_modifier6)
        print("new data ===== " + str(new_data))

    return HttpResponse("god")
    # if __name__ == 'main':
    #     get_important_word()
