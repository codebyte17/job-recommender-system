import pandas as pd
import spacy
from transformers import pipeline
import torch
# ----------------------------
# LOAD MODELS (ONCE)
# ----------------------------
nlp = spacy.load("en_core_web_sm", disable=["ner", "tagger", "lemmatizer"])

classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=0  # GPU (use -1 if CPU)
)

labels = [
    "RESPONSIBILITY",
    "REQUIREMENTS",
    "SKILLS",
    "QUALIFICATIONS",
    "EXPERIENCE",
    "LANGUAGE_REQUIREMENTS",
    "TOOLS_TECHNOLOGIES",
    "WORK_CONDITIONS",
    "TASK_TO_DO",
    "LOCATION",
    "EDUCATION",
    "ABOUT_COMPANY",
    "QUESTION"
]

# ----------------------------
# FILTER FUNCTION (your logic)
# ----------------------------
def filter_response(outputs):
    composed_sent = []

    for result in outputs:
        try:
            indexs = [
                result["labels"].index(field)
                for field in [
                    "EXPERIENCE",
                    "REQUIREMENTS",
                    "QUALIFICATIONS",
                    "TOOLS_TECHNOLOGIES",
                    "SKILLS",
                    "EDUCATION",
                    "RESPONSIBILITY",
                    "TASK_TO_DO"
                ]
            ]

            scores = [result["scores"][i] for i in indexs]

            if sum(scores) > 0.55:
                composed_sent.append(str(result["sequence"]))

        except:
            continue

    return " ".join(composed_sent)


# ----------------------------
# PROCESS ONE TEXT
# ----------------------------
def process_text(doc):
    sentences = [
        sent.text
        for sent in doc.sents
        if len(sent.text.split()) > 4
    ]

    if not sentences:
        return ""

    outputs = classifier(
        sentences,
        candidate_labels=labels,
        batch_size=32
    )

    return filter_response(outputs)


# ----------------------------
# MAIN PIPELINE
# ----------------------------
def run_pipeline(input_csv, output_csv, chunk_size=200):

    df = pd.read_csv(input_csv)

    results = []

    for start in range(0, len(df), chunk_size):

        end = min(start + chunk_size, len(df))  # 0 + 1600 , 1938
        chunk = df.iloc[start:end].copy()

        print(f"Processing rows {start} to {end}")

        # 🚀 FAST spaCy batching
        docs = list(nlp.pipe(chunk["description_en"].astype(str).tolist()))

        chunk_results = [
            process_text(doc)
            for doc in docs
        ]

        chunk["new_description"] = chunk_results
        results.append(chunk)

    final_df = pd.concat(results, ignore_index=True)
    final_df.to_csv(output_csv, index=False)

    print("Done! Saved:", output_csv)


# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    run_pipeline(
        input_csv="/app/jobs_en.csv",
        output_csv="/output/processed_jobs.csv",
        chunk_size=200
    )