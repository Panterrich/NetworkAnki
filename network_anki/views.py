"""
This module contains the views for the Network Anki application.

Views:
    index: Renders the main page
    terms_list: Renders the terms list page
    add_term: Renders the add term page
    send_term: Handles the submission of a new term
    show_stats: Renders the stats page
"""
from django.shortcuts import render
from django.core.cache import cache
from . import terms_work

def index(request):
    """Renders the main page."""
    return render(request, "index.html")


def terms_list(request):
    """Renders the terms list page."""
    terms = terms_work.get_terms_for_table()
    return render(request, "terms_list.html", context={"terms": terms})


def add_term(request):
    """Renders the add term page."""
    return render(request, "terms_add.html")


def send_term(request):
    """Handles the submission of a new term."""
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        new_term = request.POST.get("new_term", "")
        new_definition = request.POST.get("new_definition", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Описание должно быть не пустым"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Термин должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваш термин принят"
            terms_work.write_term(new_term, new_definition)
        if context["success"]:
            context["success-title"] = ""
        return render(request, "terms_request.html", context)
    else:
        return add_term(request)


def show_stats(request):
    """Renders the stats page."""
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)
