import logging
import re
import sys
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)

ENTRY_RE = re.compile(r"@(\w+)\{([^,]+),(.*?)\n\}", re.DOTALL)
FIELD_RE = re.compile(r"^\s*(\w+)\s*=\s*\{(.*?)\},?\s*$", re.MULTILINE | re.DOTALL)
UMLAUTS = {f'\\"{c}': u for c, u in zip("aouAOU", "äöüÄÖÜ")}

Date = int | str


class Source(BaseModel):
    model_config = ConfigDict(extra="ignore", frozen=True)


class Job(Source):
    company: str
    position: str
    location: str
    start_date: Date
    end_date: Date
    summary: str = ""


class Degree(Source):
    institution: str
    area: str
    studyType: str
    location: str
    start_date: Date | None = None
    end_date: Date | None = None
    date: Date | None = None
    highlights: list[str] = []


class Award(Source):
    title: str
    date: Date
    awarder: str
    url: str
    summary: str


class Project(Source):
    name: str
    summary: str
    url: str
    date: Date


class Labelled(Source):
    name: str
    summary: str = ""
    keywords: str = ""


class Network(Source):
    network: str
    username: str


class Sections(Source):
    Experience: list[Job]
    Education: list[Degree]
    Awards: list[Award]
    Projects: list[Project]
    Languages: list[Labelled]
    Interests: list[Labelled]


class CV(Source):
    name: str
    location: str
    email: str
    website: str
    summary: str
    social_networks: list[Network]
    sections: Sections


def link(text: str, url: str) -> str:
    return f"[{text}]({url})"


def unbrace(text: str) -> str:
    for latex, char in UMLAUTS.items():
        text = text.replace(latex, char)
    return re.sub(r"\s+", " ", text.replace("{", "").replace("}", "")).strip()


def author_names(field: str, own_name: str) -> list[str]:
    names: list[str] = []
    for raw in re.split(r"\s+and\s+", field):
        last, _, first = unbrace(raw).partition(", ")
        name = f"{first} {last}".strip() if first else last
        names.append(f"**{name}**" if name == own_name else name)
    return names


def publications(bib_text: str, own_name: str) -> list[dict[str, object]]:
    entries: list[tuple[int, dict[str, object]]] = []
    for _, key, body in ENTRY_RE.findall(bib_text):
        fields = {name.lower(): value for name, value in FIELD_RE.findall(body)}
        year = int(fields["year"])
        entry: dict[str, object] = {
            "title": unbrace(fields["title"]),
            "authors": author_names(fields["author"], own_name),
            "journal": unbrace(fields.get("booktitle") or fields["journal"]),
            "date": year,
        }
        if "doi" in fields:
            entry["doi"] = fields["doi"]
        elif "url" in fields:
            entry["url"] = fields["url"]
        logger.info("publication %s", key)
        entries.append((year, entry))
    return [entry for _, entry in sorted(entries, key=lambda pair: pair[0], reverse=True)]


def degree_entry(d: Degree) -> dict[str, object]:
    entry: dict[str, object] = {
        "institution": d.institution,
        "area": d.area,
        "degree": d.studyType.removesuffix(" candidate"),
        "location": d.location,
    }
    for key, value in (("start_date", d.start_date), ("end_date", d.end_date), ("date", d.date)):
        if value is not None:
            entry[key] = value
    if d.highlights:
        entry["highlights"] = d.highlights
    return entry


def rendercv_doc(cv: CV, bib_text: str) -> dict[str, object]:
    s = cv.sections
    sections: dict[str, list[object]] = {
        "Summary": [cv.summary],
        "Experience": [j.model_dump(exclude_defaults=True) for j in s.Experience],
        "Education": [degree_entry(d) for d in s.Education],
        "Publications": list(publications(bib_text, cv.name)),
        "Awards": [
            {"name": link(a.title, a.url), "date": a.date, "summary": f"{a.awarder}. {a.summary}"} for a in s.Awards
        ],
        "Projects": [{"name": link(p.name, p.url), "date": p.date, "summary": p.summary} for p in s.Projects],
        "Languages": [{"label": e.name, "details": e.summary} for e in s.Languages],
        "Interests": [{"label": e.name, "details": e.keywords} for e in s.Interests],
    }
    return {
        "cv": {
            "name": cv.name,
            "location": cv.location,
            "email": cv.email,
            "website": cv.website,
            "social_networks": [n.model_dump() for n in cv.social_networks],
            "sections": sections,
        }
    }


def main(cv_path: Path, bib_path: Path, out_path: Path) -> None:
    cv = CV.model_validate(yaml.safe_load(cv_path.read_text())["cv"])
    doc = rendercv_doc(cv, bib_path.read_text())
    out_path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
    logger.info("wrote %s", out_path)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
