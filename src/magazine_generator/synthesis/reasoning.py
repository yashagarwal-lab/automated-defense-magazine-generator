from typing import Dict, Any

def generate_editorial_reasoning(rec: Dict[str, Any], category: str) -> str:
    """Generate analytical editorial rationale explaining why an article was selected."""
    title = rec.get("title", "").lower()
    text = (title + " " + rec.get("description", "")).lower()

    if category == "Security & Strategic Affairs":
        if "manipur" in text or "kangpokpi" in text:
            return "Demonstrates the Army and Assam Rifles joint intelligence and counter-insurgency operations restoring stability in Manipur."
        if "arunachal" in text or "tawang" in text or "lac" in text:
            return "Highlights forward defense posture, strategic vigilance, and infrastructure readiness along the Line of Actual Control."
        if "ambush" in text or "encounter" in text or "militant" in text:
            return "Illustrates the active threat matrix, rapid tactical reinforcement, and operational resilience of security forces in border sectors."
        return "Selected to illustrate the multifaceted security architecture and operational preparedness of the Eastern Command."

    if category == "Regional News & Development":
        if "bro" in text or "border roads" in text or "tunnel" in text:
            return "Highlights Border Roads Organisation’s rapid strategic connectivity drives enhancing military logistics and civilian access."
        if "flood" in text or "rescue" in text or "disaster" in text:
            return "Demonstrates Armed Forces Humanitarian Assistance and Disaster Relief (HADR) operations during regional climate emergencies."
        return "Showcases dual-use civil-military infrastructure projects accelerating economic integration across Northeast frontier corridors."

    if category == "Society & Youth Empowerment":
        if "ncc" in text or "cadet" in text:
            return "Focuses on National Cadet Corps leadership camps cultivating discipline, national integration, and defense career pathways."
        if "school" in text or "education" in text or "sadbhavana" in text:
            return "Showcases Operation Sadbhavana and Army Goodwill School initiatives expanding educational opportunities in remote border belts."
        return "Highlights grassroots civic engagement, skill development, and youth empowerment initiatives by security forces."

    if category == "Sports & Achievements":
        if "durand" in text or "football" in text:
            return "Celebrates Armed Forces-led historic sporting institutions like the Durand Cup fostering athletic excellence and community unity."
        if "hockey" in text or "tournament" in text:
            return "Highlights regional sporting tournaments organized by Assam Rifles identifying and nurturing grassroots athletic talent."
        return "Underscores the Armed Forces’ commitment to promoting sportsmanship and regional representation on national podiums."

    return "Curated as a verified primary development within the Eastern Theatre’s operational jurisdiction."
