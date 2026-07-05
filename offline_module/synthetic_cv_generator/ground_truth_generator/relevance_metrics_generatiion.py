import json
import pandas as pd
import requests

url = "http://ollama-service:11434/api/generate"

df = pd.read_csv("/app/dfsample_with_cvs.csv")

cv_df = df.iloc[:50]
job_df = df.iloc[:50]

results = []

for _, cv_row in cv_df.iterrows():

    cv_id = cv_row["job_id"]   # your CV id column (as in your dataset)
    cv_text = cv_row["cvs"]

    for _, job_row in job_df.iterrows():

        job_id = f"JOB_{job_row['job_id']}"
        job_text = job_row["description_improved"]

        judge_prompt = f"""
You are a STRICT information retrieval evaluator.

Your task is to decide whether a JOB is RELEVANT for a given CV.

---

CANDIDATE CV:
{cv_text}

---

JOB DESCRIPTION:
{job_text}

---

DECISION RULE:

Return:
1 = relevant (candidate can realistically be hired for this job)
0 = not relevant (candidate is not suitable for this job)

IMPORTANT RULES:
- Be STRICT like a hiring manager
- Only mark 1 if candidate is clearly suitable for the role
- Otherwise mark 0
- Ignore wording similarity
- Ignore country differences
- Ignore job title similarity alone 
- Do not recommend full time jobs to students and part time workers and vice versa.

---

OUTPUT FORMAT (STRICT JSON ONLY):

{{
  "relevance": 0,
  "reason": "short 1-2 line explanation"
}}
"""

        payload = {
            "model": "llama3.2",
            "prompt": judge_prompt,
            "stream": False,
            "format": "json"
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()

            output = response.json()["response"]
            result = json.loads(output)

            results.append({
                "cv_id": cv_id,
                "job_id": job_id,
                "relevance": int(result["relevance"]),
                "reason": result["reason"]
            })

            print(f"{cv_id} -> {job_id}: {result['relevance']}")

        except Exception as e:
            print(f"Failed for {cv_id} -> {job_id}: {e}")

# Save qrels
qrels_df = pd.DataFrame(results)
qrels_df.to_csv("/output/qrels.csv", index=False)