import pygame

pygame.init()

# --------------------------------------------------
# WINDOW SETTINGS
# --------------------------------------------------

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
BASE_WIDTH = 320
BASE_HEIGHT = 180
SCALE = 3
FPS = 60

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cybersecurity Attack")
canvas = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
clock = pygame.time.Clock()

# --------------------------------------------------
# COLORS
# --------------------------------------------------

BACKGROUND = (10, 12, 24)
DARK_BLUE = (15, 25, 45)
PANEL_BLUE = (21, 34, 56)
WALL = (30, 40, 57)
WALL_DARK = (22, 30, 44)
FLOOR = (24, 29, 42)
FLOOR_LINE = (40, 48, 66)
BLACK = (6, 8, 14)
CYAN = (54, 238, 255)
GREEN = (78, 255, 132)
WHITE = (240, 240, 240)
GRAY = (135, 145, 165)
PINK = (255, 73, 173)
YELLOW = (255, 222, 89)
RED = (255, 77, 77)
ORANGE = (255, 155, 65)
PURPLE = (165, 100, 255)

# --------------------------------------------------
# FONTS
# --------------------------------------------------

# Pixel fonts are used for large retro headings.
title_font = pygame.font.Font(None, 42)
subtitle_font = pygame.font.Font(None, 22)
small_pixel_font = pygame.font.Font(None, 14)
room_pixel_font = pygame.font.Font(None, 26)

# High-resolution text is rendered after scaling so it remains readable.
hud_heading_font = pygame.font.SysFont("consolas", 27, bold=True)
hud_body_font = pygame.font.SysFont("consolas", 18)
hud_body_bold = pygame.font.SysFont("consolas", 18, bold=True)
hud_small_font = pygame.font.SysFont("consolas", 16, bold=True)
hud_tiny_font = pygame.font.SysFont("consolas", 13, bold=True)
hud_status_font = pygame.font.SysFont("consolas", 20, bold=True)
hud_inventory_font = pygame.font.SysFont("consolas", 17, bold=True)

# --------------------------------------------------
# GAME DATA
# --------------------------------------------------

game_state = "title"
current_room = "Main Lobby"
inventory = []
collected_items = set()

player_x = 95
player_y = 91
player_speed = 1
player_direction = "down"
walk_frame = 0
walk_timer = 0
is_walking = False

frame_counter = 0
interaction_message = ""
message_timer = 0

transition_active = False
transition_alpha = 0
transition_phase = "out"
transition_target = None
transition_direction = None

rooms = {
    "Main Lobby": {
        "description": [
            "Emergency systems are active.",
            "The building is under attack.",
            "Recover all 6 security tools."
        ],
        "north": "Control Room",
        "west": "Security Office"
    },
    "Security Office": {
        "description": [
            "Security consoles are online.",
            "Authentication logs are open.",
            "Search for the MFA Token."
        ],
        "east": "Main Lobby",
        "north": "Network Operations Center",
        "item": "MFA Token"
    },
    "Network Operations Center": {
        "description": [
            "Network traffic is unstable.",
            "Firewall alerts fill the screens.",
            "Locate the Firewall Key."
        ],
        "south": "Security Office",
        "north": "IT Office",
        "item": "Firewall Key"
    },
    "IT Office": {
        "description": [
            "Workstations show update errors.",
            "A critical patch is available.",
            "Recover the Security Patch."
        ],
        "south": "Network Operations Center",
        "east": "Server Room",
        "item": "Security Patch"
    },
    "Server Room": {
        "description": [
            "Server racks hum under load.",
            "Backup systems are isolated.",
            "Find the Backup Drive."
        ],
        "west": "IT Office",
        "east": "Data Center",
        "item": "Backup Drive"
    },
    "Data Center": {
        "description": [
            "Encrypted traffic fills the core.",
            "Cooling systems are strained.",
            "Recover the Encryption Key."
        ],
        "west": "Server Room",
        "south": "Admin Office",
        "item": "Encryption Key"
    },
    "Admin Office": {
        "description": [
            "Executive systems are locked.",
            "Access controls are restricted.",
            "Find the Access Card."
        ],
        "north": "Data Center",
        "west": "Control Room",
        "item": "Access Card"
    },
    "Control Room": {
        "description": [
            "The Ransomware Bot is here.",
            "Every tool is required.",
            "This is the final encounter."
        ],
        "south": "Main Lobby",
        "east": "Admin Office"
    }
}

ITEM_DATA = {
    "MFA Token": {"label": "MFA", "color": GREEN},
    "Firewall Key": {"label": "FW", "color": ORANGE},
    "Security Patch": {"label": "PATCH", "color": CYAN},
    "Backup Drive": {"label": "BACKUP", "color": PURPLE},
    "Encryption Key": {"label": "ENC", "color": YELLOW},
    "Access Card": {"label": "CARD", "color": PINK},
}

DOOR_LABELS = {
    "Control Room": "CTRL",
    "Security Office": "SEC",
    "Main Lobby": "LOBBY",
    "Network Operations Center": "NET",
    "IT Office": "IT",
    "Server Room": "SERVER",
    "Data Center": "DATA",
    "Admin Office": "ADMIN",
}

door_progress = {
    (room_name, direction): 0.0
    for room_name, room_data in rooms.items()
    for direction in ("north", "south", "east", "west")
    if direction in room_data
}

# --------------------------------------------------
# SHARED HELPERS
# --------------------------------------------------


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def draw_pixel_lock(surface, x, y):
    """Draw a simple pixel-style cybersecurity lock."""
    pygame.draw.rect(surface, YELLOW, (x, y + 8, 24, 20))
    pygame.draw.rect(surface, BACKGROUND, (x + 9, y + 15, 6, 8))
    pygame.draw.rect(surface, YELLOW, (x + 5, y + 2, 14, 4))
    pygame.draw.rect(surface, YELLOW, (x + 3, y + 4, 4, 8))
    pygame.draw.rect(surface, YELLOW, (x + 17, y + 4, 4, 8))

