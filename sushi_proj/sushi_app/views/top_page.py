from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from sushi_proj.settings import BASE_DIR
import urllib.parse
import json


def show_top_page(request):
    json_file = BASE_DIR + '/analyze_files/dictionary.json'
    #f = open(json_file, "r")
    #json_data = json.load(f)
    with open(json_file, encoding='utf-8') as f:
        json_data = json.load(f)
        keywords_list = json_data["all_jiku"]["all_jiku_list"]
        # keywords_obj_list = []
        # print("keyword_list===" + str(keywords_list))
        # for keyword in keywords_list:
        #     print("keyword type === " + str(type(keyword)))
        #     parameter = urllib.parse.quote(keyword, encoding='utf-8')
        #     list = [keyword, parameter]
        #     keywords_obj_list.append(list)
        # print("keyword_obj === " + str(keywords_obj_list))
        # return render(
        #     request, 'index.html', {
        #         "keywords_obj_list": keywords_obj_list})
        keyword_dict = {}
        for keyword in keywords_list:
            parameter = urllib.parse.quote(keyword, encoding='utf-8')
            keyword_dict[keyword] = parameter
        print("keyword___dict === " + str(keyword_dict))
        return render(request, 'index.html', {"keyword_dict": keyword_dict})
