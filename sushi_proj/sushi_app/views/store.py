from django.shortcuts import render, get_object_or_404, redirect
from sushi_proj.settings import BASE_DIR
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.core.paginator import Paginator
from sushi_app.models.store_model import Store
from sushi_app.models.review_model import Review
from sushi_app.models.store_summary import DinnerStoreSummary
from sushi_app.models.score_history_model import TabelogHistory
from get_important_word.analysis import Analyzer
import json
import math
from .get_average import get_keyword_average
from .get_gender_popular import get_gender_rate, get_gender_ave

SAMPLE_STORE_LIST = {
    1: 'aozora',
    2: 'hatsune',
    3: 'imamura',
    4: 'kiyoda',
    5: 'mitani',
    6: 'sawada',
    7: 'sushiichi',
    8: 'sushitsuu'
}


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
    review_length = len(Review.objects.filter(store__id__exact=store_id))
    gender_ave_score_list = get_gender_ave(store)
    summaries = DinnerStoreSummary.objects.filter(store__id__exact=store_id)
    summary_list = []
    for summary in summaries:
        keyword = summary.keyword
        keyword_sentiment = summary.keyword_sentiment
        keyword_modifier1 = summary.keyword_modifier1
        keyword_modifier2 = summary.keyword_modifier2
        keyword_modifier3 = summary.keyword_modifier3
        keyword_modifier4 = summary.keyword_modifier4
        keyword_modifier5 = summary.keyword_modifier5
        keyword_modifier6 = summary.keyword_modifier6
        keyword_modifiers = [
            keyword_modifier1,
            keyword_modifier2,
            keyword_modifier3,
            keyword_modifier4,
            keyword_modifier5,
            keyword_modifier6]
        summary_list.append(
            [keyword, [keyword_sentiment, keyword_modifiers]])
    sorted_summary_list = sorted(
        summary_list, reverse=True,
        key=lambda obj: obj[1][0][0])
    #  [['握り', [3.33, 3.45] [['大きい', '0.8099999999999999', '0.0'], ['小さい', '0.9700000000000001', '0.6400000000000001'], ['創作', '1.55', '0.0'], [], [], []]]],
    # radar chart ------------------------
    chart_score_list = []
    chart_labels = []
    chart_store_ave_list = []
    sliced_summary_list = sorted_summary_list[:5]
    for sorted_summary in sliced_summary_list:
        score = float(sorted_summary[1][0][0])
        adj = sorted_summary[0]
        ave_score = get_keyword_average(adj)
        chart_store_ave_list.append(ave_score)
        chart_labels.append(str(adj))
        chart_score_list.append(score)
    chart_store_name = store.store_name
    chart_data = chart_score_list
    max_scale = math.ceil(max(chart_score_list))
    min_scale = math.floor(min(chart_score_list))
    radar_json_data = json.dumps({
        'type': 'radar',
        'data': {
            'labels': chart_labels,
            'datasets': [
                {
                    'label': chart_store_name,
                    'data': chart_data,
                    'backgroundColor': 'rgba(255, 99, 132, 0.6)',
                    'borderColor': 'rgba(255, 99, 132, 0.9)',
                    'pointBackgroundColor': 'rgba(255, 99, 132, 0.9)',
                    'pointBorderColor': 'rgba(255, 99, 132, 1)',
                    'borderWidth': 3,
                    'pointRadius': 3,
                }, {
                    'label': '他店平均',
                    'data': chart_store_ave_list,
                    'backgroundColor': 'rgba(0, 0, 255, 0.6)',
                    'borderColor': 'rgba(0, 0, 255, 0.9)',
                    'pointBackgroundColor': 'rgba(0, 0, 255, 0.9)',
                    'pointBorderColor': 'rgba(0, 0, 255, 1)',
                    'borderWidth': 3,
                    'pointRadius': 3,
                }
            ]
        },
        'options': {
            'animation': {'duration': 2000},
            # 'legend': {'display': false},
            'scale': {
                'ticks': {
                    'min': min_scale,
                    'max': max_scale,
                    'stepSize': 1,
                    'backdropColor': 'rgba(255, 255, 255, 0)',
                }
            }
        }
    })
