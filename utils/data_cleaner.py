# utils/data_cleaner.py

import pandas as pd
import re
from collections import Counter

print("Loading dataset... (this may take 30 seconds)")

df = pd.read_csv(
    'data/raw_jobs.csv',
    usecols=['Job Title', 'skills'],
    low_memory=False
)

print(f"Loaded {len(df)} rows")
df = df.dropna(subset=['Job Title', 'skills'])
print(f"After dropping empty rows: {len(df)} rows")

df['Job Title'] = df['Job Title'].str.strip().str.lower()

def parse_skills(skill_value):
    text = str(skill_value).lower()
    text = re.sub(r"[\[\]\'\"]", "", text)
    text = text.replace(";", ",")
    text = text.replace("|", ",")
    text = text.replace("\n", ",")
    raw_skills = text.split(",")
    cleaned = []
    for skill in raw_skills:
        skill = skill.strip()
        skill = re.sub(r"\s+", " ", skill)
        if len(skill) < 3:
            continue
        cleaned.append(skill)
    return list(dict.fromkeys(cleaned))

df['skills_list'] = df['skills'].apply(parse_skills)

print("\nGrouping skills by job role...")

def get_top_skills(skill_lists, top_n=15):
    all_skills = []
    for lst in skill_lists:
        all_skills.extend(lst)
    counter = Counter(all_skills)
    return [skill for skill, count in counter.most_common(top_n)]

grouped = df.groupby('Job Title')['skills_list'].apply(
    lambda x: get_top_skills(x, top_n=15)
).reset_index()

grouped.columns = ['role', 'skills_list']
grouped = grouped[grouped['skills_list'].apply(len) >= 5]
grouped['skills'] = grouped['skills_list'].apply(lambda x: ', '.join(x))
grouped = grouped.drop(columns=['skills_list'])

output_path = 'data/job_roles.csv'
grouped.to_csv(output_path, index=False)

print(f"\n✅ Cleaning complete!")
print(f"Total unique roles extracted: {len(grouped)}")
print(f"Saved to: {output_path}")
print(f"\nSample output:")
print(grouped.head(5).to_string())