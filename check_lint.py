"""Pylint from here"""
import os

import pylint.lint

BASE_DIR = os.path.join(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "lunch_selector")
pylint_opts = [
    os.path.join(PROJECT_DIR, d) for d in os.listdir(PROJECT_DIR)
    if os.path.isdir(os.path.join(PROJECT_DIR, d))
] + ["--rcfile", os.path.join(BASE_DIR, "pylintrc")]

pylint.lint.Run(pylint_opts)
