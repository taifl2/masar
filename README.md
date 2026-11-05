# Masar

Paste a job posting and your profile, and Masar tells you which skills you already have, which you're missing, and which certifications from a curated list close the gap, with their HRDF support status.

**Status:** work in progress. Week 2 of 4.

## How it works

1. **Job Analyzer** reads the posting and extracts required and nice-to-have skills. Every skill comes with the exact sentence it was taken from.
2. **Gap Analyzer** compares those skills with your profile and marks each one as have, partial or missing, again quoting your profile as evidence.
3. **Certification Agent** searches a small knowledge base of certifications (`data/certifications.json`) with sentence embeddings and FAISS, then asks the model to pick the best matches for the missing skills. It can only choose from what the search returned, and any other id is dropped in code.
4. A plain Python check flags any evidence that doesn't appear word for word in the source text, so made-up skills are caught instead of trusted.

HRDF support status and links come from the knowledge base, never from the model. Entries not yet checked against hrdf.org.sa are shown as "not verified".

### What I changed after testing

Searching with the bare skill name ("LangChain") missed relevant certifications because one word gives the embedding too little context. Searching with the skill plus its sentence from the job post fixed it:

| Missing skill | Search by name only | Search by name + job sentence |
|---|---|---|
| Python | PCAP | PCAP |
| RAG | nothing above threshold | NVIDIA Generative AI LLMs |

A second test showed the model justifying a match with a skill that isn't in the certification's data ("including RAG"). The prompt now requires the reason to use only the listed skills.

The model decides; the code counts and verifies.

## Stack

Python · LangChain · Pydantic · Groq (`openai/gpt-oss-120b`, OpenAI-compatible API) · sentence-transformers (`all-MiniLM-L6-v2`) · FAISS

Any OpenAI-compatible provider works: change `MODEL_NAME` and `BASE_URL` in `masar/config.py`.

## Run it in Colab

```python
!git clone https://github.com/taifl2/masar.git
%cd masar
!pip install -q -r requirements.txt

import os
from google.colab import userdata
os.environ["GROQ_API_KEY"] = userdata.get("GROQ_API_KEY")

from masar.job_analyzer import analyze_job
from masar.gap_analyzer import analyze_gap
from masar.certification_agent import recommend_certs
from masar.report import show_report, show_certifications

job = analyze_job(open("job.txt").read())
gap = analyze_gap(job, open("profile.txt").read())
show_report(job, gap)
show_certifications(recommend_certs(job, gap))
```

Add your free Groq key to Colab Secrets as `GROQ_API_KEY` first.

## Roadmap

- [x] Job Analyzer
- [x] Gap Analyzer + evidence check
- [x] Certification Agent: semantic search over a certification knowledge base
- [ ] Verify every knowledge-base entry against hrdf.org.sa
- [ ] Planner and Reviewer agents, orchestrated with LangGraph
- [ ] Streamlit interface
- [ ] Evaluation set and tests

## Author

Taif Al-Anzi · [LinkedIn](https://www.linkedin.com/in/taifalanzi/)
