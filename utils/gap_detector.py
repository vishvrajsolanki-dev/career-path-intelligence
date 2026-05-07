# utils/gap_detector.py
# APPROACH: Keyword-level gap detection
#
# WHY: The dataset stores skills as messy long phrases.
# Trying to split them into clean phrases always breaks.
# Instead we extract the most meaningful WORDS from the
# role's skill text and check which ones the user knows.

import re
from collections import Counter


# Words too generic to be meaningful skill indicators
IGNORE_WORDS = {
    'and', 'the', 'for', 'with', 'using', 'skills', 'knowledge',
    'experience', 'ability', 'understanding', 'proficiency', 'strong',
    'development', 'management', 'analysis', 'tools', 'systems',
    'practices', 'methods', 'techniques', 'principles', 'processes',
    'e.g', 'etc', 'such', 'including', 'related', 'based', 'driven',
    'working', 'ability', 'excellent', 'good', 'high', 'large', 'best'
}


def extract_keywords(text, top_n=20):
    """
    Pull the most meaningful individual words from a skill text blob.

    Steps:
    1. Lowercase and remove punctuation
    2. Split into words
    3. Remove short words and generic filler words
    4. Count frequency — most repeated words = most important skills
    5. Return top N
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)   # remove punctuation
    words = text.split()

    # Filter: keep only meaningful words of decent length
    words = [
        w for w in words
        if len(w) > 3 and w not in IGNORE_WORDS
    ]

    # Count frequency and return most common
    counter = Counter(words)
    top_words = [word for word, count in counter.most_common(top_n)]

    return top_words


def detect_gaps(user_skills_text, role_skills_text):
    """
    Compare user skills against a role's required skills.

    Parameters:
      user_skills_text  → string, what the user typed
      role_skills_text  → string, role's full skill blob from CSV

    Returns dict with:
      'matched'  → keywords the user already has  (list)
      'missing'  → keywords the user is missing   (list)
      'coverage' → % of role keywords user covers (float)
    """

    # Extract top keywords from the role
    role_keywords = extract_keywords(role_skills_text, top_n=20)

    # Extract words from user input
    user_words = set(extract_keywords(user_skills_text, top_n=100))

    matched = []
    missing = []

    for keyword in role_keywords:
        if keyword in user_words:
            matched.append(keyword)
        else:
            missing.append(keyword)

    total = len(matched) + len(missing)
    coverage = round((len(matched) / total) * 100, 1) if total > 0 else 0.0

    return {
        'matched': matched,
        'missing': missing,
        'coverage': coverage
    }


# ─────────────────────────────────────────
# SELF-TEST
# ─────────────────────────────────────────

if __name__ == "__main__":
    import pandas as pd

    df = pd.read_csv('data/job_roles.csv')

    # Print all available roles so we can pick a valid one
    print("Available roles:", df['role'].tolist())
    print()

    # Test with first role in dataset
    role_row = df.iloc[0]
    user_input = "python machine learning pandas data analysis sql"

    print(f"Role       : {role_row['role'].title()}")
    print(f"User Input : {user_input}")

    result = detect_gaps(user_input, role_row['skills'])

    print(f"\nCoverage   : {result['coverage']}%")

    print(f"\n✅ Skills You Already Have ({len(result['matched'])}):")
    for s in result['matched']:
        print(f"   + {s}")

    print(f"\n❌ Skills You're Missing ({len(result['missing'])}):")
    for s in result['missing']:
        print(f"   - {s}")