# radar chart --------------------
# line chart -------------------
    tabelog_history_list = TabelogHistory.objects.filter(
        store__id__exact=store_id)
    sorted_tabelog_history_list = sorted(
        tabelog_history_list,
        reverse=True,
        key=lambda obj: obj.nth)
    chart_line_data = [
        tabelog_history.score for tabelog_history in sorted_tabelog_history_list]
    chart_line_labels = [
        tabelog_history.nth for tabelog_history in sorted_tabelog_history_list]
    line_json_data = json.dumps({
        'type': 'line',
        'data': {
            'labels': chart_line_labels,
            'datasets': [
                {
                    'label': 'tabelog 変化',
                    'data': chart_line_data,
                    'borderColor': "rgba(255,0,0,1)",
                    'backgroundColor': "rgba(0,0,0,0)"
                },
            ],
        },
        'options': {
            'title': {
                'text': 'tabelog_change'
            },
            'scales': {
                'yAxes': [{
                    'ticks': {
                        'suggestedMax': 5,
                        'suggestedMin': 0,
                        'stepSize': 1,
                    }
                }]
            },
        }
    })
    # line chart ----------------------
    # pie chart -------------------
    chart_pie_data = get_gender_rate(True, store_id)
    pie_json_data = json.dumps({
        'type': 'pie',
        'data': {
            'labels': ["男性", "女性", "不明"],
            'datasets': [{
                'backgroundColor': [
                    "rgba(0, 0, 255, 0.9)",
                    "rgba(255, 99, 132, 0.9)",
                    "#58A27C",
                ],
                'data': chart_pie_data
            }]
        },
        'options': {
            'title': {
                # 'display': True,
                'text': '血液型 割合'
            }
        }})

    try:
        page = int(request.GET.get('from_page'))
    except BaseException:
        page = 1
    return render(request,
                  'sushi_app/store_detail.html',
                  {'review_length': review_length,
                   'gender_ave_score_list': gender_ave_score_list,
                   'store': store,
                   'sorted_summary_list': sorted_summary_list,
                   'page': page,
                   'radar_json_data': radar_json_data,
                   'line_json_data': line_json_data,
                   'pie_json_data': pie_json_data,
                   })


def save_review(request):
    for key, value in SAMPLE_STORE_LIST.items():
        store = Store.objects.get(id=key)
        analyzer = Analyzer()
        csv_path = BASE_DIR + \
            "/sample_files/pretest_{}_dinner.csv".format(value)
        reviews = analyzer.read_csv(csv_path)
        for review in reviews:
            try:
                max_id = Review.objects.latest('id').id
            except ObjectDoesNotExist:
                max_id = 1
            dinner_review_id = max_id + 1
            Review.objects.create(
                id=dinner_review_id,
                review=review,
                store=store,
                ld_id=1,
                is_new=True)
    # ここからしたの処理はユーザーの応答に応じてレスポンスするものではなく、システムとして常時稼働し、実行される。
    return redirect('show_top_page')


def keyword_sort(request, keyword, site):
    if request.POST:
        site = request.POST.get('sort')

    stores = Store.objects.filter(dinnerstoresummary__keyword=keyword).all(
    ).order_by("dinnerstoresummary__keyword_sentiment")[:30]

    if(site == "tabelog"):
        sorted_stores = sorted(stores, key=lambda store: store.tabelog_score)
    elif(site == "retty"):
        sorted_stores = sorted(stores, key=lambda store: store.retty_score)
    store_summary_list = []
    # ex), [[store_obj], [dinner_summary_obj]]
    for store in sorted_stores:
        list = [
            store, DinnerStoreSummary.objects.filter(
                store__id__exact=store.id).filter(
                keyword=keyword).get()]
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


def get_top_growth_rate(request):
    tabelog_store_list = Store.objects.all().order_by('tabelog_growth_rate').reverse()
    retty_store_list = Store.objects.all().order_by('retty_growth_rate').reverse()

    return render(request,
                  'sushi_app/growth_rate_store_list.html',
                  {'tabelog_store_list': tabelog_store_list,
                   'retty_score_list': retty_store_list})


def area_search(request):
    if request.GET.get('prefecture'):
        print("area wur^^^^^^^^^")
        print("request.GET == ")
        query_string = request.GET.get('prefecture')
        print("value ==== " + query_string)
        if Store.objects.filter(
                Q(address__icontains=query_string)).exists():
            searched_store_list = Store.objects.filter(
                Q(address__icontains=query_string)).all()
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
