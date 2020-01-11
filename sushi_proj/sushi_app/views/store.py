from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from sushi_app.models import Store

import random

message_rate_created = '評価が登録されました！'
message_rate_updated = '評価が更新されました！'


def list_view(request):
    rentroom_list = Store.objects.all().order_by('-id')
    paginator = Paginator(rentroom_list, 20)  # ページ当たり20個表示

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


# def detail_view(request, rentroom_id):
#     rentroom = get_object_or_404(RentRoom, id=rentroom_id)

#     try:
#         page = int(request.GET.get('from_page'))
#     except BaseException:
#         page = 1

#     try:
#         log = ScoreLog.objects.get(
#             profile_id=request.user.profile.id,
#             rent_room_id=rentroom_id)
#         current_score = log.score
#     except BaseException:
#         current_score = -1

#     return render(request,
#                   'iekari/rentroom_detail.html',
#                   {'rentroom': rentroom,
#                    'page': page,
#                    'current_score': current_score})

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