def draw_player(surface, x, y, direction, walk_frame, is_walking):
    """Draw the animated pixel-art cybersecurity analyst."""

    # Character palette.
    skin = (232, 184, 145)
    skin_light = (244, 199, 158)
    skin_shadow = (196, 137, 99)
    hair = (79, 48, 29)
    hair_light = (112, 68, 38)
    eye = (18, 16, 20)
    hoodie = (25, 34, 52)
    hoodie_light = (42, 57, 78)
    shirt = (36, 210, 220)
    shirt_dark = (20, 142, 154)
    pants = (20, 28, 43)
    shoes = (105, 118, 137)
    mouth = (116, 65, 58)

    # A tiny vertical bounce makes the walking cycle feel less static.
    bob = -1 if is_walking and walk_frame == 1 else 0
    y += bob

    # Alternate arm and leg positions while walking.
    left_step = 1 if is_walking and walk_frame == 0 else 0
    right_step = 1 if is_walking and walk_frame == 1 else 0

    # Floor shadow.
    pygame.draw.rect(surface, (10, 13, 21), (x + 4, y + 30, 15, 2))

    if direction == "up":
        # Back of head and hair.
        pygame.draw.rect(surface, hair, (x + 5, y, 12, 3))
        pygame.draw.rect(surface, hair, (x + 3, y + 2, 16, 7))
        pygame.draw.rect(surface, hair_light, (x + 5, y + 2, 4, 1))
        pygame.draw.rect(surface, skin_shadow, (x + 6, y + 9, 10, 5))

        # Hood and shoulders.
        pygame.draw.rect(surface, hoodie_light, (x + 3, y + 14, 16, 5))
        pygame.draw.rect(surface, hoodie, (x + 4, y + 17, 14, 9))
        pygame.draw.rect(surface, hoodie_light, (x + 7, y + 16, 8, 3))

        # Small cyan security emblem on the back.
        pygame.draw.rect(surface, shirt, (x + 9, y + 20, 4, 4))
        pygame.draw.rect(surface, shirt_dark, (x + 10, y + 21, 2, 2))

        # Arms swing opposite the legs.
        pygame.draw.rect(surface, hoodie, (x + 1, y + 18 + right_step, 3, 7))
        pygame.draw.rect(surface, hoodie, (x + 18, y + 18 + left_step, 3, 7))
        pygame.draw.rect(surface, skin_shadow, (x + 1, y + 25 + right_step, 3, 2))
        pygame.draw.rect(surface, skin_shadow, (x + 18, y + 25 + left_step, 3, 2))

    elif direction == "left":
        # Side-facing hair and face.
        pygame.draw.rect(surface, hair, (x + 5, y, 11, 3))
        pygame.draw.rect(surface, hair, (x + 3, y + 2, 13, 5))
        pygame.draw.rect(surface, hair, (x + 3, y + 5, 3, 5))
        pygame.draw.rect(surface, hair_light, (x + 5, y + 1, 4, 1))
        pygame.draw.rect(surface, skin, (x + 5, y + 5, 10, 10))
        pygame.draw.rect(surface, skin_light, (x + 5, y + 6, 2, 3))
        pygame.draw.rect(surface, eye, (x + 6, y + 8, 2, 2))
        pygame.draw.rect(surface, WHITE, (x + 6, y + 8, 1, 1))
        pygame.draw.rect(surface, skin_shadow, (x + 4, y + 10, 2, 2))
        pygame.draw.rect(surface, mouth, (x + 5, y + 13, 3, 1))

        # Neck, hoodie, and shirt edge.
        pygame.draw.rect(surface, skin_shadow, (x + 9, y + 15, 4, 2))
        pygame.draw.rect(surface, hoodie_light, (x + 4, y + 16, 14, 3))
        pygame.draw.rect(surface, hoodie, (x + 5, y + 18, 13, 8))
        pygame.draw.rect(surface, shirt, (x + 5, y + 19, 3, 5))
        pygame.draw.rect(surface, shirt_dark, (x + 5, y + 21, 2, 2))

        # Arms: front arm is more visible in profile.
        pygame.draw.rect(surface, hoodie, (x + 2, y + 18 + right_step, 3, 7))
        pygame.draw.rect(surface, skin, (x + 1, y + 24 + right_step, 3, 2))
        pygame.draw.rect(surface, hoodie_light, (x + 16, y + 19 + left_step, 2, 6))

    elif direction == "right":
        # Side-facing hair and face mirrored to the right.
        pygame.draw.rect(surface, hair, (x + 6, y, 11, 3))
        pygame.draw.rect(surface, hair, (x + 6, y + 2, 13, 5))
        pygame.draw.rect(surface, hair, (x + 16, y + 5, 3, 5))
        pygame.draw.rect(surface, hair_light, (x + 12, y + 1, 4, 1))
        pygame.draw.rect(surface, skin, (x + 7, y + 5, 10, 10))
        pygame.draw.rect(surface, skin_light, (x + 15, y + 6, 2, 3))
        pygame.draw.rect(surface, eye, (x + 14, y + 8, 2, 2))
        pygame.draw.rect(surface, WHITE, (x + 15, y + 8, 1, 1))
        pygame.draw.rect(surface, skin_shadow, (x + 16, y + 10, 2, 2))
        pygame.draw.rect(surface, mouth, (x + 14, y + 13, 3, 1))

        # Neck, hoodie, and shirt edge.
        pygame.draw.rect(surface, skin_shadow, (x + 9, y + 15, 4, 2))
        pygame.draw.rect(surface, hoodie_light, (x + 4, y + 16, 14, 3))
        pygame.draw.rect(surface, hoodie, (x + 4, y + 18, 13, 8))
        pygame.draw.rect(surface, shirt, (x + 14, y + 19, 3, 5))
        pygame.draw.rect(surface, shirt_dark, (x + 15, y + 21, 2, 2))

        # Arms: front arm is more visible in profile.
        pygame.draw.rect(surface, hoodie, (x + 17, y + 18 + left_step, 3, 7))
        pygame.draw.rect(surface, skin, (x + 19, y + 24 + left_step, 3, 2))
        pygame.draw.rect(surface, hoodie_light, (x + 4, y + 19 + right_step, 2, 6))

    else:
        # Front-facing ears.
        pygame.draw.rect(surface, skin_shadow, (x + 3, y + 7, 2, 4))
        pygame.draw.rect(surface, skin_shadow, (x + 17, y + 7, 2, 4))

        # Face.
        pygame.draw.rect(surface, skin, (x + 5, y + 4, 12, 11))
        pygame.draw.rect(surface, skin_shadow, (x + 5, y + 13, 12, 2))
        pygame.draw.rect(surface, skin_light, (x + 6, y + 5, 3, 2))

        # Hair with an uneven fringe and highlights.
        pygame.draw.rect(surface, hair, (x + 5, y, 11, 2))
        pygame.draw.rect(surface, hair, (x + 3, y + 2, 15, 3))
        pygame.draw.rect(surface, hair, (x + 3, y + 4, 3, 5))
        pygame.draw.rect(surface, hair, (x + 16, y + 4, 3, 4))
        pygame.draw.rect(surface, hair, (x + 6, y + 4, 4, 2))
        pygame.draw.rect(surface, hair, (x + 13, y + 4, 3, 1))
        pygame.draw.rect(surface, hair_light, (x + 6, y + 1, 4, 1))
        pygame.draw.rect(surface, hair_light, (x + 4, y + 3, 3, 1))

        # Eyebrows, eyes, nose, and mouth.
        pygame.draw.rect(surface, hair, (x + 7, y + 7, 2, 1))
        pygame.draw.rect(surface, hair, (x + 13, y + 7, 2, 1))
        pygame.draw.rect(surface, eye, (x + 7, y + 8, 2, 2))
        pygame.draw.rect(surface, eye, (x + 13, y + 8, 2, 2))
        pygame.draw.rect(surface, WHITE, (x + 7, y + 8, 1, 1))
        pygame.draw.rect(surface, WHITE, (x + 13, y + 8, 1, 1))
        pygame.draw.rect(surface, skin_shadow, (x + 10, y + 10, 2, 2))
        pygame.draw.rect(surface, mouth, (x + 9, y + 13, 4, 1))

        # Neck and hoodie.
        pygame.draw.rect(surface, skin_shadow, (x + 9, y + 15, 4, 2))
        pygame.draw.rect(surface, hoodie_light, (x + 3, y + 16, 16, 3))
        pygame.draw.rect(surface, hoodie, (x + 4, y + 18, 14, 8))
        pygame.draw.rect(surface, hoodie_light, (x + 4, y + 18, 2, 7))
        pygame.draw.rect(surface, hoodie_light, (x + 16, y + 18, 2, 7))

        # Shirt and hoodie details.
        pygame.draw.rect(surface, shirt, (x + 9, y + 18, 4, 6))
        pygame.draw.rect(surface, shirt_dark, (x + 10, y + 20, 2, 3))
        pygame.draw.rect(surface, WHITE, (x + 8, y + 18, 1, 3))
        pygame.draw.rect(surface, WHITE, (x + 13, y + 18, 1, 3))

        # Arms swing while moving.
        pygame.draw.rect(surface, hoodie, (x + 1, y + 18 + right_step, 3, 7))
        pygame.draw.rect(surface, hoodie, (x + 18, y + 18 + left_step, 3, 7))
        pygame.draw.rect(surface, hoodie_light, (x + 1, y + 23 + right_step, 3, 2))
        pygame.draw.rect(surface, hoodie_light, (x + 18, y + 23 + left_step, 3, 2))
        pygame.draw.rect(surface, skin, (x + 1, y + 25 + right_step, 3, 2))
        pygame.draw.rect(surface, skin, (x + 18, y + 25 + left_step, 3, 2))

        # Cybersecurity badge.
        pygame.draw.rect(surface, CYAN, (x + 14, y + 20, 3, 4))
        pygame.draw.rect(surface, GREEN, (x + 15, y + 21, 1, 1))

    # Legs are shared by all directions and alternate during movement.
    pygame.draw.rect(surface, pants, (x + 6, y + 26 + left_step, 5, 4))
    pygame.draw.rect(surface, pants, (x + 12, y + 26 + right_step, 5, 4))

    # Shoes shift with the walking cycle.
    pygame.draw.rect(surface, shoes, (x + 5, y + 29 + left_step, 6, 2))
    pygame.draw.rect(surface, shoes, (x + 12, y + 29 + right_step, 6, 2))
    pygame.draw.rect(surface, WHITE, (x + 6, y + 29 + left_step, 2, 1))
    pygame.draw.rect(surface, WHITE, (x + 13, y + 29 + right_step, 2, 1))

