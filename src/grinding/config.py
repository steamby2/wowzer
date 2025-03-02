# Configuration for Level 1 Hunter - Elwynn Forest

# Recommended targets (English names)
TARGETS = [
    "Young_Wolf",  # Level 1-2
    "Rabbit",             # Level 1
    "Kobold Worker",      # Level 1-3
    "Defias Thug",        # Level 1-2
]

# Waypoints for Elwynn Forest (near Northshire Abbey)
ELWYNN_STARTING_WAYPOINTS = [
    # Coordinates near starting area
    # These values should be adjusted based on your screen resolution
    (800, 400),   # Near the Abbey
    (850, 450),   # Path toward wolves
    (900, 500),   # Wolf area to the east
    (800, 550),   # Back toward south
    (750, 500)    # Complete the loop
]

# Combat configuration for Level 1 Hunter
HUNTER_LEVEL1_ABILITIES = {
    "auto_shot": {
        "key": "1",     # Key for Auto Shot
        "cooldown": 0,  # No cooldown, it's auto
        "range": "far"  # Preferred distance
    },
    "raptor_strike": {
        "key": "2",     # Key for Raptor Strike (if available)
        "cooldown": 6,  # Cooldown in seconds
        "range": "melee" # Melee range
    }
}

# General settings
SETTINGS = {
    "combat_distance": 15,    # Distance to start combat (in pixels)
    "rest_threshold": 50,     # Health % to rest
    "grinding_radius": 100,   # Radius to search for enemies
    "avoid_level": 3,         # Avoid mobs with level > player level + this value
    "target_priority": [      # Target priority order
        "Young Forest Wolf",
        "Kobold Worker",
        "Defias Thug"
    ]
}

# Detection thresholds
DETECTION = {
    "enemy_confidence": 0.65,  # Confidence threshold for enemy detection
    "health_low": 60,          # Health % considered "low"
    "loot_radius": 30          # Search radius for loot in pixels
}