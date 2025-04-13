"""
This module contains the views for the Network Anki application.

Views:
    index: Renders the main page
    terms_list: Renders the terms list page
    add_term: Renders the add term page
    send_term: Handles the submission of a new term
    show_stats: Renders the stats page
    quiz: Renders the quiz page
    check_answer: Handles answer checking
"""
import random
from django.shortcuts import render
from django.core.cache import cache
from . import terms_work

def index(request):
    """Renders the main page."""
    request.session.clear()
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

def quiz(request):
    """Renders the quiz page with a random term."""
    if 'score' not in request.session:
        terms = terms_work.get_terms_for_table()
        if not terms:
            return render(request, "quiz.html", {"error": "Нет доступных терминов для квиза"})

        terms_in_game = random.sample(terms, min(10, len(terms)))

        wrong_definitions_per_term = []
        for term in terms_in_game:
            other_definitions = [t[2] for t in terms if t[0] != term[0]]

            wrong_definitions = random.sample(other_definitions, min(3, len(other_definitions)))
            wrong_definitions_per_term.append(wrong_definitions)

        request.session['score'] = 0
        request.session['current_term'] = 0
        request.session['terms_in_game'] = terms_in_game
        request.session['wrong_definitions'] = wrong_definitions_per_term

    if 'score' in request.session:
        if request.session['current_term'] == len(request.session['terms_in_game']):
            return quiz_results(request)

    term = request.session['terms_in_game'][request.session['current_term']]
    wrong_definitions = request.session['wrong_definitions'][request.session['current_term']]

    request.session['correct_answer'] = term[2]

    all_definitions = wrong_definitions + [term[2]]
    random.shuffle(all_definitions)

    context = {
        'term': term[1],
        'definitions': all_definitions,
        'score': request.session['score'],
        'total': len(request.session['terms_in_game']),
        'current_term': request.session['current_term'] + 1
    }
    return render(request, "quiz.html", context)

def quiz_results(request):
    """Renders the quiz results page."""

    score = request.session['score']
    terms_count = len(request.session['terms_in_game'])

    request.session.clear()

    context = {
        'score': score,
        'terms_count': terms_count
    }
    return render(request, "quiz_results.html", context)

def check_answer(request):
    """Checks the user's answer and updates the score."""
    if request.method == "POST":
        user_answer = request.POST.get('answer')
        correct_answer = request.session['correct_answer']


        if user_answer == correct_answer:
            request.session['score'] += 1
            message = "Правильно!"
        else:
            message = "Неправильно"

        request.session['current_term'] += 1
        request.session['correct_answer'] = None

        context = {
            'message': message,
            'correct_answer': correct_answer,
            'score': request.session['score'],
            'total': len(request.session['terms_in_game']),
            'current_term': request.session['current_term'],
            'show_next': True
        }
        return render(request, "quiz.html", context)

    return quiz(request)
