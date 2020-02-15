from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from sushi_proj.settings import BASE_DIR
import json
from collections import defaultdict

prefecture_list = ["北海道",
                   "青森県",
                   "岩手県",
                   "宮城県",
                   "秋田県",
                   "山形県",
                   "福島県",
                   "茨城県",
                   "栃木県",
                   "群馬県",
                   "埼玉県",
                   "千葉県",
                   "東京都",
                   "神奈川県",
                   "新潟県",
                   "富山県",
                   "石川県",
                   "福井県",
                   "山梨県",
                   "長野県",
                   "岐阜県",
                   "静岡県",
                   "愛知県",
                   "三重県",
                   "滋賀県",
                   "京都府",
                   "大阪府",
                   "兵庫県",
                   "奈良県",
                   "和歌山県",
                   "鳥取県",
                   "島根県",
                   "岡山県",
                   "広島県",
                   "山口県",
                   "徳島県",
                   "香川県",
                   "愛媛県",
                   "高知県",
                   "福岡県",
                   "佐賀県",
                   "長崎県",
                   "熊本県",
                   "大分県",
                   "宮崎県",
                   "鹿児島県",
                   "沖縄県"]


def show_top_page(request):

    json_file = BASE_DIR + '/analyze_files/dictionary.json'

    with open(json_file, encoding='utf-8') as f:
        json_data = json.load(f)
        keywords_list = json_data["all_jiku"]["all_jiku_list"]
        keywords_dic = defaultdict(list)
        for keyword in keywords_list:
            print("keyword ==== " + str(keyword))
            if json_data["all_jiku"][keyword]["adjective"]:
                modi_words = json_data["all_jiku"][str(
                    keyword)]["syusyoku"]["syusyoku_list"]
            else:
                modi_words = []
            keywords_dic[keyword] = modi_words

        print("keyword === " + str(keywords_dic))

        return render(
            request, 'index.html', {
                "keywords_list": keywords_list, "prefecture_list": prefecture_list})
