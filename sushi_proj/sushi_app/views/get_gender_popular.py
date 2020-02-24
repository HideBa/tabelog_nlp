from sushi_proj.settings import BASE_DIR
from django.core.exceptions import ObjectDoesNotExist
from sushi_app.models.store_model import Store
from sushi_app.models.review_model import LunchReview, DinnerReview
# from sushi_app.models.sentiment_result_model import LunchSentimentResult, DinnerSentimentResult
# from sushi_app.models.important_word_model import LunchImportantWords, DinnerImportantWords
# from sushi_app.models.store_summary import DinnerStoreSummary, LunchStoreSummary
# from sushi_app.models.dinner_summary_average import DinnerSummaryAverage
from django.http import HttpResponse, Http404, JsonResponse


def get_popular_store(is_dinner):
    store_list = Store.objects.all()
    if is_dinner:
        for store in store_list:
            all_reviews = DinnerReview.objects.filter(store_id__exact=store.id)
            # male_reviews = DinnerReview.objects.filter(user_sex__exact=1).all()
            # female_reviews = DinnerReview.objects.filter(user_sex_exact=2).all()
            # unknown_review = DinnerReview.objects.filter(user_sex__exact=0).all()
            male_reviews_list = [
                review for review in all_reviews if review.user_sex == 1]
            female_reviews_list = [
                review for review in all_reviews if review.user_sex == 2]
            unknown_reviews_list = [
                review for review in all_reviews if review.user_sex == 0]
            print("review_num== " + str(len(all_reviews)))
            print("male review_num==" + str(len(male_reviews_list)))
            male_rate = len(male_reviews_list) / len(all_reviews)
            female_rate = len(female_reviews_list) / len(all_reviews)
            if male_reviews_list:
                male_score_ave = sum(
                    male_review.score for male_review in male_reviews_list) / len(male_reviews_list)
            else:
                male_score_ave = 0
            if female_reviews_list:
                female_score_ave = sum(
                    female_review.score for female_review in female_reviews_list) / len(male_reviews_list)
            else:
                female_score_ave = 0
            print("male_rate === " + str(male_rate))
            print("male ave === " + str(male_score_ave))
    return HttpResponse("male rate")
