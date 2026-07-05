import pandas as pd
import requests
import json
import os

# =========================
# KUBERNETES OLLAMA SERVICE
# =========================
OLLAMA_URL = "http://ollama-service:11434/api/generate"

# =========================
# LOAD DATA
# =========================
df_sample = pd.read_csv("/app/sample_integrated_cleaned.v2.csv")
job_descriptions = df_sample.description_improved.to_list()

results = []

# =========================
# CV GENERATION FUNCTION
# =========================
def generate_cv(job_description):

    prompt = f"""
You are an expert HR specialist and professional resume writer.

Given the following job description, create a highly realistic and professional CV for an ideal candidate.

JOB DESCRIPTION:
{job_description}

Instructions:
- Create an original CV that is inspired by the job requirements but does NOT copy or closely paraphrase the job description.
- Infer a believable career history, education, certifications, technical skills, and achievements that naturally align with the role.
- Ensure the work experience demonstrates career progression and includes realistic responsibilities and measurable accomplishments.
- Include relevant skills, but avoid listing every keyword from the job description.
- Use varied wording and natural language that resembles a resume written by a professional, not generated from the job posting.
- Introduce reasonable variation in industries, company types, job titles, education, and certifications where appropriate.
- Keep dates, durations, promotions, and qualifications internally consistent.
- Avoid exaggerated achievements or unrealistic career trajectories.
- Do not invent impossible credentials or famous employers unless they are plausible.
- The CV should feel unique and suitable for training or testing AI systems with synthetic data.

Requirements:
- Return ONLY plain text CV
- No JSON, no markdown
- Sections: FULL NAME, ADDRESS, SUMMARY, SKILLS, EDUCATION, WORK EXPERIENCE, CERTIFICATIONS
"""

    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["response"]


# =========================
# PROCESS SEQUENTIALLY (K8S SAFE)
# =========================
for i, jd in enumerate(job_descriptions):
    try:
        cv_text = generate_cv(jd)
        results.append((i, cv_text))

        # write directly to PVC
        output_path = f"/output/cv_{i}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(cv_text)

        print(f"Saved CV {i}")

    except Exception as e:
        print(f"Error at {i}: {e}")


# =========================
# FINAL JSON SUMMARY
# =========================
final_output = {
    "items": [r[1] for r in results]
}

with open("/output/generated_df_sample.v2.json", "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=4, ensure_ascii=False)

print("DONE — All CVs saved to PVC")