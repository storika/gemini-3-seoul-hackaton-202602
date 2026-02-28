from src.agents.brand_guard.tools import verify_creator_brand_fit

def test_strict_fit_chamisul_real_beauty():
    # Mock data for @real.beauty5
    creator_data = {
        "creator_id": "@real.beauty5",
        "visual_persona_deep": {
            "beauty_archetype": {
                "pure_innocent": 0.2,
                "healthy_vitality": 0.7
            }
        },
        "brand_fit_logic": {
            "soju_affinity_matrix": {
                "chamisul_clean_index": 0.7
            }
        },
        "risk_management": {
            "brand_safety_score": 0.9,
            "competitor_overlap_index": 0.4
        }
    }
    
    result = verify_creator_brand_fit("chamisul", creator_data)
    print(f"Result for @real.beauty5 (Chamisul): {result['passed']} (Score: {result['final_score']})")
    assert result['passed'] is False
    assert result['final_score'] < 0.7

def test_strict_fit_saero_chrlsty():
    # Mock data for @chrlsty
    creator_data = {
        "creator_id": "@chrlsty",
        "visual_persona_deep": {
            "beauty_archetype": {
                "hip_crush": 0.9,
                "quirky_individualistic": 0.8
            }
        },
        "brand_fit_logic": {
            "soju_affinity_matrix": {
                "saero_zero_hip_index": 0.8
            }
        },
        "risk_management": {
            "brand_safety_score": 0.9,
            "competitor_overlap_index": 0.6
        }
    }
    
    result = verify_creator_brand_fit("saero", creator_data)
    print(f"Result for @chrlsty (Saero): {result['passed']} (Score: {result['final_score']})")
    assert result['passed'] is True
    assert result['final_score'] >= 0.7

if __name__ == "__main__":
    test_strict_fit_chamisul_real_beauty()
    test_strict_fit_saero_chrlsty()
    print("All strict fit tests passed!")
