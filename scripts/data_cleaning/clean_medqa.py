import os
import json
import re
import pandas as pd
from tqdm import tqdm
from config.config import RAW_MEDQA, CLEANED_QA

def clean_text(text):
    if not text: return None
    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x20-\x7E]', '', text)
    return text.strip()

def load_jsonl(filepath):
    records = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                try: records.append(json.loads(line))
                except: pass
    return records

all_records = []
for split in ['train', 'dev', 'test']:
    fpath = RAW_MEDQA / f"{split}.jsonl"
    if fpath.exists():
        recs = load_jsonl(fpath)
        for r in recs:
            r['split'] = split
        all_records.extend(recs)
        print(f"Loaded {split}: {len(recs)} records")

print(f"Total loaded: {len(all_records)}")

cleaned = []
for rec in tqdm(all_records, desc="Cleaning"):
    question = clean_text(rec.get('question', ''))
    options  = rec.get('options', {})
    answer   = clean_text(rec.get('answer', ''))
    split    = rec.get('split', 'train')
    if not question or not answer: continue
    clean_options = {k.upper(): clean_text(v) for k, v in options.items() if clean_text(v)}
    if len(clean_options) < 2: continue
    cleaned.append({
        'question': question,
        'options': clean_options,
        'correct_answer': answer,
        'split': split,
        'source': 'medqa_usmle'
    })

df = pd.DataFrame(cleaned)
df = df.dropna(subset=['correct_answer'])
df = df.drop_duplicates(subset=['question'])
print(f"Final records: {len(df)}")

df.to_csv(CLEANED_QA / 'medqa_usmle_clean.csv', index=False)
with open(CLEANED_QA / 'medqa_usmle_clean.jsonl', 'w') as f:
    for _, row in df.iterrows():
        record = {'question': row['question'], 'answer': row['correct_answer'], 'source': 'medqa_usmle'}
        f.write(json.dumps(record) + '\n')

print("✅ Done!")