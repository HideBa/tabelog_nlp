from sushi_app.models.store_model import Store
# /sushi_proj/sushi_app/models/store_model.py
from sushi_app.models.review_model import LunchReview, DinnerReview
from sushi_app.models.sentiment_result_model import LunchSentimentResult, DinnerSentimentResult
from sushi_app.models.important_word_model import LunchImportantWords, DinnerImportantWords
from sushi_app.models.store_summary import DinnerStoreSummary, LunchStoreSummary
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from sushi_proj.settings import BASE_DIR
from get_important_word.analysis import Analyzer
from django.http import HttpResponse
# from django.http import JsonResponse


class AnalyzeExe:
    def __init__(self, keyword_dict, is_dinner):
        self.keyword_dict = keyword_dict
        self.is_dinner = is_dinner

    def get_store_id_list(self):
        store_obj_list = Store.objects.all()
        print("store obj list === " + str(store_obj_list))
        store_id_list = []
        for store_obj in store_obj_list:
            store_id = store_obj.id
            store_id_list.append(store_id)
            print("store id === " + str(store_id))
        return store_id_list

    def implement_all(self, store_id_list):
        for store_id in store_id_list:
            self.get_important_word(store_id, self.is_dinner)
            # self.get_sentiment_result(store_id, self.is_dinner)
            # self.get_posinega(store_id, self.is_dinner)

    def get_important_word(self, store_id, is_dinner):
        # decide dinner or lunch
        if is_dinner:
            # delete old data
            DinnerImportantWords.objects.all().delete()
        # 各店舗のレビューが入ったリストを格納
            dinner_reviews = DinnerReview.objects.filter(
                store__id__exact=store_id)
            dinner_reviews_list = []
            for dinner_review in dinner_reviews:
                review_content = dinner_review.content
                dinner_reviews_list.append(review_content)
            content = ''.join(dinner_reviews_list)
            analyzer = Analyzer()
            temp = analyzer.feature_analysis(content, self.keyword_dict)
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
        else:
            LunchImportantWords.objects.all().delete()
            lunch_reviews = LunchReview.objects.filter(
                store__id__exact=store_id)
            lunch_reviews_list = []
            for lunch_review in lunch_reviews:
                temp = lunch_review.content
                lunch_reviews_list.append(temp)
            content = ''.join(lunch_reviews_list)
            analyzer = Analyzer()
            temp = analyzer.feature_analysis(content, self.keyword_dict)
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
                new_data = LunchImportantWords.objects.create(
                    id=lunch_important_words_id,
                    store=store,
                    key_words=key_words,
                    key_words_nums=key_words_nums,
                    keyword_modifier1=keyword_modifier1,
                    keyword_modifier2=keyword_modifier2,
                    keyword_modifier3=keyword_modifier3)
                print("saved data ==== " + str(new_data))

                # return render(self, 'sushi_app/sample.html', {'temp': temp})

                # 感情値を取得

    def get_sentiment_result(self, store_id, is_dinner):
        if is_dinner:
            dinner_reviews = DinnerReview.objects.filter(
                store__id__exact=store_id)  # review object
            store = get_object_or_404(Store, id=store_id)  # ストアオブジェクト
            key = 'AIzaSyCIl8F1e8D7mLIs0jhgp4Z3U4KWI76pcvE'
            analyzer = Analyzer()
            gcp_nums = 0
            for dinner_review in dinner_reviews:
                text = dinner_review.content
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
                    new_data = DinnerSentimentResult.objects.create(
                        id=dinner_sentiment_result_id,
                        sentense=sentense,
                        sentiment=sentiment,
                        magnitude=magnitude,
                        review=review,
                        store=store)
                    print("new data === " + str(new_data))
        # return HttpResponse('hello')
        else:
            lunch_reviews = LunchReview.objects.filter(
                store__id__exact=store_id)  # review object
            store = get_object_or_404(Store, id=store_id)  # ストアオブジェクト
            key = 'AIzaSyCIl8F1e8D7mLIs0jhgp4Z3U4KWI76pcvE'
            analyzer = Analyzer()
            for lunch_review in lunch_reviews:
                text = lunch_review.content
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
                    new_data = LunchSentimentResult.objects.create(
                        id=lunch_sentiment_result_id,
                        sentense=sentense,
                        sentiment=sentiment,
                        magnitude=magnitude,
                        review=review,
                        store=store)
                    print("new data === " + str(new_data))

    # 以下でポジネガを取得

    def get_posinega(self, store_id, is_dinner):
        store = get_object_or_404(Store, id=store_id)
        if is_dinner:
            sentiment_result_objects = DinnerSentimentResult.objects.filter(
                store__id__exact=store_id)
            # json_file = BASE_DIR + '/analyze_files/dictionary.json'
            # (ex):[["まぐろが美味しいです", 0.3, 0.7], ["hoge", 0.3, 0.5]]
            parse_list = []
            for sentiment_result_object in sentiment_result_objects:
                text = sentiment_result_object.sentense
                sentiment = sentiment_result_object.sentiment
                magnitude = sentiment_result_object.magnitude
                sentiment_list = [text, magnitude, sentiment]
                print("parse_list === " + str(sentiment_list))
                parse_list.append(sentiment_list)
            analyzer = Analyzer()
            # ["まぐろ":[["うまい", 0.2, 0.5]["くさい", 0.5, -0.2]]
            posi_nega_result, sentiment_dic = analyzer.get_posinega(
                parse_list, self.keyword_dict)  # {("まぐろ", "おいしい"): posi_point}
        #  {'赤酢': [['強い', 0.0, 0.0], ['あっさり', 0.0, 0.0], ['すっぱい', 0.0, 0.0]], '握り': [['大きい', 0.48999999999999994, 0.0], ['小さい', 0.0, 0.0], ['創作', 0.0, 0.0]], 'シャリ': [['大きい', 0.0, 0.0], ['小さい', 0.0, 0.0], ['パラパラ', 0.0, 0.0], ['塩気', 0.0, 0.0], ['甘い', 0.0, 0.0], ['熟成', 0.0, 0.0]]})
        #    {'赤酢': [0.4, 0.4], }
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
                new_data = DinnerStoreSummary.objects.create(
                    id=dinner_store_id,
                    store=store,
                    keyword=keyword,
                    keyword_sentiment=keyword_sentiment,
                    keyword_modifier1=keyword_modifier1,
                    keyword_modifier2=keyword_modifier2,
                    keyword_modifier3=keyword_modifier3,
                    keyword_modifier4=keyword_modifier4,
                    keyword_modifier5=keyword_modifier5,
                    keyword_modifier6=keyword_modifier6)
                print("new data ===== " + str(new_data))
        else:
            sentiment_result_objects = LunchSentimentResult.objects.filter(
                store__id__exact=store_id)
            # json_file = BASE_DIR + '/analyze_files/dictionary.json'
            # (ex):[["まぐろが美味しいです", 0.3, 0.7], ["hoge", 0.3, 0.5]]
            parse_list = []
            for sentiment_result_object in sentiment_result_objects:
                text = sentiment_result_object.sentense
                sentiment = sentiment_result_object.sentiment
                magnitude = sentiment_result_object.magnitude
                sentiment_list = [text, magnitude, sentiment]
                print("parse_list === " + str(sentiment_list))
                parse_list.append(sentiment_list)
            analyzer = Analyzer()
            # ["まぐろ":[["うまい", 0.2, 0.5]["くさい", 0.5, -0.2]]
            posi_nega_result, sentiment_dic = analyzer.get_posinega(
                parse_list, self.keyword_dict)  # {("まぐろ", "おいしい"): posi_point}
        #  {'赤酢': [['強い', 0.0, 0.0], ['あっさり', 0.0, 0.0], ['すっぱい', 0.0, 0.0]], '握り': [['大きい', 0.48999999999999994, 0.0], ['小さい', 0.0, 0.0], ['創作', 0.0, 0.0]], 'シャリ': [['大きい', 0.0, 0.0], ['小さい', 0.0, 0.0], ['パラパラ', 0.0, 0.0], ['塩気', 0.0, 0.0], ['甘い', 0.0, 0.0], ['熟成', 0.0, 0.0]]})
            print("====" + str(posi_nega_result))
            for keyword in posi_nega_result:
                try:
                    max_id = LunchStoreSummary.objects.latest('id').id
                except ObjectDoesNotExist:
                    max_id = 'DSS0000000000'
                lunch_store_id = 'DSS' + \
                    (str(int(max_id[3:]) + 1).zfill(10))
                print("keyword ==== " + str(keyword))
                # 赤酢
                keyword_sentiment = sentiment_dic[keyword]
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
                new_data = LunchStoreSummary.objects.create(
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
                print("new data ===== " + str(new_data))

        # return HttpResponse("god")
#     get_important_word()


def implement_all_process(request):
    print("base dir === " + BASE_DIR)
    json_file = BASE_DIR + '/analyze_files/dictionary.json'
    analyze_implement = AnalyzeExe(json_file, is_dinner=True)
    store_id_list = analyze_implement.get_store_id_list()
    analyze_implement.implement_all(store_id_list)
    return HttpResponse("done")
