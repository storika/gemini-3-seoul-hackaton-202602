"""Batch vectorize creators from CSV using Vertex AI Batch Prediction.

Usage:
    # Sample 100 first
    python3 scripts/batch_vectorize_creators.py --sample 100

    # Full run after validation
    python3 scripts/batch_vectorize_creators.py
"""

import argparse
import csv
import json
import os
import time

from dotenv import load_dotenv
from google import genai
from google.cloud import storage

load_dotenv()

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SCHEMA_PATH = "data/schemas/creator_feature_vector.schema.json"
INSTAGRAM_CSV = "data/instagram_gb_creators_100k.csv"
MODEL = "gemini-3-flash-preview"
GCP_PROJECT = "storika-455708"
GCS_BUCKET = "storika-ai-agents"
GCS_PREFIX = "batch-vectorize"
POLL_INTERVAL = 30  # seconds

with open(SCHEMA_PATH) as f:
    SCHEMA_JSON = f.read()

SYSTEM_PROMPT = f"""# Role: Senior Visual Brand Strategist & AI Persona Architect (Korean Soju Industry)

# Task
Convert the following Instagram creator data into the 'Hyper-Detailed Creator Visual Persona Schema v2'.
Return ONLY valid JSON matching the schema.

# Schema Reference
{SCHEMA_JSON}

# CRITICAL: Celebrity-Level Absolute Scoring Standard
All scores MUST be evaluated against the ABSOLUTE standard of top-tier Korean celebrity brand ambassadors, NOT relative to other creators.

The scoring baseline is defined by real soju CF celebrities:
- Chamisul 0.9+ = IU, Lee Young-ae level (National 'clean' image, zero scandal, pure innocent archetype)
- Chumchurum 0.9+ = Jennie, Lee Hyori level (Era-defining trendsetter, instant brand recall)
- Saero 0.9+ = Kim Ji-won, Jeon Yeo-been level (Intellectual chic, sophisticated modern image)
- Jinro 0.9+ = Son Ye-jin, Park Bo-gum level (Timeless classic, retro-modern crossover appeal)

For a typical Instagram/TikTok creator:
- brand_safety_score: Most creators should be 0.7-0.85 (celebrities with managed PR teams get 0.9+)
- soju_affinity_matrix: A creator rarely exceeds 0.5 for any brand unless they are a near-perfect visual/persona match. Average creators should be 0.15-0.35. Only exceptional fits reach 0.5-0.65.
- beauty_archetype scores: Evaluate against celebrity-grade visual presence. A typical creator should score 0.1-0.4 in most archetypes. Only give 0.6+ if they genuinely rival celebrity-level visual impact in that archetype.
- competitor_overlap_index: Be strict. If a creator has worked with or frequently features competitor products, this should be 0.5+.

Remember: A score of 0.7+ in soju_affinity means "this person could realistically be cast in a national TV commercial for this brand." Most social media creators cannot.

# Constraints
- Return ONLY valid JSON. No markdown fences, no explanation.
- Scores (0.0 to 1.0) must reflect the celebrity-level absolute standard above. Do NOT inflate scores.
- Infer facial details, skin texture, and color harmony based on their content style and demographics.
- Focus on how they fit into the 100-year Korean Soju brand evolution."""


def build_user_prompt(row: dict) -> str:
    return (
        f"Username: @{row.get('username', '')}\n"
        f"Full Name: {row.get('full_name', '')}\n"
        f"Biography: {row.get('biography', '')}\n"
        f"Categories: {row.get('categories', '')}\n"
        f"Subcategories: {row.get('subcategories', '')}\n"
        f"Gender: {row.get('gender', '')}\n"
        f"Age Group: {row.get('age_group', '')}\n"
        f"Ethnicity: {row.get('ethnicity', '')}\n"
        f"Country: {row.get('country', '')}\n"
        f"Primary Language: {row.get('primary_language', '')}\n"
        f"Followers: {row.get('followers_count', '')}\n"
        f"Posts: {row.get('posts_count', '')}\n"
        f"Engagement Rate: {row.get('engagement_rate_percentage', '')}%\n"
        f"Account Type: {row.get('account_type', '')}\n"
        f"Business Category: {row.get('business_category_name', '')}\n"
        f"Is Verified: {row.get('is_verified', '')}"
    )


def load_creators(csv_path: str, sample: int | None = None) -> list[dict]:
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for i, row in enumerate(reader):
            if sample and i >= sample:
                break
            rows.append(row)
    return rows


