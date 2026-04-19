from datasets import load_dataset
import pandas as pd
import re
import json
from tqdm import tqdm
from config.config import RAW_MEDMCQA, CLEANED_QA

def clean_text(text):
    if pd.isna(text): return None
    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text)
    return text.strip() if text.strip() else None

print("Downloading MedMCQA from HuggingFace...")
dataset = load_dataset("medmcqa")

for split in ['train', 'validation', 'test']:
    df = pd.DataFrame(dataset[split])
    df.to_csv(RAW_MEDMCQA / f'medmcqa_{split}.csv', index=False)
    print(f"Saved medmcqa_{split}.csv — {len(df)} rows")

all_dfs = []
for split in ['train', 'validation', 'test']:
    df = pd.read_csv(RAW_MEDMCQA / f'medmcqa_{split}.csv')
    df['split'] = split
    all_dfs.append(df)

df = pd.concat(all_dfs, ignore_index=True)
print(f"Total loaded: {len(df)}")

for col in ['question', 'opa', 'opb', 'opc', 'opd', 'exp']:
    if col in df.columns:
        df[col] = df[col].apply(clean_text)

df = df.dropna(subset=['question', 'opa', 'opb'])

option_map = {0: 'opa', 1: 'opb', 2: 'opc', 3: 'opd'}

def get_answer(row):
    try:
        col = option_map.get(int(row.get('cop')))
        return row.get(col)
    except: return None

df['correct_answer'] = df.apply(get_answer, axis=1)
df = df.dropna(subset=['correct_answer'])
df = df.drop_duplicates(subset=['question'])

cleaned = []
for _, row in tqdm(df.iterrows(), total=len(df)):
    options = {}
    for i, col in option_map.items():
        val = row.get(col)
        if val: options[chr(65+i)] = str(val).strip()
    cleaned.append({
        'question': row['question'],
        'answer': row['correct_answer'],
        'explanation': row.get('exp'),
        'subject': row.get('subject_name', 'unknown'),
        'source': 'medmcqa'
    })

df_clean = pd.DataFrame(cleaned)
df_clean.to_csv(CLEANED_QA / 'medmcqa_clean.csv', index=False)
with open(CLEANED_QA / 'medmcqa_clean.jsonl', 'w') as f:
    for _, row in df_clean.iterrows():
        f.write(json.dumps(row.to_dict()) + '\n')

print(f"Final records: {len(df_clean)}")
print("✅ Done!")