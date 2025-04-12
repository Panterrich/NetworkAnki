"""
Django models for the Network Anki application.

This module contains the database models for storing terms and their authors.

Models:
    Terms: Stores network terminology and definitions
    TermAuthors: Stores author information for terms
"""
from django.db import models

class Terms(models.Model):
    """Stores network terminology and definitions."""
    term_id = models.AutoField(primary_key=True, db_column="term_id")
    term = models.CharField(max_length=200, db_column="term")
    definition = models.TextField(db_column="definition")
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")

    class Meta:
        db_table = "terms"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.term)


class TermAuthors(models.Model):
    """Stores author information for terms."""
    term_id = models.ForeignKey(Terms, on_delete=models.CASCADE, db_column="term_id")
    author = models.CharField(max_length=200, db_column="author")
    email = models.EmailField(db_column="email")

    class Meta:
        db_table = "term_authors"

    def __str__(self) -> str:
        return str(self.author)