def upload_jsonl_to_gcs(creators: list[dict], batch_num: int) -> str:
    """Build JSONL requests and upload to GCS. Returns gcs_uri."""
    lines = []
    for row in creators:
        request = {
            "request": {
                "contents": [
                    {
                        "parts": [{"text": SYSTEM_PROMPT}],
                        "role": "user",
                    },
                    {
                        "parts": [{"text": build_user_prompt(row)}],
                        "role": "user",
                    },
                ],
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "temperature": 0.2,
                },
            }
        }
        lines.append(json.dumps(request, ensure_ascii=False))

    jsonl_content = "\n".join(lines)
    blob_name = f"{GCS_PREFIX}/input/batch_{batch_num}_{int(time.time())}.jsonl"

    gcs_client = storage.Client(project=GCP_PROJECT)
    bucket = gcs_client.bucket(GCS_BUCKET)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(jsonl_content, content_type="application/jsonl", timeout=600)

    gcs_uri = f"gs://{GCS_BUCKET}/{blob_name}"
    size_mb = len(jsonl_content.encode("utf-8")) / 1024 / 1024
    print(f"  Uploaded {len(lines)} requests ({size_mb:.1f} MB) to {gcs_uri}")
    return gcs_uri


def submit_and_wait(client: genai.Client, gcs_input_uri: str, display_name: str, batch_num: int) -> object:
    """Submit Vertex AI batch job and poll until done."""
    gcs_output_uri = f"gs://{GCS_BUCKET}/{GCS_PREFIX}/output/batch_{batch_num}_{int(time.time())}/"

    print(f"Submitting batch job '{display_name}'...")
    print(f"  Input:  {gcs_input_uri}")
    print(f"  Output: {gcs_output_uri}")

    job = client.batches.create(
        model=MODEL,
        src=gcs_input_uri,
        config={
            "display_name": display_name,
            "dest": gcs_output_uri,
        },
    )
    print(f"  Job created: {job.name}")

    completed = {"JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED"}
    max_retries = 5
    while True:
        print(f"  Status: {job.state.name} ... waiting {POLL_INTERVAL}s", flush=True)
        time.sleep(POLL_INTERVAL)
        for attempt in range(max_retries):
            try:
                job = client.batches.get(name=job.name)
                break
            except Exception as e:
                if attempt < max_retries - 1:
                    wait = 10 * (attempt + 1)
                    print(f"  Poll error (attempt {attempt+1}/{max_retries}): {e}. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    raise
        if job.state.name in completed:
            break

    print(f"  Final state: {job.state.name}")
    return job, gcs_output_uri


def download_results(gcs_output_uri: str, creators: list[dict]) -> list[dict]:
    """Download and parse batch results from GCS."""
    gcs_client = storage.Client(project=GCP_PROJECT)

    # Parse bucket and prefix from URI
    # gcs_output_uri = gs://bucket/prefix/
    path = gcs_output_uri.replace("gs://", "")
    bucket_name = path.split("/")[0]
    prefix = "/".join(path.split("/")[1:])

    bucket = gcs_client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=prefix))
    print(f"  Found {len(blobs)} output files in {gcs_output_uri}")

    results = []
    errors = 0
    for blob in blobs:
        if not blob.name.endswith(".jsonl"):
            continue
        content = blob.download_as_text()
        for line in content.strip().split("\n"):
            if not line.strip():
                continue
            try:
                resp = json.loads(line)
                # Vertex AI batch output format: each line has a response object
                candidates = resp.get("response", resp).get("candidates", [])
                if candidates:
                    text = candidates[0]["content"]["parts"][0]["text"]
                    parsed = json.loads(text)
                    # Handle case where model returns a list
                    if isinstance(parsed, list):
                        for item in parsed:
                            if isinstance(item, dict):
                                results.append(item)
                    elif isinstance(parsed, dict):
                        results.append(parsed)
                    else:
                        errors += 1
                else:
                    errors += 1
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                errors += 1

    print(f"  Parsed: {len(results)} OK, {errors} errors")

    # Ensure creator_id is set
    for i, r in enumerate(results):
        if not isinstance(r, dict):
            continue
        if "creator_id" not in r or not r["creator_id"]:
            username = creators[i].get("username", f"unknown_{i}") if i < len(creators) else f"unknown_{i}"
            r["creator_id"] = f"@{username}"

    return results


