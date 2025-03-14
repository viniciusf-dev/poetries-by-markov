"""
Configuration settings for the Markov Poetry Generator
"""

# Default model parameters
DEFAULT_ORDER = 2
DEFAULT_MIN_WORDS = 3
DEFAULT_MAX_WORDS = 8
DEFAULT_LINES = 10

# Text processing settings
LINE_BREAK_TOKEN = '\n'
PUNCTUATION_MARKS = [',', '.', ';', ':', '!', '?', ')', '(']

# Generation settings
TITLE_LENGTH_MIN = 2
TITLE_LENGTH_MAX = 5
LINE_ENDING_PROBABILITY = 0.3

# File handling settings
DEFAULT_ENCODING = 'utf-8'
DEFAULT_OUTPUT_DIR = 'generated_poems'