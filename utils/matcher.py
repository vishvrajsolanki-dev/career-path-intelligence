# utils/matcher.py
# PURPOSE: Match a user's skills against all 42 job roles
# METHOD: TF-IDF vectorization + Cosine Similarity
#
# INPUT  → user types their skills as plain text
# OUTPUT → list of top N roles with match % scores

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ─────────────────────────────────────────
# LOAD ROLES FROM CSV
# ─────────────────────────────────────────

def load_roles(filepath='data/job_roles.csv'):
    """
    Reads the cleaned job_roles.csv file.
    Expects two columns: 'role' and 'skills'
    """
    df = pd.read_csv(filepath)

    if 'role' not in df.columns or 'skills' not in df.columns:
        raise ValueError("job_roles.csv must have 'role' and 'skills' columns")

    # Drop rows where skills column is empty
    df = df.dropna(subset=['skills'])

    # Make sure skills column is always a string
    df['skills'] = df['skills'].astype(str)

    return df


# ─────────────────────────────────────────
# BUILD TF-IDF VECTORIZER
# ─────────────────────────────────────────

def build_vectorizer(skills_text_list):
    """
    Trains a TF-IDF model on all role skill texts.

    ngram_range=(1,2) means it considers:
      - single words: "python", "sql"
      - two-word phrases: "machine learning", "data analysis"

    stop_words='english' ignores filler words:
      - "and", "the", "of", "with" etc.

    Returns:
      vectorizer   → the trained model (we'll reuse this for user input)
      role_matrix  → a 2D array, one row per role, columns = skill terms
    """
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words='english',
        min_df=1
    )

    role_matrix = vectorizer.fit_transform(skills_text_list)

    return vectorizer, role_matrix


# ─────────────────────────────────────────
# MAIN FUNCTION — MATCH USER SKILLS
# ─────────────────────────────────────────

def match_roles(user_skills_text, top_n=5, filepath='data/job_roles.csv'):
    """
    Given a user's skills as plain text, returns top N matching roles.

    Parameters:
      user_skills_text → string e.g. "python sql pandas machine learning"
      top_n            → how many roles to return (default 5)
      filepath         → path to job_roles.csv

    Returns:
      List of dicts, each containing:
        'role'   → job title string
        'score'  → match percentage (float, 0–100)
        'skills' → that role's full skill text (for gap detection later)
    """

    # 1. Load the role data
    df = load_roles(filepath)

    # 2. Build vectorizer using all 42 role skill texts
    vectorizer, role_matrix = build_vectorizer(df['skills'].tolist())

    # 3. Transform user input using the SAME vectorizer
    #    (transform not fit_transform — vocabulary is already fixed)
    user_vector = vectorizer.transform([user_skills_text])

    # 4. Calculate cosine similarity between user and every role
    #    Result: 1D array of 42 scores, one per role
    scores = cosine_similarity(user_vector, role_matrix).flatten()

    # 5. Sort scores highest to lowest, take top N indices
    top_indices = np.argsort(scores)[::-1][:top_n]

    # 6. Build result list
    results = []
    for idx in top_indices:
        score = scores[idx]

        # Skip roles with near-zero relevance
        if score < 0.01:
            continue

        results.append({
            'role': df.iloc[idx]['role'],
            'score': round(float(score) * 100, 1),
            'skills': df.iloc[idx]['skills']
        })

    return results


# ─────────────────────────────────────────
# SELF-TEST — run this file directly to verify
# python utils/matcher.py
# ─────────────────────────────────────────

if __name__ == "__main__":

    test_cases = [
        "python machine learning data analysis sql pandas scikit-learn",
        "html css javascript react frontend web development",
        "marketing social media brand strategy analytics",
    ]

    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"INPUT SKILLS: {test}")
        print(f"{'='*60}")

        matches = match_roles(test, top_n=3)

        if not matches:
            print("No matches found.")
        else:
            for i, m in enumerate(matches, 1):
                print(f"\n  {i}. {m['role'].title()}")
                print(f"     Match Score : {m['score']}%")