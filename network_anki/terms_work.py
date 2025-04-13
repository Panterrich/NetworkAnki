"""
This module contains the logic for working with terms and authors.
"""
from django.db import models
from network_anki.models import Terms, TermAuthors

def get_terms_for_table():
    """Retrieves all terms and their definitions for display in a table."""
    terms = []
    for i, term in enumerate(Terms.objects.all()):
        terms.append([i+1, term.term, term.definition])
    return terms


def write_term(new_term, new_definition):
    """Adds a new term and its author to the database."""
    term = Terms(term=new_term, definition=new_definition)
    term_addition = TermAuthors(term_id=term, author="user", email="user@example.com")
    term.save()
    term_addition.save()


def get_terms_stats():
    """Calculates statistics about the terms in the database."""
    db_terms = TermAuthors.objects.filter(author="db").count()
    user_terms = TermAuthors.objects.filter(author="user").count()
    all_terms = Terms.objects.all()
    defin_len = [len(term.definition.split()) for term in all_terms]

    top_users = (TermAuthors.objects
                 .exclude(author="db")
                 .values('author', 'email')
                 .annotate(terms_count=models.Count('author'))
                 .order_by('-terms_count')[:5])

    stats = {
        "terms_all": db_terms + user_terms,
        "terms_own": db_terms,
        "terms_added": user_terms,
        "words_avg": sum(defin_len)/len(defin_len) if defin_len else 0,
        "words_max": max(defin_len) if defin_len else 0,
        "words_min": min(defin_len) if defin_len else 0,
        "top_users": list(top_users)
    }
    return stats
