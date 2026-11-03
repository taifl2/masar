# Masar

Paste a job posting and your profile, and Masar tells you which skills you already have, which you're missing, and (soon) which HRDF supported certifications close the gap.

**Status:** work in progress. Week 1 of 4.

## How it works

1. **Job Analyzer** reads the posting and extracts required and nice-to-have skills. Every skill comes with the exact sentence it was taken from.
2. **Gap Analyzer** compares those skills with your profile and marks each one as have, partial or missing, again quoting your profile as evidence.
3. A plain Python check flags any evidence that doesn't appear word for word in the source text, so made-up skills are caught instead of trusted.

The model decides; the code counts and verifies.

## Stack

Python · LangChain · Pydantic · Groq (`openai/gpt-oss-120b`, OpenAI-compatible API)

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
from masar.report import show_report

job = analyze_job(open("job.txt").read())
gap = analyze_gap(job, open("profile.txt").read())
show_report(job, gap)
```

Add your free Groq key to Colab Secrets as `GROQ_API_KEY` first.

## Roadmap

- [x] Job Analyzer
- [x] Gap Analyzer + evidence check
- [ ] Certification Agent: RAG over official HRDF pages
- [ ] Planner and Reviewer agents, orchestrated with LangGraph
- [ ] Streamlit interface
- [ ] Evaluation set and tests

## Author

Taif Al-Anzi · [LinkedIn](https://www.linkedin.com/in/taifalanzi/)
