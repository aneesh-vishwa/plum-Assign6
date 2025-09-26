# src/services/risk_engine.py

from typing import Dict, Any, List, Tuple

def extract_factors(answers: Dict[str, Any]) -> List[str]:
    """Converts survey answers into a list of health risk factors."""
    factors = []
    if answers.get("smoker"):
        factors.append("smoking")
    
    if answers.get("diet") in ["high sugar", "high fat", "processed"]:
        factors.append("poor diet")
        
    if answers.get("exercise") in ["rarely", "never"]:
        factors.append("low exercise")
        
    if answers.get("age", 0) > 60:
        factors.append("advanced age")
        
    return factors

def calculate_risk(factors: List[str]) -> Dict[str, Any]:
    """Computes a risk level and score based on a simple scoring logic."""
    score = 0
    score_map = {
        "smoking": 35,
        "poor diet": 25,
        "low exercise": 20,
        "advanced age": 10,
    }
    
    for factor in factors:
        score += score_map.get(factor, 0)
        
    if score >= 70:
        risk_level = "high"
    elif score >= 40:
        risk_level = "medium"
    else:
        risk_level = "low"
        
    return {"risk_level": risk_level, "score": score, "rationale": factors}

def generate_recommendations(factors: List[str]) -> List[str]:
    """Generates actionable, non-diagnostic guidance based on risk factors."""
    recommendations = []
    rec_map = {
        "smoking": "Consider resources for quitting smoking.",
        "poor diet": "Try to incorporate more whole foods and reduce sugar intake.",
        "low exercise": "Aim for a 30-minute walk on most days of the week.",
        "advanced age": "Discuss regular health screenings with your doctor."
    }
    
    if not factors:
        return ["Maintain your healthy lifestyle and continue with regular check-ups."]
        
    for factor in factors:
        if factor in rec_map:
            recommendations.append(rec_map[factor])
            
    return recommendations