# --------------------------------------------------
# ROOM / DOOR HELPERS
# --------------------------------------------------


def direction_door_rect(direction):
    """Return the base-resolution rectangle used for a room exit."""
    if direction == "north":
        return pygame.Rect(84, 49, 48, 48)
    if direction == "south":
        return pygame.Rect(84, 96, 48, 29)
    if direction == "west":
        return pygame.Rect(16, 68, 25, 29)
    return pygame.Rect(173, 68, 25, 29)


def is_near_door(direction, x=None, y=None):
    """Return True when the player is close enough for a door to open."""
    if x is None:
        x = player_x
    if y is None:
        y = player_y

    center_x = x + 11
    center_y = y + 16

    if direction == "north":
        return 84 <= center_x <= 132 and center_y <= 88
    if direction == "south":
        return 84 <= center_x <= 132 and center_y >= 102
    if direction == "west":
        return center_x <= 49 and 72 <= center_y <= 113
    if direction == "east":
        return center_x >= 171 and 72 <= center_y <= 113
    return False


def nearest_interaction():
    """Return the current interaction type and associated value."""
    room = rooms[current_room]
    room_item = room.get("item")

    if room_item and room_item not in collected_items:
        item_x, item_y = item_position(current_room)
        player_center = pygame.Vector2(player_x + 11, player_y + 16)
        item_center = pygame.Vector2(item_x + 6, item_y + 6)
        if player_center.distance_to(item_center) <= 24:
            return "item", room_item

    for direction in ("north", "south", "west", "east"):
        if direction in room and is_near_door(direction):
            return "door", direction

    return None, None


