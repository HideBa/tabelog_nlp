from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from sushi_proj.settings import BASE_DIR


def show_top_page(request):
    return HttpResponse("top page")
