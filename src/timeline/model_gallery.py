"""Alcohol brand model/endorser gallery — auto-generated from alcohol_models.json.

Loads 25 products × 70+ timeline entries from the hackathon dataset.
Real celebrity images are served when available; falls back to Imagen-generated images.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote


@dataclass
class SojuModel:
    """A soju/beer brand endorser/model."""

    id: str
    name: str
    name_ko: str
    brand: str
    start_year: int
    end_year: int
    image_prompt: str = ""
    era_note: str = ""
    product_type: str = "soju"
    product_id: str = ""
    company_ko: str = ""
    notes: list[str] = field(default_factory=list)
    confidence: str = "medium"
    real_image_url: str = ""


# ── Brand key normalisation from product_id ──────────────────────────────────

_BRAND_MAP: dict[str, str] = {
    "soju_chamisul": "chamisul",
    "soju_chumchurum": "chum_churum",
    "soju_saero": "saero",
    "soju_jinro_isback": "jinro_is_back",
    "soju_jinro_classic": "jinro",
    "soju_goodday": "goodday",
    "soju_san": "san",
    "soju_green": "green",
    "soju_ipseju": "ipseju",
    "soju_ipseju_brother": "ipseju",
    "soju_daesun": "daesun",
    "beer_terra": "terra",
    "beer_terra_light": "terra_light",
    "beer_kelly": "kelly",
    "beer_cass": "cass",
    "beer_cass_bitz": "cass",
    "beer_cass_light": "cass_light",
    "beer_kloud": "kloud",
    "beer_kloud_draft": "kloud_draft",
    "beer_krush": "krush",
    "beer_kloud_nonalcoholic": "kloud_na",
    "beer_hite": "hite",
    "beer_max": "max",
    "beer_ob": "ob",
    "beer_crown": "crown",
    "fruit_soju_sunhari": "sunhari",
    "sparkling_soju_isul_ttokttok": "isul_ttokttok",
    "whisky_jw_red": "jw_red",
    "whisky_jw_black": "jw_black",
    "whisky_jw_blue": "jw_blue",
    "whisky_jw_global": "jw_global",
}

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# ── Real image scanning ──────────────────────────────────────────────────────

def _scan_real_images() -> dict[str, list[str]]:
    """Return {product_id: [filename, ...]} from generated_images/real/."""
    real_dir = _PROJECT_ROOT / "generated_images" / "real"
    result: dict[str, list[str]] = {}
    if not real_dir.is_dir():
        return result
    for product_dir in real_dir.iterdir():
        if product_dir.is_dir():
            result[product_dir.name] = sorted(
                f.name for f in product_dir.iterdir() if f.is_file()
            )
    return result


def _find_real_image(
    product_id: str,
    start_year: int,
    model_names: list[str],
    image_index: dict[str, list[str]],
) -> str:
    """Find a real image URL for this timeline entry, or return empty string."""
    files = image_index.get(product_id, [])
    if not files:
        return ""

    year_str = str(start_year)

    # 1) year + model name match
    for model_name in model_names:
        clean = model_name.split("(")[0].strip()
        for fname in files:
            if fname.startswith(year_str) and clean in fname:
                return f"/images/real/{quote(product_id, safe='')}/{quote(fname, safe='')}"

    return ""


# ── JSON → SojuModel conversion ─────────────────────────────────────────────

def _load_gallery() -> list[SojuModel]:
    json_path = Path(__file__).resolve().parent / "data" / "alcohol_models.json"
    if not json_path.exists():
        return []

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    image_index = _scan_real_images()
    models: list[SojuModel] = []
    counter = 1

    for entity in data.get("entities", []):
        product_id = entity["product_id"]
        product_name = entity.get("product_name_ko", "")
        company_ko = entity.get("company_ko", "")
        product_type = entity.get("product_type", "soju")
        brand = _BRAND_MAP.get(product_id, product_id)

        for entry in entity.get("timeline", []):
            start_year = entry["start_year"]
            end_year = entry["end_year"]
            model_names: list[str] = entry.get("models", [])
            notes: list[str] = entry.get("notes", [])
            confidence: str = entry.get("confidence", "medium")

            display_name = ", ".join(model_names) if model_names else product_name
            real_image = _find_real_image(product_id, start_year, model_names, image_index)

            model_id = f"model-{counter:03d}"
            models.append(SojuModel(
                id=model_id,
                name=display_name,
                name_ko=display_name,
                brand=brand,
                start_year=start_year,
                end_year=end_year,
                era_note="; ".join(notes) if notes else "",
                product_type=product_type,
                product_id=product_id,
                company_ko=company_ko,
                notes=notes,
                confidence=confidence,
                real_image_url=real_image,
            ))
            counter += 1

    return models


MODEL_GALLERY: list[SojuModel] = _load_gallery()


# ── Public helpers ───────────────────────────────────────────────────────────

def get_models_at_year(
    year: int,
    brand: str | None = None,
    product_type: str | None = None,
) -> list[SojuModel]:
    """Return models active at a given year."""
    result = []
    for m in MODEL_GALLERY:
        if m.start_year <= year <= m.end_year:
            if brand and brand != "all" and m.brand != brand:
                continue
            if product_type and product_type != "all" and m.product_type != product_type:
                continue
            result.append(m)
    return result


def serialize_model(m: SojuModel) -> dict:
    image_url = m.real_image_url if m.real_image_url else f"/images/models/{m.id}.png"
    return {
        "id": m.id,
        "name": m.name,
        "name_ko": m.name_ko,
        "brand": m.brand,
        "start_year": m.start_year,
        "end_year": m.end_year,
        "era_note": m.era_note,
        "image_url": image_url,
        "product_type": m.product_type,
        "product_id": m.product_id,
        "company_ko": m.company_ko,
        "notes": m.notes,
        "confidence": m.confidence,
    }