def update_door_animations():
    """Automatically open nearby doors and close distant doors."""
    for direction in ("north", "south", "west", "east"):
        key = (current_room, direction)
        if key not in door_progress:
            continue

        target = 1.0 if is_near_door(direction) else 0.0
        speed = 0.09

        if door_progress[key] < target:
            door_progress[key] = min(target, door_progress[key] + speed)
        elif door_progress[key] > target:
            door_progress[key] = max(target, door_progress[key] - speed)


def spawn_from_direction(direction):
    """Place the player near the matching entry door after a transition."""
    global player_x, player_y, player_direction

    if direction == "north":
        player_x, player_y, player_direction = 97, 91, "up"
    elif direction == "south":
        player_x, player_y, player_direction = 97, 64, "down"
    elif direction == "west":
        player_x, player_y, player_direction = 158, 80, "left"
    elif direction == "east":
        player_x, player_y, player_direction = 29, 80, "right"


def start_room_transition(target_room, direction):
    """Begin a short fade transition into another room."""
    global transition_active, transition_alpha
    global transition_phase, transition_target, transition_direction

    transition_active = True
    transition_alpha = 0
    transition_phase = "out"
    transition_target = target_room
    transition_direction = direction


def update_transition():
    """Update the fade-out / fade-in room transition."""
    global transition_active, transition_alpha, transition_phase
    global current_room

    if not transition_active:
        return

    if transition_phase == "out":
        transition_alpha += 24
        if transition_alpha >= 255:
            transition_alpha = 255
            current_room = transition_target
            spawn_from_direction(transition_direction)
            transition_phase = "in"
    else:
        transition_alpha -= 24
        if transition_alpha <= 0:
            transition_alpha = 0
            transition_active = False


def reset_game():
    """Restore the enhanced game to its initial playable state."""
    global game_state, current_room, inventory, collected_items
    global player_x, player_y, player_direction
    global walk_frame, walk_timer, is_walking
    global interaction_message, message_timer
    global transition_active, transition_alpha, transition_phase

    game_state = "game"
    current_room = "Main Lobby"
    inventory.clear()
    collected_items.clear()

    player_x = 95
    player_y = 91
    player_direction = "down"
    walk_frame = 0
    walk_timer = 0
    is_walking = False

    interaction_message = ""
    message_timer = 0
    transition_active = False
    transition_alpha = 0
    transition_phase = "out"

    for key in door_progress:
        door_progress[key] = 0.0


def handle_interaction():
    """Handle the E key for doors and collectible security tools."""
    global game_state, interaction_message, message_timer

    interaction_type, value = nearest_interaction()

    if interaction_type == "item":
        collected_items.add(value)
        inventory.append(value)
        interaction_message = f"{value.upper()} RECOVERED"
        message_timer = 150
        return

    if interaction_type == "door":
        direction = value
        target_room = rooms[current_room][direction]

        # Entering the Control Room is the final decision, matching the
        # original text adventure rules.
        if target_room == "Control Room":
            if len(inventory) == 6:
                game_state = "win"
            else:
                game_state = "lose"
            return

        start_room_transition(target_room, direction)
        return

    interaction_message = "NOTHING TO INTERACT WITH"
    message_timer = 80


# --------------------------------------------------
# PIXEL ART: DOORS, ITEMS, ENVIRONMENTS
# --------------------------------------------------


def draw_sliding_door(surface, direction, progress, destination):
    """Draw an animated sci-fi sliding door for an exit."""
    rect = direction_door_rect(direction)
    frame_color = CYAN if destination != "Control Room" else RED

    # Dark doorway interior and bright frame.
    pygame.draw.rect(surface, BLACK, rect)
    pygame.draw.rect(surface, frame_color, rect, 2)

    if direction in ("north", "south"):
        half = rect.width // 2
        slide = int(half * progress)
        left_w = max(0, half - slide)
        right_w = max(0, rect.width - half - slide)

        if left_w:
            pygame.draw.rect(
                surface,
                WALL_DARK,
                (rect.x + 2, rect.y + 3, left_w - 1, rect.height - 5)
            )
        if right_w:
            pygame.draw.rect(
                surface,
                WALL_DARK,
                (rect.centerx + slide, rect.y + 3, right_w - 2, rect.height - 5)
            )

        pygame.draw.line(
            surface,
            frame_color,
            (rect.centerx, rect.y + 5),
            (rect.centerx, rect.bottom - 3)
        )
    else:
        half = rect.height // 2
        slide = int(half * progress)
        top_h = max(0, half - slide)
        bottom_h = max(0, rect.height - half - slide)

        if top_h:
            pygame.draw.rect(
                surface,
                WALL_DARK,
                (rect.x + 3, rect.y + 2, rect.width - 5, top_h - 1)
            )
        if bottom_h:
            pygame.draw.rect(
                surface,
                WALL_DARK,
                (rect.x + 3, rect.centery + slide, rect.width - 5, bottom_h - 2)
            )

    # Compact sign above/inside each door.
    label = DOOR_LABELS.get(destination, destination[:4].upper())
    sign = small_pixel_font.render(label, False, frame_color)

    if direction == "north":
        label_x = rect.centerx - sign.get_width() // 2
        label_y = rect.y + 5
    elif direction == "south":
        label_x = rect.centerx - sign.get_width() // 2
        label_y = rect.y + 3
    elif direction == "west":
        label_x = rect.x + 2
        label_y = rect.y + 2
    else:
        label_x = rect.x + rect.width - sign.get_width() - 2
        label_y = rect.y + 2

    surface.blit(sign, (label_x, label_y))


