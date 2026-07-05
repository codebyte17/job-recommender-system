import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
import pandas as pd
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import multiprocessing
# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Initialize the SkillExtractor
skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
df = pd.read_csv("../datasets/processed/integrated_dataset.v2.csv")


def init_worker():
    global skill_extractor


def extract_skill_names(description):
    try:
        annotations = skill_extractor.annotate(description)


        return annotations["results"]

    except Exception:
        return {"results": []}





texts = df["description_improved"].tolist()

if __name__ == "__main__":

    with ProcessPoolExecutor(
        max_workers=multiprocessing.cpu_count(),
        initializer=init_worker
    ) as executor:

        results = list(tqdm(
            executor.map(extract_skill_names, texts),
            total=len(texts),
            desc="Extracting skills"
        ))

    df["skills_ids"] = results

    df.to_csv("../datasets/processed/integrated_data_skills_extracted.v2.csv", index=False)