def evaluate_brand_fit(creator_data: dict, brand_namespace: str) -> dict:
    """Run brand guard scoring (same logic as tools.py)."""
    affinity_matrix = creator_data.get("brand_fit_logic", {}).get("soju_affinity_matrix", {})
    visual_archetype = creator_data.get("visual_persona_deep", {}).get("beauty_archetype", {})
    risk_mgmt = creator_data.get("risk_management", {})

    affinity_map = {
        "chamisul": affinity_matrix.get("chamisul_clean_index", 0),
        "chumchurum": affinity_matrix.get("chumchurum_soft_index", 0),
        "saero": affinity_matrix.get("saero_zero_hip_index", 0),
        "jinro": affinity_matrix.get("jinro_retro_index", 0),
    }
    affinity_score = affinity_map.get(brand_namespace, 0)

    visual_map = {
        "chamisul": (visual_archetype.get("pure_innocent", 0) + visual_archetype.get("healthy_vitality", 0)) / 2,
        "chumchurum": (visual_archetype.get("lovely_juicy", 0) + visual_archetype.get("moody_cinematic", 0)) / 2,
        "saero": (visual_archetype.get("hip_crush", 0) + visual_archetype.get("quirky_individualistic", 0)) / 2,
        "jinro": (visual_archetype.get("vintage_analog", 0) + visual_archetype.get("elegant_classic", 0)) / 2,
    }
    visual_score = visual_map.get(brand_namespace, 0)

    brand_safety = risk_mgmt.get("brand_safety_score", 0)
    competitor_overlap = risk_mgmt.get("competitor_overlap_index", 0)
    risk_score = (brand_safety + (1.0 - competitor_overlap)) / 2

    final_score = (affinity_score * 0.4) + (visual_score * 0.3) + (risk_score * 0.3)

    passed = final_score >= 0.7
    reason = "Meets strict brand-creator correlation threshold."
    if final_score < 0.7:
        reason = f"Final Score {final_score:.2f} is below strict threshold (0.70)."
    if competitor_overlap > 0.6:
        passed = False
        reason = f"Critical Risk: Competitor overlap ({competitor_overlap}) is too high."
    if brand_safety < 0.8:
        passed = False
        reason = f"Critical Risk: Brand safety score ({brand_safety}) is below 0.8."

    return {
        "creator_id": creator_data.get("creator_id", "unknown"),
        "brand": brand_namespace,
        "passed": passed,
        "final_score": round(final_score, 3),
        "affinity": round(affinity_score, 3),
        "visual": round(visual_score, 3),
        "risk": round(risk_score, 3),
        "reason": reason,
    }


def print_evaluation_summary(vectorized: list[dict]):
    brands = ["chamisul", "chumchurum", "saero", "jinro"]
    all_evals = []

    for v in vectorized:
        for b in brands:
            all_evals.append(evaluate_brand_fit(v, b))

    # Print per-creator
    print(f"\n{'='*130}")
    print(f"{'Creator':25s} {'Brand':12s} {'Status':6s} {'Score':7s} {'Aff':6s} {'Vis':6s} {'Risk':6s} Reason")
    print(f"{'-'*130}")

    for e in all_evals:
        status = "PASS" if e["passed"] else "FAIL"
        print(f"{e['creator_id']:25s} {e['brand']:12s} {status:6s} {e['final_score']:.3f}   {e['affinity']:.3f}  {e['visual']:.3f}  {e['risk']:.3f}  {e['reason']}")

    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY:")
    for b in brands:
        b_evals = [e for e in all_evals if e["brand"] == b]
        passed = sum(1 for e in b_evals if e["passed"])
        total = len(b_evals)
        avg_score = sum(e["final_score"] for e in b_evals) / total if total else 0
        print(f"  {b:12s}: {passed:3d} PASS / {total - passed:3d} FAIL (avg score {avg_score:.3f})")

    return all_evals


def main():
    parser = argparse.ArgumentParser(description="Batch vectorize creators via Vertex AI Batch Prediction")
    parser.add_argument("--sample", type=int, default=None, help="Sample N creators (default: all)")
    parser.add_argument("--csv", default=INSTAGRAM_CSV, help="Path to creator CSV")
    parser.add_argument("--output", default=None, help="Output JSON path (auto-generated if not set)")
    parser.add_argument("--batch-size", type=int, default=500, help="Max requests per batch job")
    args = parser.parse_args()

    client = genai.Client(vertexai=True, project=GCP_PROJECT, location="global")

    # Load creators
    creators = load_creators(args.csv, sample=args.sample)
    print(f"Loaded {len(creators)} creators from {args.csv}")

    # Process in batches
    all_vectorized = []
    for batch_start in range(0, len(creators), args.batch_size):
        batch_end = min(batch_start + args.batch_size, len(creators))
        batch_creators = creators[batch_start:batch_end]
        batch_num = batch_start // args.batch_size + 1

        # Upload JSONL to GCS
        gcs_input_uri = upload_jsonl_to_gcs(batch_creators, batch_num)
        display_name = f"creator-vectorize-batch-{batch_num}"

        # Submit and wait
        job, gcs_output_uri = submit_and_wait(client, gcs_input_uri, display_name, batch_num)

        if job.state.name == "JOB_STATE_SUCCEEDED":
            results = download_results(gcs_output_uri, batch_creators)
            all_vectorized.extend(results)
            print(f"  Batch {batch_num}: {len(results)}/{len(batch_creators)} succeeded")
        else:
            print(f"  Batch {batch_num}: FAILED ({job.state.name})")

    # Save results
    suffix = f"_sample{args.sample}" if args.sample else ""
    platform = "instagram" if "instagram" in args.csv else "tiktok"
    output_path = args.output or f"data/vectorized_{platform}_creators{suffix}.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_vectorized, f, ensure_ascii=False, indent=2)
    print(f"\nSaved {len(all_vectorized)} vectorized creators to {output_path}")

    # Evaluate
    print_evaluation_summary(all_vectorized)


if __name__ == "__main__":
    main()
