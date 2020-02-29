from sushi_app.models.store_model import Store
from sushi_app.models.review_model import Review
from django.shortcuts import render


def get_popular_store(request, is_dinner, is_male):
    store_list = Store.objects.all()
    result_list = []
    if is_dinner:
        for store in store_list:
            result_list.append(get_gender_ave(store))
    if is_male:
        sorted_result_list = sorted(
            result_list,
            reverse=True,
            key=lambda result: result[1])
    else:
        sorted_result_list = sorted(
            result_list,
            reverse=True,
            key=lambda result: result[2])
    return render(request, 'sushi_app/gender_sorted_list.html',
                  {'sorted_result_list': sorted_result_list})


def get_gender_ave(store):
    all_reviews = Review.objects.filter(store_id__exact=store.id)
    male_reviews_list = [
        review for review in all_reviews if review.user_sex == 1]
    female_reviews_list = [
        review for review in all_reviews if review.user_sex == 2]
    unknown_reviews_list = [
        review for review in all_reviews if review.user_sex == 0]
    if male_reviews_list:
        male_score_ave = sum(
            male_review.score for male_review in male_reviews_list) / len(male_reviews_list)
    else:
        male_score_ave = 0
    if female_reviews_list:
        female_score_ave = sum(
            female_review.score for female_review in female_reviews_list) / len(female_reviews_list)
    else:
        female_score_ave = 0
    return [store, male_score_ave, female_score_ave]


def get_gender_rate(store_id, is_dinner):
    if is_dinner:
        all_reviews = Review.objects.filter(store_id__exact=store_id)
        male_reviews_list = [
            review for review in all_reviews if review.user_sex == 1]
        female_reviews_list = [
            review for review in all_reviews if review.user_sex == 2]
        unknown_reviews_list = [
            review for review in all_reviews if review.user_sex == 0]
        if male_reviews_list:
            male_rate = len(male_reviews_list) / len(all_reviews)
        else:
            male_rate = 0
        if female_reviews_list:
            female_rate = len(female_reviews_list) / len(all_reviews)
        else:
            female_rate = 0
        if unknown_reviews_list:
            unknown_rate = len(unknown_reviews_list) / len(all_reviews)
        else:
            unknown_rate = 0
        return [
            male_rate,
            female_rate,
            unknown_rate]
