from masar.schemas import GapReport, JobRequirements


def check_evidence(job: JobRequirements, job_text: str) -> list[str]:
    """Return the skills whose evidence is not found word for word in the job post."""
    return [
        s.name
        for s in job.required_skills + job.nice_to_have
        if s.evidence.strip() not in job_text
    ]


def show_report(job: JobRequirements, gap: GapReport) -> None:
    """Display the gap report as an HTML card in a notebook."""
    from IPython.display import HTML, display

    groups = {"have": [], "partial": [], "missing": []}
    for m in gap.matches:
        groups[m.status].append(m)

    total = len(gap.matches)
    have = len(groups["have"])
    percent = round(have / total * 100) if total else 0
    experience = f"{job.years_of_experience} years" if job.years_of_experience else "not stated"

    def cards(items, color):
        html = ""
        for m in items:
            kind = "Required" if m.required else "Nice to have"
            evidence = m.candidate_evidence or "Not mentioned in your profile"
            html += f"""
            <div style="border-left:4px solid {color};padding:8px 12px;margin:6px 0;
                        background:#f6f7f9;border-radius:6px">
              <b>{m.skill}</b>
              <span style="color:#888;font-size:12px"> · {kind}</span><br>
              <span style="color:#555;font-size:13px">{evidence}</span>
            </div>"""
        return html or "<p style='color:#999'>None</p>"

    page = f"""
    <div style="font-family:Arial;max-width:720px;color:#222;background:white;
                padding:20px 24px;border-radius:12px">
      <h2 style="margin:0">{job.job_title}</h2>
      <p style="color:#666;margin:4px 0 16px">Experience: {experience}</p>
      <div style="background:#e6e6e6;border-radius:8px;height:12px">
        <div style="background:#2e7d32;height:12px;border-radius:8px;width:{percent}%"></div>
      </div>
      <p><b>{percent}% match</b> · {have} of {total} skills</p>
      <h3 style="color:#2e7d32">✅ You have</h3>{cards(groups["have"], "#2e7d32")}
      <h3 style="color:#e0a000">🟡 Partly</h3>{cards(groups["partial"], "#e0a000")}
      <h3 style="color:#c62828">❌ Missing</h3>{cards(groups["missing"], "#c62828")}
    </div>"""

    display(HTML(page))
