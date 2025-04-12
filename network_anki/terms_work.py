from network_anki.models import Terms, TermAuthors

def get_terms_for_table():
    terms = []
    for i, term in enumerate(Terms.objects.all()):
        terms.append([i+1, term.term, term.definition])
    return terms


def write_term(new_term, new_definition):
    term = Terms(term=new_term, definition=new_definition)
    term_addition = TermAuthors(term_id=term, author="user", email="user@example.com")
    term.save()
    term_addition.save()


def get_terms_stats():
    db_terms = TermAuthors.objects.filter(author="db").count()
    user_terms = TermAuthors.objects.filter(author="user").count()
    all_terms = Terms.objects.all()
    defin_len = [len(term.definition) for term in all_terms]
    stats = {
        "terms_all": db_terms + user_terms,
        "terms_own": db_terms,
        "terms_added": user_terms,
        "words_avg": sum(defin_len)/len(defin_len),
        "words_max": max(defin_len),
        "words_min": min(defin_len)
    }
    return stats
