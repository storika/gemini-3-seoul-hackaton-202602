import os
import json
import clickhouse_connect
from google import genai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# ClickHouse Connection
def get_clickhouse_client():
    return clickhouse_connect.get_client(
        host='goyxu9pwfe.us-central1.gcp.clickhouse.cloud',
        port=443,
        username='default',
        password='ZRdOt.SZq3AKG',
        database='default',
        secure=True
    )

# Gemini Client
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    # Try loading from .env manually if os.environ fails
    try:
        with open(".env", "r") as f:
            for line in f:
                if line.startswith("GOOGLE_API_KEY"):
                    api_key = line.split("=")[1].strip().strip('"').strip("'")
                    break
    except:
        pass

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment or .env file")

client = genai.Client(api_key=api_key)

# Load Schema for reference in prompt
with open('data/schemas/creator_feature_vector.schema.json', 'r') as f:
    schema_json = f.read()

def vectorize_creator(creator_data):
    prompt = f"""
    # Role: Senior Visual Brand Strategist & AI Persona Architect (Korean Soju Industry)

    # Task
    Convert the following TikTok creator data into the 'Hyper-Detailed Creator Visual Persona Schema v2'.

    # Input Data
    - Username: {creator_data.get('username')}
    - Nickname: {creator_data.get('nickname')}
    - Summary: {creator_data.get('summary')}
    - Categories: {creator_data.get('categories')}
    - Archetypes: {creator_data.get('creator_archetypes')}
    - Bio/Signature: {creator_data.get('signature')}
    - Primary Language/Country: {creator_data.get('primary_language')} / {creator_data.get('primary_country')}

    # Schema Reference
    {schema_json}

    # CRITICAL: Celebrity-Level Absolute Scoring Standard
    All scores MUST be evaluated against the ABSOLUTE standard of top-tier Korean celebrity brand ambassadors, NOT relative to other creators.

    The scoring baseline is defined by real soju CF celebrities:
    - Chamisul 0.9+ = IU, Lee Young-ae level (National 'clean' image, zero scandal, pure innocent archetype)
    - Chumchurum 0.9+ = Jennie, Lee Hyori level (Era-defining trendsetter, instant brand recall)
    - Saero 0.9+ = Kim Ji-won, Jeon Yeo-been level (Intellectual chic, sophisticated modern image)
    - Jinro 0.9+ = Son Ye-jin, Park Bo-gum level (Timeless classic, retro-modern crossover appeal)

    For a typical TikTok creator:
    - brand_safety_score: Most creators should be 0.7-0.85 (celebrities with managed PR teams get 0.9+)
    - soju_affinity_matrix: A creator rarely exceeds 0.5 for any brand unless they are a near-perfect visual/persona match. Average creators should be 0.15-0.35. Only exceptional fits reach 0.5-0.65.
    - beauty_archetype scores: Evaluate against celebrity-grade visual presence. A typical creator should score 0.1-0.4 in most archetypes. Only give 0.6+ if they genuinely rival celebrity-level visual impact in that archetype.
    - competitor_overlap_index: Be strict. If a creator has worked with or frequently features competitor products, this should be 0.5+.

    Remember: A score of 0.7+ in soju_affinity means "this person could realistically be cast in a national TV commercial for this brand." Most TikTok creators cannot.

    # Constraints
    - Return ONLY valid JSON.
    - Scores (0.0 to 1.0) must reflect the celebrity-level absolute standard above. Do NOT inflate scores.
    - Infer facial details, skin texture, and color harmony based on their content style and demographics.
    - Focus on how they fit into the 100-year Korean Soju brand evolution.
    """
    
    response = client.models.generate_content(
        model='gemini-2.0-flash-lite',
        contents=prompt,
        config={
            'response_mime_type': 'application/json'
        }
    )
    return json.loads(response.text)

def main():
    ch_client = get_clickhouse_client()
    print("Fetching 10 Korean creators from ClickHouse...")
    # Filter for Korean creators if possible
    query = """
    SELECT * FROM tiktok_profiles 
    WHERE (primary_country = 'KR' OR primary_language = 'ko') 
    AND summary != '' 
    LIMIT 10
    """
    sample = ch_client.query(query).result_rows
    columns = [col[0] for col in ch_client.query("DESCRIBE TABLE tiktok_profiles").result_rows]
    creators = [dict(zip(columns, row)) for row in sample]
    
    if not creators:
        print("No Korean creators found with summary, fetching generic samples...")
        creators = [dict(zip(columns, row)) for row in ch_client.query("SELECT * FROM tiktok_profiles WHERE summary != '' LIMIT 10").result_rows]

    vectorized_results = []
    for i, creator in enumerate(creators):
        print(f"Vectorizing {i+1}/{len(creators)}: @{creator['username']}...")
        try:
            vector = vectorize_creator(creator)
            vectorized_results.append(vector)
        except Exception as e:
            print(f"Error vectorizing {creator['username']}: {e}")
            
    output_path = 'data/vectorized_clickhouse_samples.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(vectorized_results, f, ensure_ascii=False, indent=2)
    
    print(f"\nSuccessfully vectorized {len(vectorized_results)} creators.")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    main()
