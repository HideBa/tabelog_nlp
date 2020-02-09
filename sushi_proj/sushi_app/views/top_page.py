from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from sushi_proj.settings import BASE_DIR
import json


def show_top_page(request):
    json_file = BASE_DIR + '/analyze_files/dictionary.json'

    with open(json_file, encoding='utf-8') as f:
        json_data = json.load(f)
        keywords_list = json_data["all_jiku"]["all_jiku_list"]

        return render(
            request, 'index.html', {
                "keywords_list": keywords_list})
