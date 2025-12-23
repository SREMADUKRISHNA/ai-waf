import json
from fastapi import APIRouter
from config.settings import LOG_FILE
from typing import List, Dict

router = APIRouter()

@router.get("/api/dashboard/stats")
async def get_stats():
    """
    Returns aggregated stats for the dashboard.
    """
    total_blocked = 0
    attack_types = {}
    recent_attacks = []
    
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r') as f:
            for line in f:
                try:
                    # Parse log format: "YYYY-MM-DD HH:MM:SS... - {json}"
                    # We look for the first '{'
                    json_part_idx = line.find('{')
                    if json_part_idx != -1:
                        data = json.loads(line[json_part_idx:])
                        total_blocked += 1
                        
                        atype = data.get("attack_type", "Unknown")
                        attack_types[atype] = attack_types.get(atype, 0) + 1
                        
                        recent_attacks.append(data)
                except Exception:
                    continue
    
    # Sort recent attacks by timestamp desc
    recent_attacks.sort(key=lambda x: x.get('timestamp', 0), reverse=True)
    
    return {
        "total_blocked": total_blocked,
        "attack_distribution": attack_types,
        "recent_attacks": recent_attacks[:10]
    }
