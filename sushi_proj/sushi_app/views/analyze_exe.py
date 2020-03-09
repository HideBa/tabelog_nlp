from sushi_app.models.store_model import Store
# /sushi_proj/sushi_app/models/store_model.py
from sushi_app.models.review_model import Review
from sushi_app.models.sentiment_result_model import LunchSentimentResult, DinnerSentimentResult
from sushi_app.models.important_word_model import LunchImportantWords, DinnerImportantWords
from sushi_app.models.store_summary import DinnerStoreSummary, LunchStoreSummary
from sushi_app.models.dinner_summary_average import DinnerSummaryAverage
from sushi_app.models.score_history_model import TabelogHistory, RettyHistory
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect
from sushi_proj.settings import BASE_DIR, GCP_API_KEY
from get_important_word.analysis import Analyzer
from django.http import HttpResponse
from statistics import mean
import json
# from django.http import JsonResponse


class AnalyzeExe:
    def __init__(self, keyword_dict, adjective_dict, is_dinner):
        self.keyword_dict = keyword_dict
        self.adjective_dict = adjective_dict
        self.is_dinner = is_dinner

    def get_store_id_list(self):
        store_obj_list = Store.objects.all()
        store_id_list = []
        for store_obj in store_obj_list:
            store_id = store_obj.id
            store_id_list.append(store_id)
        return store_id_list

    def implement_all(self, store_id_list):
        for store_id in store_id_list:
            self.get_important_word(store_id, self.is_dinner)
            self.get_sentiment_result(store_id, self.is_dinner)
            self.get_posinega(store_id, self.is_dinner)
        self.get_summary_average(self.is_dinner, self.keyword_dict)
        self.update_growth_rate()

    def get_important_word(self, store_id, is_dinner):
        # decide dinner or lunch
        if is_dinner:
            # delete old data
            DinnerImportantWords.objects.filter(
                store__id__exact=store_id).delete()
        # 各店舗のレビューが入ったリストを格納
            dinner_reviews = Review.objects.filter(
                store__id__exact=store_id).filter(ld_id__exact=1)
            dinner_reviews_list = []
            for dinner_review in dinner_reviews:
                review_content = dinner_review.review
                dinner_reviews_list.append(review_content)
            content = ''.join(dinner_reviews_list)
            analyzer = Analyzer()
            temp = analyzer.feature_analysis_adjective(
                content, self.keyword_dict, self.adjective_dict)
            store = get_object_or_404(Store, id=store_id)
            for t in temp:
                try:
                    max_id = DinnerImportantWords.objects.latest('id').id
                except ObjectDoesNotExist:
                    max_id = 'DI00000'

                dinner_important_words_id = 'DI' + \
                    (str(int(max_id[2:]) + 1).zfill(5))

                # 例：['赤酢', 0, ['強い', 0], ['あっさり', 0], ['すっぱい', 0]]
                key_words = t[0]
                key_words_nums = t[1]
                keyword_modifier1 = t[2]
                keyword_modifier2 = t[3]
                if len(t) > 4:
                    keyword_modifier3 = t[4]
                else:
                    keyword_modifier3 = []
                DinnerImportantWords.objects.create(
                    id=dinner_important_words_id,
                    store=store,
                    key_words=key_words,
                    key_words_nums=key_words_nums,
                    keyword_modifier1=keyword_modifier1,
                    keyword_modifier2=keyword_modifier2,
                    keyword_modifier3=keyword_modifier3)
        else:
            LunchImportantWords.objects.all().delete()
            lunch_reviews = Review.objects.filter(
                store__id__exact=store_id).filter(ld_id__exact=0)
            lunch_reviews_list = []
            for lunch_review in lunch_reviews:
                temp = lunch_review.review
                lunch_reviews_list.append(temp)
            content = ''.join(lunch_reviews_list)
            analyzer = Analyzer()
            temp = analyzer.feature_analysis_adjective(
                content, self.keyword_dict)
            store = get_object_or_404(Store, id=store_id)
            for t in temp:
                try:
                    max_id = LunchImportantWords.objects.latest('id').id
                except ObjectDoesNotExist:
                    max_id = 'DI00000'

                lunch_important_words_id = 'DI' + \
                    (str(int(max_id[2:]) + 1).zfill(5))

                # 例：['赤酢', 0, ['強い', 0], ['あっさり', 0], ['すっぱい', 0]]
                key_words = t[0]
                key_words_nums = t[1]
                keyword_modifier1 = t[2]
                keyword_modifier2 = t[3]
                keyword_modifier3 = t[4]
                LunchImportantWords.objects.create(
                    id=lunch_important_words_id,
                    store=store,
                    key_words=key_words,
                    key_words_nums=key_words_nums,
                    keyword_modifier1=keyword_modifier1,
                    keyword_modifier2=keyword_modifier2,
                    keyword_modifier3=keyword_modifier3)

                # return render(self, 'sushi_app/sample.html', {'temp': temp})

                # 感情値を取得

    def get_sentiment_result(self, store_id, is_dinner):
        if is_dinner:
            dinner_reviews = Review.objects.filter(
                store__id__exact=store_id).filter(
                ld_id__exact=1)  # review object
            store = get_object_or_404(Store, id=store_id)  # ストアオブジェクト
            # import api key from settings
            key = GCP_API_KEY
            analyzer = Analyzer()
            gcp_nums = 0
            for dinner_review in dinner_reviews:
                if not dinner_review.is_new:
                    continue
                text = dinner_review.review
                sentiment_result = analyzer.gcp_analyzer(text, key)
                gcp_nums += 1
                print("gcp nums === " + str(gcp_nums))
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
                    DinnerSentimentResult.objects.create(
                        id=dinner_sentiment_result_id,
                        sentense=sentense,
                        sentiment=sentiment,
                        magnitude=magnitude,
                        review=review,
                        store=store)
                dinner_review.is_new = False
                dinner_review.save()
        # return HttpResponse('hello')
        else:
            lunch_reviews = Review.objects.filter(
                store__id__exact=store_id).filter(
                ld_id__exact=0)  # review object
            store = get_object_or_404(Store, id=store_id)  # ストアオブジェクト
            key = GCP_API_KEY
            analyzer = Analyzer()
            for lunch_review in lunch_reviews:
                text = lunch_review.review
                sentiment_result = analyzer.gcp_analyzer(text, key)
                for elem in sentiment_result:
                    try:
                        max_id = LunchSentimentResult.objects.latest('id').id
                    except ObjectDoesNotExist:
                        max_id = 'DSR0000000000'
                    lunch_sentiment_result_id = 'DSR' + \
                        (str(int(max_id[3:]) + 1).zfill(10))
                    sentense = elem[0]
                    magnitude = elem[1]
                    sentiment = elem[2]
                    review = lunch_review
                    LunchSentimentResult.objects.create(
                        id=lunch_sentiment_result_id,
                        sentense=sentense,
                        sentiment=sentiment,
                        magnitude=magnitude,
                        review=review,
                        store=store)

    # 以下でポジネガを取得

    def get_posinega(self, store_id, is_dinner):
        store = get_object_or_404(Store, id=store_id)
        if is_dinner:
            # delete old data
            DinnerStoreSummary.objects.filter(
                store__id__exact=store_id).delete()
            sentiment_result_objects = DinnerSentimentResult.objects.filter(
                store__id__exact=store_id)
            # (ex):[["まぐろが美味しいです", 0.3, 0.7], ["hoge", 0.3, 0.5]]
            parse_list = []
            for sentiment_result_object in sentiment_result_objects:
                text = sentiment_result_object.sentense
                sentiment = sentiment_result_object.sentiment
                magnitude = sentiment_result_object.magnitude
                sentiment_list = [text, magnitude, sentiment]
                parse_list.append(sentiment_list)
            analyzer = Analyzer()
            # ["まぐろ":[["うまい", 0.2, 0.5]["くさい", 0.5, -0.2]]
            posi_nega_result, sentiment_dic = analyzer.get_posinega_adjective(
                parse_list, self.keyword_dict, self.adjective_dict)
        #  {'赤酢': [['強い', 0.0, 0.0], ['あっさり', 0.0, 0.0], ['すっぱい', 0.0, 0.0]], '握り': [['大きい', 0.48999999999999994, 0.0], ['小さい', 0.0, 0.0], ['創作', 0.0, 0.0]], 'シャリ': [['大きい', 0.0, 0.0], ['小さい', 0.0, 0.0], ['パラパラ', 0.0, 0.0], ['塩気', 0.0, 0.0], ['甘い', 0.0, 0.0], ['熟成', 0.0, 0.0]]})
        #    {'赤酢': [0.4, 0.4], }
            for keyword in posi_nega_result:
                try:
                    max_id = DinnerStoreSummary.objects.latest('id').id
                except ObjectDoesNotExist:
                    max_id = 'DSS0000000000'
                dinner_store_summary_id = 'DSS' + \
                    (str(int(max_id[3:]) + 1).zfill(10))
                keyword_sentiment = sentiment_dic[keyword]
                # [['強い', 0.0, 0.0], ['あっさり', 0.0, 0.0], ['すっぱい', 0.0, 0.0]]
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
                DinnerStoreSummary.objects.create(
                    id=dinner_store_summary_id,
                    store=store,
                    keyword=keyword,
                    keyword_sentiment=keyword_sentiment,
                    keyword_modifier1=keyword_modifier1,
                    keyword_modifier2=keyword_modifier2,
                    keyword_modifier3=keyword_modifier3,
                    keyword_modifier4=keyword_modifier4,
                    keyword_modifier5=keyword_modifier5,
                    keyword_modifier6=keyword_modifier6)
        else:
            sentiment_result_objects = LunchSentimentResult.objects.filter(
                store__id__exact=store_id)
            # (ex):[["まぐろが美味しいです", 0.3, 0.7], ["hoge", 0.3, 0.5]]
            parse_list = []
            for sentiment_result_object in sentiment_result_objects:
                text = sentiment_result_object.sentense
                sentiment = sentiment_result_object.sentiment
                magnitude = sentiment_result_object.magnitude
                sentiment_list = [text, magnitude, sentiment]
                parse_list.append(sentiment_list)
            analyzer = Analyzer()
            # ["まぐろ":[["うまい", 0.2, 0.5]["くさい", 0.5, -0.2]]
            posi_nega_result, sentiment_dic = analyzer.get_posinega(
                parse_list, self.keyword_dict)  # {("まぐろ", "おいしい"): posi_point}
        #  {'赤酢': [['強い', 0.0, 0.0], ['あっさり', 0.0, 0.0], ['すっぱい', 0.0, 0.0]], '握り': [['大きい', 0.48999999999999994, 0.0], ['小さい', 0.0, 0.0], ['創作', 0.0, 0.0]], 'シャリ': [['大きい', 0.0, 0.0], ['小さい', 0.0, 0.0], ['パラパラ', 0.0, 0.0], ['塩気', 0.0, 0.0], ['甘い', 0.0, 0.0], ['熟成', 0.0, 0.0]]})
            for keyword in posi_nega_result:
                try:
                    max_id = LunchStoreSummary.objects.latest('id').id
                except ObjectDoesNotExist:
                    max_id = 'DSS0000000000'
                lunch_store_id = 'DSS' + \
                    (str(int(max_id[3:]) + 1).zfill(10))
                # 赤酢
                keyword_sentiment = sentiment_dic[keyword]
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
                LunchStoreSummary.objects.create(
                    id=lunch_store_id,
                    store=store,
                    keyword=keyword,
                    keyword_sentiment=keyword_sentiment,
                    keyword_modifier1=keyword_modifier1,
                    keyword_modifier2=keyword_modifier2,
                    keyword_modifier3=keyword_modifier3,
                    keyword_modifier4=keyword_modifier4,
                    keyword_modifier5=keyword_modifier5,
                    keyword_modifier6=keyword_modifier6)

    def get_summary_average(self, is_dinner, json_file):
        if is_dinner:
            if DinnerSummaryAverage.objects.all():
                DinnerSummaryAverage.objects.all().delete()
            with open(json_file, encoding='utf-8') as f:
                json_data = json.load(f)
                keywords = json_data['all_jiku']['all_jiku_list']
            for keyword in keywords:
                summaries = DinnerStoreSummary.objects.filter(
                    keyword__exact=keyword).all()
                posi_score_list = [float(summary.keyword_sentiment[0])
                                   for summary in summaries]
                if posi_score_list:
                    score_ave = mean(posi_score_list)
                else:
                    score_ave = 0.0
                try:
                    max_id = DinnerSummaryAverage.objects.latest('id').id
                except ObjectDoesNotExist:
                    max_id = 'DSA0000000'
                id = 'DSA' + \
                    (str(int(max_id[3:]) + 1).zfill(7))
                DinnerSummaryAverage.objects.create(
                    id=id, keyword=keyword, keyword_sentiment_ave_score=score_ave)

    def update_growth_rate(self):
        store_list = Store.objects.all()
        for store_obj in store_list:
            latest_tabelog_score = TabelogHistory.objects.filter(
                store__id__exact=store_obj.id).order_by('-nth').all()
            if latest_tabelog_score:
                growth_rate = (
                    (latest_tabelog_score[0].score - latest_tabelog_score[1].score) / latest_tabelog_score[1].score) * 100
                store_obj.tabelog_growth_rate = growth_rate
            latest_retty_score = RettyHistory.objects.filter(
                store__id__exact=store_obj.id).order_by('-nth').all()
            if latest_retty_score:
                growth_rate = (
                    (latest_retty_score[0].score - latest_retty_score[1].score) / latest_retty_score[1].score) * 100
                store_obj.retty_growth_rate = growth_rate
            store_obj.save()


def implement_all_process(request):
    keyword_file = BASE_DIR + '/analyze_files/dictionary.json'
    adjective_file = BASE_DIR + '/analyze_files/adjective.json'
    analyze_implement = AnalyzeExe(
        keyword_file, adjective_file, is_dinner=True)
    store_id_list = analyze_implement.get_store_id_list()
    analyze_implement.implement_all(store_id_list)
    return redirect('show_top_page')