def item_position(room_name):
    """Return the location used for the collectible in a given room."""
    positions = {
        "Security Office": (118, 81),
        "Network Operations Center": (111, 78),
        "IT Office": (135, 79),
        "Server Room": (111, 82),
        "Data Center": (135, 78),
        "Admin Office": (112, 79),
    }
    return positions.get(room_name, (112, 80))


def draw_collectible(surface, item_name, x, y):
    """Draw a small glowing pixel icon for a security tool."""
    color = ITEM_DATA[item_name]["color"]
    pulse = 1 if (frame_counter // 18) % 2 == 0 else 0

    pygame.draw.rect(surface, (20, 26, 39), (x - 3 - pulse, y - 3 - pulse, 18 + pulse * 2, 18 + pulse * 2), 1)

    if item_name == "MFA Token":
        pygame.draw.rect(surface, color, (x + 2, y + 1, 9, 12))
        pygame.draw.rect(surface, BLACK, (x + 4, y + 4, 5, 3))
        pygame.draw.rect(surface, WHITE, (x + 5, y + 9, 3, 1))

    elif item_name == "Firewall Key":
        pygame.draw.circle(surface, color, (x + 4, y + 5), 4, 2)
        pygame.draw.rect(surface, color, (x + 7, y + 4, 8, 3))
        pygame.draw.rect(surface, color, (x + 11, y + 7, 2, 3))

    elif item_name == "Security Patch":
        pygame.draw.rect(surface, color, (x + 1, y + 1, 12, 12))
        pygame.draw.rect(surface, BLACK, (x + 5, y + 3, 4, 8))
        pygame.draw.rect(surface, BLACK, (x + 3, y + 5, 8, 4))

    elif item_name == "Backup Drive":
        pygame.draw.rect(surface, color, (x + 2, y + 2, 11, 10))
        pygame.draw.rect(surface, BLACK, (x + 4, y + 4, 7, 4))
        pygame.draw.rect(surface, GREEN, (x + 10, y + 10, 2, 1))

    elif item_name == "Encryption Key":
        pygame.draw.rect(surface, color, (x + 2, y + 6, 11, 5))
        pygame.draw.rect(surface, color, (x + 4, y + 1, 7, 7), 2)
        pygame.draw.rect(surface, BLACK, (x + 7, y + 7, 2, 2))

    elif item_name == "Access Card":
        pygame.draw.rect(surface, color, (x + 1, y + 2, 13, 9))
        pygame.draw.rect(surface, WHITE, (x + 3, y + 4, 7, 1))
        pygame.draw.rect(surface, BLACK, (x + 3, y + 7, 4, 2))


def draw_room_shell(surface, accent):
    """Draw the shared wall/floor structure used by every playable room."""
    pygame.draw.rect(surface, (18, 22, 34), (12, 35, 190, 94))
    pygame.draw.rect(surface, WALL, (16, 39, 182, 58))
    pygame.draw.rect(surface, FLOOR, (16, 97, 182, 28))

    # Wall panels and trim.
    for x in range(20, 196, 29):
        pygame.draw.line(surface, WALL_DARK, (x, 42), (x, 94))
    pygame.draw.line(surface, accent, (16, 39), (198, 39))
    pygame.draw.line(surface, WALL_DARK, (16, 96), (198, 96), 2)

    # Floor tile grid.
    for x in range(16, 199, 22):
        pygame.draw.line(surface, FLOOR_LINE, (x, 97), (x, 125))
    pygame.draw.line(surface, FLOOR_LINE, (16, 111), (198, 111))

    # Ceiling lights.
    for x in (42, 96, 150):
        pygame.draw.rect(surface, (70, 86, 106), (x, 43, 22, 2))
        pygame.draw.rect(surface, accent, (x + 4, 43, 14, 1))


def draw_alarm(surface):
    """Draw a flashing emergency beacon instead of a plain red block."""
    flash = (frame_counter // 18) % 2 == 0
    glow = RED if flash else (110, 35, 42)

    if flash:
        pygame.draw.rect(surface, (62, 24, 32), (160, 45, 24, 13), 1)
        pygame.draw.line(surface, RED, (157, 49), (153, 47))
        pygame.draw.line(surface, RED, (187, 49), (191, 47))

    pygame.draw.rect(surface, (88, 36, 28), (164, 55, 16, 3))
    pygame.draw.rect(surface, glow, (166, 48, 12, 7))
    pygame.draw.rect(surface, (255, 128, 105), (169, 48, 6, 2))


def draw_security_terminal(surface, x, y):
    """Draw an animated security workstation."""
    pygame.draw.rect(surface, (8, 11, 18), (x, y, 30, 24))
    pygame.draw.rect(surface, CYAN, (x + 3, y + 3, 24, 13), 1)
    pygame.draw.rect(surface, (14, 42, 49), (x + 5, y + 5, 20, 9))

    scan_y = y + 6 + (frame_counter // 4) % 7
    pygame.draw.line(surface, GREEN, (x + 6, scan_y), (x + 23, scan_y))
    pygame.draw.rect(surface, GREEN, (x + 6, y + 7, 6, 1))
    pygame.draw.rect(surface, CYAN, (x + 6, y + 11, 12, 1))

    pygame.draw.rect(surface, WALL_DARK, (x + 8, y + 18, 14, 3))
    pygame.draw.rect(surface, GRAY, (x + 6, y + 22, 18, 2))


def draw_room_props(surface, room_name):
    """Give every room a distinct retro environment."""
    if room_name == "Main Lobby":
        draw_security_terminal(surface, 48, 65)
        draw_alarm(surface)

        # Reception / security desk.
        pygame.draw.rect(surface, (20, 26, 39), (131, 76, 30, 18))
        pygame.draw.rect(surface, CYAN, (134, 79, 12, 7), 1)
        pygame.draw.rect(surface, GREEN, (137, 81, 6, 2))
        pygame.draw.rect(surface, GRAY, (132, 94, 32, 3))

        # Hazard stripe near the compromised control-room access.
        for x in range(88, 130, 8):
            pygame.draw.rect(surface, YELLOW if (x // 8) % 2 == 0 else BLACK, (x, 93, 6, 3))

    elif room_name == "Security Office":
        # Desk and dual monitors.
        pygame.draw.rect(surface, (28, 34, 49), (55, 76, 54, 5))
        pygame.draw.rect(surface, GRAY, (59, 81, 4, 15))
        pygame.draw.rect(surface, GRAY, (101, 81, 4, 15))
        for monitor_x in (62, 84):
            pygame.draw.rect(surface, BLACK, (monitor_x, 58, 18, 14))
            pygame.draw.rect(surface, CYAN, (monitor_x + 2, 60, 14, 9), 1)
            pygame.draw.rect(surface, GREEN, (monitor_x + 4, 62, 7, 1))
            pygame.draw.rect(surface, CYAN, (monitor_x + 4, 65, 10, 1))

        # Key-card cabinet.
        pygame.draw.rect(surface, WALL_DARK, (143, 56, 20, 28))
        pygame.draw.rect(surface, GRAY, (146, 59, 14, 4))
        pygame.draw.rect(surface, RED, (157, 75, 2, 2))

    elif room_name == "Network Operations Center":
        # Network wall with live traffic lines.
        for rack_x in (49, 77, 133, 161):
            pygame.draw.rect(surface, BLACK, (rack_x, 52, 18, 42))
            pygame.draw.rect(surface, GRAY, (rack_x, 52, 18, 42), 1)
            for light_y in (58, 65, 72, 79, 86):
                light = GREEN if (frame_counter // 10 + rack_x + light_y) % 3 else RED
                pygame.draw.rect(surface, light, (rack_x + 3, light_y, 3, 1))
                pygame.draw.rect(surface, CYAN, (rack_x + 8, light_y, 6, 1))

        pygame.draw.line(surface, CYAN, (67, 64), (77, 64))
        pygame.draw.line(surface, GREEN, (95, 72), (133, 72))
        pygame.draw.line(surface, CYAN, (151, 60), (161, 60))

    elif room_name == "IT Office":
        # Repair bench and diagnostics monitors.
        pygame.draw.rect(surface, (42, 45, 54), (48, 78, 112, 5))
        pygame.draw.rect(surface, GRAY, (53, 83, 4, 14))
        pygame.draw.rect(surface, GRAY, (151, 83, 4, 14))
        pygame.draw.rect(surface, BLACK, (60, 58, 30, 17))
        pygame.draw.rect(surface, CYAN, (63, 61, 24, 11), 1)
        pygame.draw.rect(surface, YELLOW, (66, 64, 12, 2))
        pygame.draw.rect(surface, GREEN, (66, 68, 17, 1))
        pygame.draw.rect(surface, (70, 75, 86), (103, 63, 23, 12))
        pygame.draw.rect(surface, RED, (109, 67, 10, 2))

    elif room_name == "Server Room":
        # Rows of dense server racks.
        for rack_x in (46, 75, 104, 133, 162):
            pygame.draw.rect(surface, BLACK, (rack_x, 50, 20, 45))
            pygame.draw.rect(surface, (80, 93, 112), (rack_x, 50, 20, 45), 1)
            for light_y in range(56, 90, 7):
                pygame.draw.rect(surface, GREEN, (rack_x + 3, light_y, 2, 1))
                pygame.draw.rect(surface, CYAN, (rack_x + 7, light_y, 8, 1))

    elif room_name == "Data Center":
        # Core data towers and cooling columns.
        for tower_x in (49, 87, 125, 163):
            pygame.draw.rect(surface, (13, 20, 32), (tower_x, 50, 24, 44))
            pygame.draw.rect(surface, PURPLE, (tower_x, 50, 24, 44), 1)
            pygame.draw.rect(surface, CYAN, (tower_x + 4, 56, 16, 3))
            pygame.draw.rect(surface, GREEN, (tower_x + 4, 65, 12, 2))
            pygame.draw.rect(surface, PURPLE, (tower_x + 4, 74, 16, 2))
        pygame.draw.line(surface, PURPLE, (61, 48), (175, 48))

    elif room_name == "Admin Office":
        # Executive desk, secure terminal, and safe.
        pygame.draw.rect(surface, (57, 45, 40), (54, 77, 72, 7))
        pygame.draw.rect(surface, (37, 29, 27), (60, 84, 5, 13))
        pygame.draw.rect(surface, (37, 29, 27), (115, 84, 5, 13))
        pygame.draw.rect(surface, BLACK, (74, 58, 27, 16))
        pygame.draw.rect(surface, CYAN, (77, 61, 21, 10), 1)
        pygame.draw.rect(surface, YELLOW, (80, 64, 12, 1))
        pygame.draw.rect(surface, WALL_DARK, (149, 60, 25, 26))
        pygame.draw.rect(surface, GRAY, (153, 64, 17, 18), 1)
        pygame.draw.circle(surface, YELLOW, (161, 73), 3, 1)

    elif room_name == "Control Room":
        # This room is normally replaced by the win/loss screen.
        pygame.draw.rect(surface, BLACK, (52, 53, 116, 40))
        pygame.draw.rect(surface, RED, (52, 53, 116, 40), 1)
        pygame.draw.circle(surface, RED, (110, 69), 10, 2)
        pygame.draw.rect(surface, RED, (106, 66, 3, 3))
        pygame.draw.rect(surface, RED, (114, 66, 3, 3))
        pygame.draw.line(surface, RED, (105, 78), (117, 78))


def draw_current_room(surface):
    """Draw the current room, exits, props, item, and player."""
    accent = CYAN
    if current_room == "Control Room":
        accent = RED
    elif current_room == "Data Center":
        accent = PURPLE
    elif current_room == "Admin Office":
        accent = YELLOW

    draw_room_shell(surface, accent)
    draw_room_props(surface, current_room)

    room = rooms[current_room]
    for direction in ("north", "south", "west", "east"):
        if direction in room:
            progress = door_progress.get((current_room, direction), 0.0)
            draw_sliding_door(surface, direction, progress, room[direction])

    room_item = room.get("item")
    if room_item and room_item not in collected_items:
        item_x, item_y = item_position(current_room)
        draw_collectible(surface, room_item, item_x, item_y)

    draw_player(
        surface,
        player_x,
        player_y,
        player_direction,
        walk_frame,
        is_walking
    )


# --------------------------------------------------
# TITLE / RESULT SCREENS
# --------------------------------------------------


def draw_title_screen(surface, show_prompt):
    """Draw the retro title screen."""
    surface.fill(BACKGROUND)
    pygame.draw.rect(surface, CYAN, (8, 8, 304, 164), 2)
    pygame.draw.rect(surface, DARK_BLUE, (12, 12, 296, 156), 2)
    pygame.draw.rect(surface, PINK, (22, 30, 55, 3))
    pygame.draw.rect(surface, PINK, (243, 30, 55, 3))

    draw_pixel_lock(surface, 148, 20)

    title_1 = title_font.render("CYBERSECURITY", False, CYAN)
    title_2 = title_font.render("ATTACK", False, PINK)
    subtitle = subtitle_font.render("RETRO RESPONSE PROTOCOL", False, WHITE)

    surface.blit(title_1, (BASE_WIDTH // 2 - title_1.get_width() // 2, 58))
    surface.blit(title_2, (BASE_WIDTH // 2 - title_2.get_width() // 2, 88))
    surface.blit(subtitle, (BASE_WIDTH // 2 - subtitle.get_width() // 2, 121))

    if show_prompt:
        prompt = small_pixel_font.render("PRESS ENTER TO START", False, GREEN)
        surface.blit(prompt, (BASE_WIDTH // 2 - prompt.get_width() // 2, 148))


def draw_result_screen(surface, won):
    """Draw the win or loss screen."""
    surface.fill(BACKGROUND)
    border = GREEN if won else RED
    pygame.draw.rect(surface, border, (8, 8, 304, 164), 2)
    pygame.draw.rect(surface, DARK_BLUE, (14, 14, 292, 152), 2)

    if won:
        title = title_font.render("SYSTEM RESTORED", False, GREEN)
        line_1 = subtitle_font.render("RANSOMWARE BOT STOPPED", False, WHITE)
        icon_color = GREEN
    else:
        title = title_font.render("SYSTEM BREACHED", False, RED)
        line_1 = subtitle_font.render("RANSOMWARE BOT WON", False, WHITE)
        icon_color = RED

    surface.blit(title, (BASE_WIDTH // 2 - title.get_width() // 2, 46))
    surface.blit(line_1, (BASE_WIDTH // 2 - line_1.get_width() // 2, 92))

    # Bot face.
    pygame.draw.rect(surface, (18, 22, 34), (138, 20, 44, 20))
    pygame.draw.rect(surface, icon_color, (138, 20, 44, 20), 2)
    pygame.draw.rect(surface, icon_color, (147, 27, 5, 4))
    pygame.draw.rect(surface, icon_color, (168, 27, 5, 4))
    pygame.draw.line(surface, icon_color, (149, 35), (171, 35), 2)

    prompt = small_pixel_font.render("PRESS R TO RESTART", False, YELLOW)
    surface.blit(prompt, (BASE_WIDTH // 2 - prompt.get_width() // 2, 137))


# --------------------------------------------------
# GAME SCREEN / HUD
# --------------------------------------------------


def draw_inventory_boxes(surface):
    """Draw inventory slots, filling recovered tools with their accent color."""
    pygame.draw.rect(surface, PANEL_BLUE, (8, 139, 304, 33))
    pygame.draw.rect(surface, CYAN, (8, 139, 304, 33), 1)

    item_order = list(ITEM_DATA.keys())
    start_x = 72

    for index, item_name in enumerate(item_order):
        slot_x = start_x + index * 38
        collected = item_name in collected_items
        accent = ITEM_DATA[item_name]["color"] if collected else GRAY
        fill = (20, 32, 43) if collected else (12, 16, 28)

        pygame.draw.rect(surface, fill, (slot_x, 144, 33, 20))
        pygame.draw.rect(surface, accent, (slot_x, 144, 33, 20), 1)

        if collected:
            pygame.draw.rect(surface, accent, (slot_x + 4, 148, 7, 7), 1)
            pygame.draw.rect(surface, accent, (slot_x + 6, 150, 3, 3))


def draw_room_panel(surface):
    pygame.draw.rect(surface, PANEL_BLUE, (208, 35, 104, 94))
    pygame.draw.rect(surface, CYAN, (208, 35, 104, 94), 1)


def draw_game_screen(surface):
    """Draw the complete low-resolution pixel layer."""
    surface.fill(BACKGROUND)
    pygame.draw.rect(surface, CYAN, (5, 5, 310, 170), 2)
    pygame.draw.rect(surface, DARK_BLUE, (8, 8, 304, 22))

    room_name = room_pixel_font.render(current_room.upper(), False, CYAN)
    surface.blit(room_name, (14, 11))

    draw_current_room(surface)
    draw_room_panel(surface)
    draw_inventory_boxes(surface)


def draw_hud_text(surface):
    """Draw readable high-resolution HUD text over the pixel layer."""
    status = hud_status_font.render("SYSTEM: COMPROMISED", True, RED)
    surface.blit(status, (925 - status.get_width(), 47))

    heading = hud_heading_font.render("MISSION STATUS", True, YELLOW)
    surface.blit(heading, (650, 132))

    room = rooms[current_room]
    y = 185
    for line in room["description"]:
        text = hud_body_font.render(line, True, WHITE)
        surface.blit(text, (650, y))
        y += 31

    exits_heading = hud_heading_font.render("EXITS", True, GREEN)
    surface.blit(exits_heading, (650, 288))

    exit_y = 330
    for direction in ("north", "south", "west", "east"):
        if direction in room:
            label = f"{direction.upper():5}: {room[direction]}"
            text = hud_body_bold.render(label, True, WHITE)
            surface.blit(text, (650, exit_y))
            exit_y += 27

    interaction_type, value = nearest_interaction()
    if interaction_type == "item":
        prompt_text = f"E  COLLECT {value.upper()}"
        prompt_color = YELLOW
    elif interaction_type == "door":
        destination = room[value]
        prompt_text = f"E  ENTER {destination.upper()}"
        prompt_color = GREEN if destination != "Control Room" else RED
    else:
        prompt_text = "ARROW KEYS / WASD TO MOVE   |   E TO INTERACT"
        prompt_color = GRAY

    prompt = hud_small_font.render(prompt_text, True, prompt_color)
    surface.blit(
        prompt,
        (WINDOW_WIDTH // 2 - prompt.get_width() // 2, 389)
    )

    if interaction_message and message_timer > 0:
        message = hud_small_font.render(interaction_message, True, CYAN)
        pygame.draw.rect(
            surface,
            (10, 14, 24),
            (WINDOW_WIDTH // 2 - message.get_width() // 2 - 12, 355, message.get_width() + 24, 28)
        )
        pygame.draw.rect(
            surface,
            CYAN,
            (WINDOW_WIDTH // 2 - message.get_width() // 2 - 12, 355, message.get_width() + 24, 28),
            1
        )
        surface.blit(message, (WINDOW_WIDTH // 2 - message.get_width() // 2, 361))

    inventory_heading = hud_heading_font.render("INVENTORY", True, YELLOW)
    surface.blit(inventory_heading, (39, 441))

    item_order = list(ITEM_DATA.keys())
    start_x = 216
    for index, item_name in enumerate(item_order):
        label = ITEM_DATA[item_name]["label"]
        slot_center_x = start_x + index * 114 + 49
        color = ITEM_DATA[item_name]["color"] if item_name in collected_items else GRAY
        text = hud_inventory_font.render(label, True, color)
        surface.blit(text, (slot_center_x - text.get_width() // 2, 460))


def draw_transition_overlay(surface):
    """Draw the full-resolution fade overlay during room transitions."""
    if not transition_active:
        return

    fade = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    fade.fill(BLACK)
    fade.set_alpha(transition_alpha)
    surface.blit(fade, (0, 0))


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------


def main():
    global game_state, current_room, player_x, player_y, player_direction
    global walk_frame, walk_timer, is_walking, frame_counter
    global interaction_message, message_timer

    running = True
    blink_timer = 0
    show_prompt = True

    while running:
        frame_counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if game_state == "title":
                    if event.key == pygame.K_RETURN:
                        reset_game()

                elif game_state == "game":
                    if event.key == pygame.K_ESCAPE:
                        game_state = "title"
                    elif event.key == pygame.K_e and not transition_active:
                        handle_interaction()

                elif game_state in ("lose", "win"):
                    if event.key == pygame.K_r:
                        reset_game()

        # Movement is disabled during room fades.
        if game_state == "game" and not transition_active:
            keys = pygame.key.get_pressed()
            move_x = 0
            move_y = 0

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                move_x = -player_speed
                player_direction = "left"
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                move_x = player_speed
                player_direction = "right"

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                move_y = -player_speed
                player_direction = "up"
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                move_y = player_speed
                player_direction = "down"

            is_walking = move_x != 0 or move_y != 0
            player_x = clamp(player_x + move_x, 18, 177)
            player_y = clamp(player_y + move_y, 63, 94)

            if is_walking:
                walk_timer += 1
                if walk_timer >= 10:
                    walk_frame = 1 - walk_frame
                    walk_timer = 0
            else:
                walk_frame = 0
                walk_timer = 0

            update_door_animations()
        else:
            is_walking = False

        if transition_active:
            update_transition()

        if message_timer > 0:
            message_timer -= 1

        # --------------------------------------------------
        # LOW-RESOLUTION PIXEL LAYER
        # --------------------------------------------------

        if game_state == "title":
            blink_timer += 1
            if blink_timer >= 30:
                show_prompt = not show_prompt
                blink_timer = 0
            draw_title_screen(canvas, show_prompt)

        elif game_state == "game":
            draw_game_screen(canvas)

        elif game_state == "lose":
            draw_result_screen(canvas, False)

        elif game_state == "win":
            draw_result_screen(canvas, True)

        scaled_canvas = pygame.transform.scale(
            canvas,
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        screen.blit(scaled_canvas, (0, 0))

        # --------------------------------------------------
        # HIGH-RESOLUTION TEXT / EFFECTS
        # --------------------------------------------------

        if game_state == "game":
            draw_hud_text(screen)
            draw_transition_overlay(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
