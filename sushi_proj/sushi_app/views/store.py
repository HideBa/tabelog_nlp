from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from sushi_app.models import Store, LunchReview

import random


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
                   #    'current_score': current_score
                   })

# # 追加！
# @login_required
# def rate(request, rentroom_id):
#     rentroom = get_object_or_404(RentRoom, id=rentroom_id)

#     log, created = ScoreLog.objects.update_or_create(
#         defaults={'score': request.POST.get('score')},
#         profile_id=request.user.profile.id,
#         rent_room_id=rentroom_id,
#     )

#     if created:
#         messages.success(request, message_rate_created)
#     else:
#         messages.success(request, message_rate_updated)

#     return redirect('iekari:rentroom_detail', rentroom_id=rentroom_id)
