"""Marks django.contrib.admin as managed by Django migrations."""

from __future__ import unicode_literals

from django_evolution.mutations import MoveToDjangoMigrations


MUTATIONS = [
    MoveToDjangoMigrations(),
]
