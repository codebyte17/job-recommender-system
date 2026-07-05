import asyncio
import aiohttp
import pandas as pd
import json
from tqdm import tqdm

df = pd.read_csv("/app/dfsample_with_cvs.csv")

cv_df = df.iloc[:20]
job_df = df.iloc[:100]

URL = "http://ollama-service:11434/api/generate"

results = []

# --------------------------
# Prompt builder
# --------------------------
def build_prompt(cv_text, job_text):
    return f"""
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


# --------------------------
# Async request function
# --------------------------
async def call_model(session, cv_id, job_id, cv_text, job_text, sem):
    async with sem:
        payload = {
            "model": "llama3.2",
            "prompt": build_prompt(cv_text, job_text),
            "stream": False,
            "format": "json"
        }

        try:
            async with session.post(URL, json=payload, timeout=300) as resp:
                resp.raise_for_status()
                data = await resp.json()

                result = json.loads(data["response"])

                return {
                    "cv_id": cv_id,
                    "job_id": job_id,
                    "relevance": int(result["relevance"]),
                    "reason": result["reason"]
                }

        except Exception as e:
            return {
                "cv_id": cv_id,
                "job_id": job_id,
                "relevance": 0,
                "reason": f"ERROR: {str(e)}"
            }

# --------------------------
# Main pipeline
# --------------------------
async def main():

    # 👆 controls max parallel requests (tune: 100–500 depending cluster)
    sem = asyncio.Semaphore(3)

    connector = aiohttp.TCPConnector(
        limit=10,
        limit_per_host=3

    )
    async with aiohttp.ClientSession(connector=connector) as session:

        tasks = []

        for _, cv_row in cv_df.iterrows():
            print(cv_row)
            cv_id = cv_row["job_id"]
            cv_text = cv_row["cvs"]

            for _, job_row in job_df.iterrows():
                job_id = f"JOB_{job_row['job_id']}"
                job_text = job_row["description_improved"]

                tasks.append(
                    call_model(session, cv_id, job_id, cv_text, job_text, sem)
                )

        # 🚀 RUN ALL IN PARALLEL
        results = await asyncio.gather(*tasks)

    return results

# --------------------------
# Run
# --------------------------
results = asyncio.run(main())

# Save
pd.DataFrame(results).to_csv("/output/qrels.csv", index=False)

print("DONE")