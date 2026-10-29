import math
from pathlib import Path
import pygame

pygame.init()

# ==================================================
# CYBERSECURITY ATTACK - FINAL MAROON POLISH BUILD
# ==================================================

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
BASE_WIDTH = 320
BASE_HEIGHT = 180
SCALE = 3
FPS = 60

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cybersecurity Attack")
canvas = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))
character_canvas = pygame.Surface((BASE_WIDTH, BASE_HEIGHT), pygame.SRCALPHA)
clock = pygame.time.Clock()


# --------------------------------------------------
# AUDIO
# --------------------------------------------------

SOUND_DIR = Path(__file__).resolve().parent / "assets" / "sounds"
SOUND_FILES = {
    "pickup": "pickup.wav",
    "transition": "transition.wav",
    "ui_click": "ui_click.wav",
    "victory": "victory.wav",
    "warning": "warning.wav",
}
SOUND_VOLUMES = {
    "pickup": 0.48,
    "transition": 0.34,
    "ui_click": 0.28,
    "victory": 0.50,
    "warning": 0.42,
}

sounds = {}
sound_available = False
sound_muted = False

def init_audio():
    """Load optional effects without ever preventing the game from starting."""
    global sound_available, sounds
    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

        loaded = {}
        for name, filename in SOUND_FILES.items():
            path = SOUND_DIR / filename
            if not path.is_file():
                continue
            effect = pygame.mixer.Sound(str(path))
            effect.set_volume(SOUND_VOLUMES.get(name, 0.4))
            loaded[name] = effect

        sounds = loaded
        sound_available = bool(sounds)
    except (pygame.error, OSError):
        sounds = {}
        sound_available = False

def play_sound(name):
    if sound_available and not sound_muted:
        effect = sounds.get(name)
        if effect is not None:
            effect.play()

def toggle_mute():
    global sound_muted
    sound_muted = not sound_muted
    if sound_available and sound_muted:
        pygame.mixer.stop()
    return sound_muted

init_audio()

# --------------------------------------------------
# COLORS
# --------------------------------------------------

BACKGROUND = (7, 10, 20)
BLACK = (4, 6, 12)
DEEP_NAVY = (8, 15, 29)
DARK_BLUE = (13, 24, 43)
PANEL_BLUE = (19, 34, 57)
PANEL_INNER = (10, 18, 31)
WALL = (29, 41, 58)
WALL_DARK = (20, 28, 42)
FLOOR = (21, 28, 41)
FLOOR_LINE = (40, 51, 70)
METAL = (62, 74, 94)
METAL_LIGHT = (101, 116, 139)
WHITE = (240, 243, 248)
GRAY = (144, 154, 174)
GRAY_DARK = (70, 82, 103)
CYAN = (55, 236, 255)
GREEN = (74, 255, 131)
YELLOW = (255, 220, 82)
RED = (255, 73, 79)
ORANGE = (255, 151, 61)
PURPLE = (166, 94, 255)
PINK = (255, 73, 176)
BLUE = (83, 153, 255)
TEAL = (46, 207, 195)

# --------------------------------------------------
# LAYOUT
# --------------------------------------------------

HEADER_RECT = pygame.Rect(6, 6, 308, 23)
ROOM_RECT = pygame.Rect(9, 33, 194, 104)
MISSION_RECT = pygame.Rect(208, 33, 104, 104)
INVENTORY_RECT = pygame.Rect(7, 141, 306, 34)

PLAY_MIN_X = 16
PLAY_MAX_X = 176
PLAY_MIN_Y = 63
PLAY_MAX_Y = 102

PLAYER_W = 22
PLAYER_H = 32

# --------------------------------------------------
# FONTS
# --------------------------------------------------

pixel_title_font = pygame.font.Font(None, 42)
pixel_subtitle_font = pygame.font.Font(None, 21)
pixel_small_font = pygame.font.Font(None, 13)
pixel_tiny_font = pygame.font.Font(None, 9)
pixel_micro_font = pygame.font.Font(None, 8)

hud_heading_font = pygame.font.SysFont("consolas", 27, bold=True)
hud_body_font = pygame.font.SysFont("consolas", 17)
hud_body_bold = pygame.font.SysFont("consolas", 16, bold=True)
hud_small_font = pygame.font.SysFont("consolas", 14, bold=True)
hud_tiny_font = pygame.font.SysFont("consolas", 12, bold=True)
hud_micro_font = pygame.font.SysFont("consolas", 10, bold=True)
hud_status_font = pygame.font.SysFont("consolas", 16, bold=True)
hud_result_title_font = pygame.font.SysFont("consolas", 38, bold=True)
hud_result_subtitle_font = pygame.font.SysFont("consolas", 22, bold=True)
hud_result_body_font = pygame.font.SysFont("consolas", 16)
hud_prompt_large_font = pygame.font.SysFont("consolas", 22, bold=True)
hud_door_font = pygame.font.SysFont("consolas", 13, bold=True)
hud_door_small_font = pygame.font.SysFont("consolas", 11, bold=True)

# --------------------------------------------------
# GAME DATA
# --------------------------------------------------

rooms = {
    "Main Lobby": {
        "description": [
            "Emergency systems are active.",
            "The company network is under attack.",
        ],
        "north": "Control Room",
        "west": "Security Office",
    },
    "Security Office": {
        "description": [
            "Camera feeds and access logs are online.",
            "Authentication controls need recovery.",
        ],
        "east": "Main Lobby",
        "north": "Network Operations Center",
        "item": "MFA Token",
    },
    "Network Operations Center": {
        "description": [
            "Traffic monitors show unstable activity.",
            "Firewall alerts continue to spike.",
        ],
        "south": "Security Office",
        "north": "IT Office",
        "item": "Firewall Key",
    },
    "IT Office": {
        "description": [
            "Workstations are failing update checks.",
            "A critical security fix is waiting.",
        ],
        "south": "Network Operations Center",
        "east": "Server Room",
        "item": "Security Patch",
    },
    "Server Room": {
        "description": [
            "Server racks are running under heavy load.",
            "The backup system is isolated.",
        ],
        "west": "IT Office",
        "east": "Data Center",
        "item": "Backup Drive",
    },
    "Data Center": {
        "description": [
            "Encrypted traffic is flooding the core.",
            "Cooling systems are under strain.",
        ],
        "west": "Server Room",
        "south": "Admin Office",
        "item": "Encryption Key",
    },
    "Admin Office": {
        "description": [
            "Administrative systems are locked down.",
            "Restricted access blocks the final route.",
        ],
        "north": "Data Center",
        "west": "Control Room",
        "item": "Access Card",
    },
    "Control Room": {
        "description": [
            "The Ransomware Bot controls the core.",
            "Every security tool is required.",
        ],
        "south": "Main Lobby",
        "east": "Admin Office",
    },
}

ITEM_DATA = {
    "MFA Token": {
        "inventory_lines": ("MFA", "TOKEN"),
        "color": GREEN,
    },
    "Firewall Key": {
        "inventory_lines": ("FIREWALL", "KEY"),
        "color": ORANGE,
    },
    "Security Patch": {
        "inventory_lines": ("SECURITY", "PATCH"),
        "color": CYAN,
    },
    "Backup Drive": {
        "inventory_lines": ("BACKUP", "DRIVE"),
        "color": PURPLE,
    },
    "Encryption Key": {
        "inventory_lines": ("ENCRYPT", "KEY"),
        "color": YELLOW,
    },
    "Access Card": {
        "inventory_lines": ("ACCESS", "CARD"),
        "color": PINK,
    },
}

ROOM_ACCENTS = {
    "Main Lobby": CYAN,
    "Security Office": GREEN,
    "Network Operations Center": BLUE,
    "IT Office": CYAN,
    "Server Room": BLUE,
    "Data Center": PURPLE,
    "Admin Office": YELLOW,
    "Control Room": RED,
}

DOOR_LABELS = {
    "Control Room": "CONTROL ROOM",
    "Security Office": "SECURITY OFFICE",
    "Main Lobby": "MAIN LOBBY",
    "Network Operations Center": "NETWORK OPS",
    "IT Office": "IT OFFICE",
    "Server Room": "SERVER ROOM",
    "Data Center": "DATA CENTER",
    "Admin Office": "ADMIN OFFICE",
}

ROOM_DOOR_RECTS = {
    "Main Lobby": {"north": (84, 43, 44, 38), "west": (12, 69, 28, 45)},
    "Security Office": {"north": (84, 43, 44, 38), "east": (171, 69, 28, 45)},
    "Network Operations Center": {"north": (84, 43, 44, 38), "south": (18, 93, 30, 39)},
    "IT Office": {"south": (72, 94, 42, 38), "east": (171, 69, 28, 45)},
    "Server Room": {"west": (12, 69, 28, 45), "east": (171, 69, 28, 45)},
    "Data Center": {"west": (12, 69, 28, 45), "south": (145, 94, 42, 38)},
    "Admin Office": {"north": (84, 43, 44, 38), "west": (12, 69, 28, 45)},
}

ITEM_POSITIONS = {
    "Security Office": (132, 76),
    "Network Operations Center": (147, 76),
    "IT Office": (130, 77),
    "Server Room": (103, 78),
    "Data Center": (112, 80),
    "Admin Office": (145, 77),
}

# --------------------------------------------------
# STATE
# --------------------------------------------------

game_state = "title"
current_room = "Main Lobby"
inventory = []
collected_items = set()

player_x = 94
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
pending_result = None

result_timer = 0


door_progress = {
    (room_name, direction): 0.0
    for room_name, room_data in rooms.items()
    for direction in ("north", "south", "west", "east")
    if direction in room_data
}

# --------------------------------------------------
# GENERAL HELPERS
# --------------------------------------------------


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def lerp(a, b, amount):
    amount = clamp(amount, 0.0, 1.0)
    return a + (b - a) * amount


def opposite_direction(direction):
    return {
        "north": "south",
        "south": "north",
        "west": "east",
        "east": "west",
    }[direction]


def get_player_center(x=None, y=None):
    if x is None:
        x = player_x
    if y is None:
        y = player_y
    return pygame.Vector2(x + PLAYER_W / 2, y + PLAYER_H / 2)


def wrap_text(text, font, max_width):
    words = text.split()
    if not words:
        return [""]

    lines = []
    current = words[0]
    for word in words[1:]:
        trial = current + " " + word
        if font.size(trial)[0] <= max_width:
            current = trial
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines


def fit_hud_text(text, max_width, start_size=17, min_size=10, bold=False):
    for size in range(start_size, min_size - 1, -1):
        font = pygame.font.SysFont("consolas", size, bold=bold)
        if font.size(text)[0] <= max_width:
            return font
    return pygame.font.SysFont("consolas", min_size, bold=bold)


def fit_pixel_text(text, max_width, start_size=28, min_size=12, color=CYAN):
    for size in range(start_size, min_size - 1, -1):
        font = pygame.font.Font(None, size)
        rendered = font.render(text, False, color)
        if rendered.get_width() <= max_width:
            return font, rendered
    font = pygame.font.Font(None, min_size)
    return font, font.render(text, False, color)


def pulse(speed=12, minimum=0.35, maximum=1.0):
    value = (math.sin(frame_counter / speed) + 1.0) / 2.0
    return minimum + (maximum - minimum) * value


def scaled_rect(rect):
    return pygame.Rect(rect.x * SCALE, rect.y * SCALE, rect.w * SCALE, rect.h * SCALE)


def mix_color(a, b, amount):
    amount = clamp(amount, 0.0, 1.0)
    return tuple(int(a[i] + (b[i] - a[i]) * amount) for i in range(3))

# --------------------------------------------------
# PIXEL ICONS
# --------------------------------------------------


def draw_pixel_lock(surface, x, y, color=YELLOW, scale=1):
    pygame.draw.rect(surface, color, (x + 4 * scale, y, 10 * scale, 3 * scale))
    pygame.draw.rect(surface, color, (x + 2 * scale, y + 2 * scale, 3 * scale, 7 * scale))
    pygame.draw.rect(surface, color, (x + 13 * scale, y + 2 * scale, 3 * scale, 7 * scale))
    pygame.draw.rect(surface, color, (x, y + 7 * scale, 18 * scale, 13 * scale))
    pygame.draw.rect(surface, BACKGROUND, (x + 7 * scale, y + 11 * scale, 4 * scale, 5 * scale))



def draw_item_icon(surface, item_name, x, y, color=None, scale=1):
    """Compact, recognizable pixel icons used both in-world and in the toolkit."""
    color = color or ITEM_DATA[item_name]["color"]
    dark = (12, 18, 30)

    if item_name == "MFA Token":
        pygame.draw.rect(surface, color, (x + 2 * scale, y, 10 * scale, 17 * scale))
        pygame.draw.rect(surface, dark, (x + 5 * scale, y + 3 * scale, 4 * scale, 5 * scale))
        pygame.draw.rect(surface, WHITE, (x + 5 * scale, y + 12 * scale, 4 * scale, 2 * scale))
        pygame.draw.rect(surface, GREEN, (x + 10 * scale, y + 1 * scale, 2 * scale, 2 * scale))

    elif item_name == "Firewall Key":
        pygame.draw.circle(surface, color, (x + 5 * scale, y + 7 * scale), 5 * scale)
        pygame.draw.circle(surface, dark, (x + 5 * scale, y + 7 * scale), 2 * scale)
        pygame.draw.rect(surface, color, (x + 9 * scale, y + 5 * scale, 10 * scale, 4 * scale))
        pygame.draw.rect(surface, color, (x + 14 * scale, y + 8 * scale, 3 * scale, 4 * scale))
        pygame.draw.rect(surface, color, (x + 18 * scale, y + 8 * scale, 2 * scale, 3 * scale))

    elif item_name == "Security Patch":
        pygame.draw.rect(surface, color, (x + 2 * scale, y + 2 * scale, 15 * scale, 14 * scale))
        pygame.draw.rect(surface, dark, (x + 5 * scale, y + 5 * scale, 9 * scale, 8 * scale))
        for pin in (4, 8, 12):
            pygame.draw.rect(surface, color, (x, y + pin * scale, 2 * scale, 1 * scale))
            pygame.draw.rect(surface, color, (x + 17 * scale, y + pin * scale, 2 * scale, 1 * scale))
        pygame.draw.line(surface, WHITE, (x + 7 * scale, y + 9 * scale),
                         (x + 9 * scale, y + 11 * scale), max(1, scale))
        pygame.draw.line(surface, WHITE, (x + 9 * scale, y + 11 * scale),
                         (x + 13 * scale, y + 7 * scale), max(1, scale))

    elif item_name == "Backup Drive":
        pygame.draw.rect(surface, color, (x + 1 * scale, y + 3 * scale, 17 * scale, 13 * scale))
        pygame.draw.rect(surface, dark, (x + 4 * scale, y + 6 * scale, 11 * scale, 5 * scale))
        pygame.draw.rect(surface, METAL_LIGHT, (x + 5 * scale, y + 12 * scale, 7 * scale, 1 * scale))
        pygame.draw.rect(surface, GREEN, (x + 14 * scale, y + 12 * scale, 2 * scale, 2 * scale))
        pygame.draw.rect(surface, color, (x + 6 * scale, y, 7 * scale, 3 * scale))

    elif item_name == "Encryption Key":
        pygame.draw.rect(surface, color, (x + 1 * scale, y + 3 * scale, 10 * scale, 10 * scale))
        pygame.draw.rect(surface, dark, (x + 4 * scale, y + 6 * scale, 4 * scale, 4 * scale))
        pygame.draw.rect(surface, color, (x + 10 * scale, y + 6 * scale, 10 * scale, 4 * scale))
        pygame.draw.rect(surface, color, (x + 15 * scale, y + 9 * scale, 2 * scale, 4 * scale))
        pygame.draw.rect(surface, color, (x + 18 * scale, y + 9 * scale, 2 * scale, 3 * scale))
        pygame.draw.rect(surface, CYAN, (x + 3 * scale, y + 4 * scale, 2 * scale, 1 * scale))
        pygame.draw.rect(surface, CYAN, (x + 7 * scale, y + 11 * scale, 2 * scale, 1 * scale))

    elif item_name == "Access Card":
        pygame.draw.rect(surface, color, (x, y + 3 * scale, 19 * scale, 13 * scale))
        pygame.draw.rect(surface, dark, (x + 3 * scale, y + 6 * scale, 6 * scale, 6 * scale))
        pygame.draw.rect(surface, WHITE, (x + 11 * scale, y + 6 * scale, 5 * scale, 2 * scale))
        pygame.draw.rect(surface, dark, (x + 11 * scale, y + 10 * scale, 5 * scale, 1 * scale))
        pygame.draw.rect(surface, YELLOW, (x + 2 * scale, y + 4 * scale, 2 * scale, 2 * scale))

def draw_inventory_glyph(surface, item_name, x, y, color):
    """Small 12x10 toolkit glyph so labels never collide with artwork."""
    dark = (8, 13, 22)
    if item_name == "MFA Token":
        pygame.draw.rect(surface, color, (x + 3, y, 6, 10))
        pygame.draw.rect(surface, dark, (x + 5, y + 2, 2, 3))
        pygame.draw.rect(surface, WHITE, (x + 5, y + 7, 2, 1))
    elif item_name == "Firewall Key":
        pygame.draw.circle(surface, color, (x + 3, y + 4), 3)
        pygame.draw.circle(surface, dark, (x + 3, y + 4), 1)
        pygame.draw.rect(surface, color, (x + 6, y + 3, 6, 2))
        pygame.draw.rect(surface, color, (x + 9, y + 5, 1, 3))
    elif item_name == "Security Patch":
        pygame.draw.rect(surface, color, (x + 2, y + 1, 8, 8))
        pygame.draw.rect(surface, dark, (x + 4, y + 3, 4, 4))
        pygame.draw.line(surface, WHITE, (x + 4, y + 5), (x + 5, y + 6), 1)
        pygame.draw.line(surface, WHITE, (x + 5, y + 6), (x + 8, y + 3), 1)
    elif item_name == "Backup Drive":
        pygame.draw.rect(surface, color, (x + 1, y + 2, 10, 7))
        pygame.draw.rect(surface, dark, (x + 3, y + 4, 6, 2))
        pygame.draw.rect(surface, GREEN, (x + 9, y + 7, 1, 1))
    elif item_name == "Encryption Key":
        pygame.draw.rect(surface, color, (x + 1, y + 2, 6, 6))
        pygame.draw.rect(surface, dark, (x + 3, y + 4, 2, 2))
        pygame.draw.rect(surface, color, (x + 7, y + 4, 5, 2))
        pygame.draw.rect(surface, color, (x + 9, y + 6, 1, 2))
    else:
        pygame.draw.rect(surface, color, (x + 1, y + 2, 10, 7))
        pygame.draw.rect(surface, dark, (x + 3, y + 4, 3, 3))
        pygame.draw.rect(surface, WHITE, (x + 7, y + 4, 3, 1))


# --------------------------------------------------
# PLAYER ART
# --------------------------------------------------


def draw_player(surface, x, y, direction, frame, walking, celebrate=False, defeated=False):
    """Draw the final unified player sprite set.

    The side profile keeps the silhouette that tested well. Front and back are
    rebuilt from the same proportions, hair mass, hoodie, legs, and shoes so
    rotating the character reads as one person rather than separate sprites.
    """
    skin = (232, 184, 145)
    skin_light = (248, 207, 170)
    skin_shadow = (188, 128, 92)
    hair = (67, 40, 25)
    hair_dark = (49, 29, 21)
    hair_light = (111, 70, 39)
    eye = (18, 17, 21)
    brow = (48, 30, 23)
    mouth = (119, 67, 61)
    # Final character palette: maroon-red hoodie chosen for strong contrast
    # across the navy/steel facility while staying distinct from cyan UI elements.
    hoodie = (122, 51, 66)
    hoodie_dark = (49, 20, 29)
    hoodie_light = (158, 72, 88)
    shirt = (37, 211, 220)
    shirt_dark = (18, 143, 154)
    pants = (16, 25, 40)
    shoes = (116, 130, 151)

    ox = x + 1
    oy = y
    leg_phase = frame if walking else 0
    bob = -1 if walking and frame else 0
    oy += bob

    jump = 0
    if celebrate:
        phase = (result_timer // 6) % 10
        if phase in (1, 2):
            jump = -6
        elif phase in (3, 4):
            jump = -3
        elif phase in (6, 7):
            jump = -4
        oy += jump

    # Grounding shadow; the sprite feels planted rather than pasted onto the floor.
    shadow_w = 10 if jump < 0 else 15
    pygame.draw.ellipse(surface, (3, 6, 11), (ox + 10 - shadow_w // 2, oy + 29 - jump, shadow_w, 3))

    if defeated:
        # Kneeling/slumped silhouette with bowed head and dropped arms.
        pygame.draw.ellipse(surface, (3, 6, 11), (ox + 2, oy + 28, 17, 3))
        pygame.draw.polygon(surface, hoodie, [
            (ox + 4, oy + 17), (ox + 16, oy + 17), (ox + 17, oy + 25),
            (ox + 13, oy + 26), (ox + 10, oy + 23), (ox + 7, oy + 26), (ox + 3, oy + 25)
        ])
        pygame.draw.rect(surface, hoodie_dark, (ox + 7, oy + 19, 6, 6))
        pygame.draw.rect(surface, pants, (ox + 5, oy + 24, 5, 5))
        pygame.draw.rect(surface, pants, (ox + 11, oy + 25, 5, 4))
        pygame.draw.rect(surface, shoes, (ox + 3, oy + 28, 7, 2))
        pygame.draw.rect(surface, shoes, (ox + 11, oy + 28, 7, 2))
        pygame.draw.rect(surface, hoodie, (ox + 1, oy + 20, 3, 7))
        pygame.draw.rect(surface, hoodie, (ox + 17, oy + 20, 3, 7))
        pygame.draw.rect(surface, skin, (ox + 1, oy + 26, 3, 2))
        pygame.draw.rect(surface, skin, (ox + 17, oy + 26, 3, 2))

        # Bowed face: normal closed eyes, not symbolic X marks.
        pygame.draw.rect(surface, hair_dark, (ox + 4, oy + 5, 13, 3))
        pygame.draw.rect(surface, hair, (ox + 3, oy + 7, 15, 4))
        pygame.draw.rect(surface, skin_shadow, (ox + 5, oy + 11, 11, 5))
        pygame.draw.line(surface, brow, (ox + 6, oy + 13), (ox + 9, oy + 13), 1)
        pygame.draw.line(surface, brow, (ox + 12, oy + 13), (ox + 15, oy + 13), 1)
        pygame.draw.line(surface, mouth, (ox + 9, oy + 15), (ox + 12, oy + 15), 1)
        return

    torso_y = oy + 15
    left_leg_y = oy + 25 + (1 if walking and leg_phase == 1 else 0)
    right_leg_y = oy + 25 + (1 if walking and leg_phase == 0 else 0)

    if direction == "up":
        # Approved Option 3 rear hairstyle: slightly longer, layered and natural.
        # Front/side sprites remain untouched. The irregular lower edge prevents
        # the old round helmet/mushroom silhouette while keeping a tidy nape.
        pygame.draw.polygon(surface, hair_dark, [
            (ox + 5, oy + 2), (ox + 8, oy), (ox + 14, oy), (ox + 17, oy + 2),
            (ox + 19, oy + 5), (ox + 18, oy + 9), (ox + 17, oy + 11),
            (ox + 15, oy + 11), (ox + 14, oy + 13), (ox + 12, oy + 12),
            (ox + 10, oy + 14), (ox + 8, oy + 12), (ox + 6, oy + 13),
            (ox + 5, oy + 10), (ox + 3, oy + 9), (ox + 3, oy + 5)
        ])
        pygame.draw.polygon(surface, hair, [
            (ox + 6, oy + 2), (ox + 9, oy + 1), (ox + 14, oy + 1),
            (ox + 17, oy + 3), (ox + 18, oy + 6), (ox + 16, oy + 9),
            (ox + 15, oy + 11), (ox + 13, oy + 10), (ox + 12, oy + 12),
            (ox + 10, oy + 11), (ox + 8, oy + 12), (ox + 7, oy + 10),
            (ox + 5, oy + 10), (ox + 4, oy + 7), (ox + 5, oy + 4)
        ])
        # Crown highlights and separated strands give the hair volume without
        # changing the character palette or making it look long.
        pygame.draw.rect(surface, hair_light, (ox + 7, oy + 2, 4, 1))
        pygame.draw.rect(surface, hair_light, (ox + 12, oy + 2, 3, 1))
        pygame.draw.rect(surface, hair_light, (ox + 15, oy + 4, 2, 1))
        pygame.draw.line(surface, hair_dark, (ox + 7, oy + 5), (ox + 6, oy + 9), 1)
        pygame.draw.line(surface, hair_dark, (ox + 10, oy + 4), (ox + 9, oy + 11), 1)
        pygame.draw.line(surface, hair_dark, (ox + 13, oy + 4), (ox + 12, oy + 11), 1)
        pygame.draw.line(surface, hair_dark, (ox + 16, oy + 5), (ox + 15, oy + 10), 1)
        # Small ears and a broader neck/nape keep the head visibly attached
        # to the hoodie even when a bright room line passes behind the sprite.
        pygame.draw.rect(surface, skin_shadow, (ox + 3, oy + 7, 2, 3))
        pygame.draw.rect(surface, skin_shadow, (ox + 17, oy + 7, 2, 3))
        pygame.draw.rect(surface, skin_shadow, (ox + 8, oy + 11, 6, 5))
        pygame.draw.rect(surface, skin, (ox + 9, oy + 12, 4, 4))

        # Raise the shoulders into the neck by two pixels so there is no
        # background-colored gap between head and body.
        pygame.draw.polygon(surface, hoodie_light, [
            (ox + 7, torso_y - 2), (ox + 14, torso_y - 2),
            (ox + 19, torso_y + 3), (ox + 18, torso_y + 7),
            (ox + 15, torso_y + 9), (ox + 6, torso_y + 9),
            (ox + 3, torso_y + 7), (ox + 2, torso_y + 3)
        ])
        pygame.draw.polygon(surface, hoodie, [
            (ox + 6, torso_y + 1), (ox + 15, torso_y + 1),
            (ox + 17, torso_y + 11), (ox + 14, torso_y + 13),
            (ox + 7, torso_y + 13), (ox + 4, torso_y + 11)
        ])
        pygame.draw.arc(surface, hoodie_dark, (ox + 7, torso_y + 2, 8, 7), 0, math.pi, 1)
        pygame.draw.line(surface, hoodie_light, (ox + 7, torso_y + 12), (ox + 14, torso_y + 12), 1)

    elif direction in ("left", "right"):
        # Keep the approved side profile, only normalize it to the final proportions.
        facing_right = direction == "right"
        hx = ox + (5 if facing_right else 4)
        pygame.draw.rect(surface, skin, (hx, oy + 5, 11, 10))
        pygame.draw.rect(surface, skin_shadow, (hx, oy + 13, 11, 2))
        pygame.draw.rect(surface, hair_dark, (hx, oy + 1, 11, 2))
        pygame.draw.rect(surface, hair, (hx - (1 if not facing_right else 0), oy + 3, 13, 4))
        tuft_x = hx - 2 if facing_right else hx + 10
        pygame.draw.rect(surface, hair, (tuft_x, oy + 5, 3, 6))
        pygame.draw.rect(surface, hair_light, (hx + 3, oy + 2, 4, 1))

        if facing_right:
            pygame.draw.rect(surface, brow, (hx + 7, oy + 7, 3, 1))
            pygame.draw.rect(surface, eye, (hx + 8, oy + 8, 2, 2))
            pygame.draw.rect(surface, WHITE, (hx + 8, oy + 8, 1, 1))
            pygame.draw.rect(surface, skin_light, (hx + 10, oy + 10, 2, 2))
            pygame.draw.rect(surface, mouth, (hx + 8, oy + 13, 3, 1))
        else:
            pygame.draw.rect(surface, brow, (hx + 1, oy + 7, 3, 1))
            pygame.draw.rect(surface, eye, (hx + 1, oy + 8, 2, 2))
            pygame.draw.rect(surface, WHITE, (hx + 1, oy + 8, 1, 1))
            pygame.draw.rect(surface, skin_light, (hx - 1, oy + 10, 2, 2))
            pygame.draw.rect(surface, mouth, (hx, oy + 13, 3, 1))

        pygame.draw.polygon(surface, hoodie_light, [
            (ox + 5, torso_y), (ox + 16, torso_y), (ox + 19, torso_y + 4),
            (ox + 17, torso_y + 7), (ox + 4, torso_y + 7), (ox + 2, torso_y + 4)
        ])
        pygame.draw.rect(surface, hoodie, (ox + 4, torso_y + 3, 13, 9))
        # Keep the side hoodie clean too; the old cyan chest block was the badge.
        chest_x = ox + (13 if facing_right else 5)
        pygame.draw.line(surface, hoodie_dark, (chest_x, torso_y + 9), (chest_x + 2, torso_y + 9), 1)

    else:
        # Refined front: tapered face, asymmetrical hairline, neck, hood,
        # drawstrings, with a clean badge-free hoodie front.
        pygame.draw.polygon(surface, skin_shadow, [
            (ox + 5, oy + 6), (ox + 16, oy + 6), (ox + 18, oy + 9),
            (ox + 17, oy + 13), (ox + 14, oy + 15), (ox + 7, oy + 15),
            (ox + 4, oy + 13), (ox + 3, oy + 9)
        ])
        pygame.draw.polygon(surface, skin, [
            (ox + 6, oy + 5), (ox + 15, oy + 5), (ox + 17, oy + 9),
            (ox + 16, oy + 13), (ox + 13, oy + 15), (ox + 8, oy + 15),
            (ox + 5, oy + 13), (ox + 4, oy + 9)
        ])
        pygame.draw.rect(surface, skin, (ox + 3, oy + 9, 2, 4))
        pygame.draw.rect(surface, skin, (ox + 16, oy + 9, 2, 4))
        pygame.draw.rect(surface, skin_light, (ox + 6, oy + 6, 3, 2))

        pygame.draw.polygon(surface, hair_dark, [
            (ox + 6, oy + 1), (ox + 15, oy + 1), (ox + 18, oy + 4),
            (ox + 18, oy + 7), (ox + 15, oy + 6), (ox + 13, oy + 5),
            (ox + 7, oy + 5), (ox + 5, oy + 7), (ox + 3, oy + 6), (ox + 3, oy + 4)
        ])
        pygame.draw.rect(surface, hair, (ox + 5, oy + 2, 11, 3))
        pygame.draw.rect(surface, hair, (ox + 3, oy + 4, 3, 6))
        pygame.draw.rect(surface, hair, (ox + 15, oy + 4, 3, 5))
        pygame.draw.rect(surface, hair, (ox + 7, oy + 5, 7, 1))
        pygame.draw.rect(surface, hair_light, (ox + 8, oy + 2, 4, 1))

        pygame.draw.rect(surface, brow, (ox + 7, oy + 7, 2, 1))
        pygame.draw.rect(surface, brow, (ox + 12, oy + 7, 2, 1))
        pygame.draw.rect(surface, eye, (ox + 7, oy + 8, 2, 2))
        pygame.draw.rect(surface, eye, (ox + 12, oy + 8, 2, 2))
        pygame.draw.rect(surface, WHITE, (ox + 7, oy + 8, 1, 1))
        pygame.draw.rect(surface, WHITE, (ox + 12, oy + 8, 1, 1))
        pygame.draw.rect(surface, skin_shadow, (ox + 10, oy + 10, 1, 2))
        pygame.draw.line(surface, mouth, (ox + 9, oy + 13), (ox + 12, oy + 13), 1)
        # Front-only neck/hood correction. Keep the neck visibly connected,
        # but start the shoulders lower so the hoodie never climbs into the jaw.
        pygame.draw.rect(surface, skin_shadow, (ox + 8, oy + 14, 6, 3))
        pygame.draw.rect(surface, skin, (ox + 9, oy + 14, 4, 3))

        # Restore the cleaner front silhouette used before the rear-view fix.
        # IMPORTANT: this block is front-facing only; the approved back sprite
        # above remains completely unchanged.
        pygame.draw.polygon(surface, hoodie_light, [
            (ox + 5, torso_y), (ox + 16, torso_y),
            (ox + 19, torso_y + 4), (ox + 18, torso_y + 7),
            (ox + 15, torso_y + 9), (ox + 6, torso_y + 9),
            (ox + 3, torso_y + 7), (ox + 2, torso_y + 4)
        ])
        pygame.draw.polygon(surface, hoodie, [
            (ox + 5, torso_y + 3), (ox + 16, torso_y + 3),
            (ox + 17, torso_y + 11), (ox + 14, torso_y + 13),
            (ox + 7, torso_y + 13), (ox + 4, torso_y + 11)
        ])

        # Short, slightly angled drawstrings read as hoodie cords instead of
        # a pause-symbol. Keep the chest clean with no ID badge.
        cord = (226, 229, 235)
        pygame.draw.line(surface, cord, (ox + 8, torso_y + 3), (ox + 9, torso_y + 6), 1)
        pygame.draw.line(surface, cord, (ox + 13, torso_y + 3), (ox + 12, torso_y + 6), 1)
        pygame.draw.rect(surface, hoodie_dark, (ox + 9, torso_y + 6, 1, 1))
        pygame.draw.rect(surface, hoodie_dark, (ox + 12, torso_y + 6, 1, 1))
        pygame.draw.line(surface, hoodie_dark, (ox + 8, torso_y + 10), (ox + 13, torso_y + 10), 1)

    # Arms use the same attachment points in every orientation.
    if celebrate and direction != "up":
        pygame.draw.rect(surface, hoodie, (ox + 1, torso_y - 3, 3, 9))
        pygame.draw.rect(surface, hoodie, (ox + 17, torso_y - 3, 3, 9))
        pygame.draw.rect(surface, skin, (ox + 1, torso_y - 6, 3, 3))
        pygame.draw.rect(surface, skin, (ox + 17, torso_y - 6, 3, 3))
    else:
        arm_a = 1 if walking and leg_phase == 0 else 0
        arm_b = 1 if walking and leg_phase == 1 else 0
        pygame.draw.rect(surface, hoodie, (ox + 1, torso_y + 3 + arm_a, 3, 7))
        pygame.draw.rect(surface, hoodie, (ox + 17, torso_y + 3 + arm_b, 3, 7))
        pygame.draw.rect(surface, skin, (ox + 1, torso_y + 9 + arm_a, 3, 2))
        pygame.draw.rect(surface, skin, (ox + 17, torso_y + 9 + arm_b, 3, 2))

    # Shared legs/shoes keep every angle on-model.
    pygame.draw.rect(surface, pants, (ox + 5, left_leg_y, 5, 4))
    pygame.draw.rect(surface, pants, (ox + 11, right_leg_y, 5, 4))
    pygame.draw.rect(surface, shoes, (ox + 4, left_leg_y + 4, 6, 2))
    pygame.draw.rect(surface, WHITE, (ox + 6, left_leg_y + 4, 3, 1))
    pygame.draw.rect(surface, shoes, (ox + 11, right_leg_y + 4, 6, 2))
    pygame.draw.rect(surface, WHITE, (ox + 12, right_leg_y + 4, 3, 1))


def direction_door_rect(direction, room_name=None):
    room_name = room_name or current_room
    room_map = ROOM_DOOR_RECTS.get(room_name, {})
    if direction in room_map:
        return pygame.Rect(*room_map[direction])

    if direction == "north":
        return pygame.Rect(84, 43, 44, 38)
    if direction == "south":
        return pygame.Rect(84, 94, 44, 38)
    if direction == "west":
        return pygame.Rect(12, 69, 28, 45)
    return pygame.Rect(171, 69, 28, 45)


def door_center(direction):
    rect = direction_door_rect(direction)
    return pygame.Vector2(rect.centerx, rect.centery)


def door_distance(direction):
    return get_player_center().distance_to(door_center(direction))


def is_near_door(direction):
    threshold = 31 if direction in ("north", "south") else 28
    return door_distance(direction) <= threshold


def item_position(room_name):
    return ITEM_POSITIONS.get(room_name, (145, 78))


def item_distance(room_name):
    x, y = item_position(room_name)
    return get_player_center().distance_to(pygame.Vector2(x + 9, y + 10))


def nearest_interaction():
    if game_state != "game" or current_room == "Control Room":
        return None, None

    candidates = []
    room = rooms[current_room]

    item = room.get("item")
    if item and item not in collected_items:
        distance = item_distance(current_room)
        if distance <= 26:
            candidates.append((distance, "item", item))

    for direction in ("north", "south", "west", "east"):
        if direction in room:
            distance = door_distance(direction)
            threshold = 31 if direction in ("north", "south") else 28
            if distance <= threshold:
                candidates.append((distance, "door", direction))

    if not candidates:
        return None, None

    candidates.sort(key=lambda candidate: candidate[0])
    _, interaction_type, value = candidates[0]
    return interaction_type, value


def update_door_animations():
    for direction in ("north", "south", "west", "east"):
        if direction not in rooms[current_room]:
            continue
        key = (current_room, direction)
        target = 1.0 if is_near_door(direction) else 0.0
        speed = 0.09
        if door_progress[key] < target:
            door_progress[key] = min(target, door_progress[key] + speed)
        elif door_progress[key] > target:
            door_progress[key] = max(target, door_progress[key] - speed)

# --------------------------------------------------
# TRANSITIONS / GAME LOGIC
# --------------------------------------------------



def spawn_from_direction(travel_direction):
    """Place the player on the threshold of the exact doorway just used.

    The player never auto-walks into the room. The transition ends with the
    character visibly standing in the doorway, facing into the destination,
    so the player chooses the first step.
    """
    global player_x, player_y, player_direction

    entry_direction = opposite_direction(travel_direction)
    rect = direction_door_rect(entry_direction, current_room)

    if entry_direction == "north":
        player_x = rect.centerx - PLAYER_W // 2
        player_y = rect.bottom - PLAYER_H + 8
        player_direction = "down"
    elif entry_direction == "south":
        player_x = rect.centerx - PLAYER_W // 2
        player_y = rect.y - 4
        player_direction = "up"
    elif entry_direction == "west":
        player_x = rect.right - 5
        player_y = rect.centery - PLAYER_H // 2
        player_direction = "right"
    else:
        player_x = rect.x - PLAYER_W + 5
        player_y = rect.centery - PLAYER_H // 2
        player_direction = "left"

    player_x = clamp(player_x, PLAY_MIN_X, PLAY_MAX_X)
    player_y = clamp(player_y, PLAY_MIN_Y, PLAY_MAX_Y)


def start_room_transition(target_room, direction):
    global transition_active, transition_alpha, transition_phase
    global transition_target, transition_direction, pending_result

    play_sound("transition")
    transition_active = True
    transition_alpha = 0
    transition_phase = "out"
    transition_target = target_room
    transition_direction = direction
    pending_result = None

    if target_room == "Control Room":
        pending_result = "victory" if len(collected_items) == 6 else "defeat"


def update_transition():
    global transition_active, transition_alpha, transition_phase
    global current_room, game_state, result_timer, pending_result

    if not transition_active:
        return

    if transition_phase == "out":
        transition_alpha += 22
        if transition_alpha >= 255:
            transition_alpha = 255
            current_room = transition_target
            spawn_from_direction(transition_direction)

            if pending_result:
                game_state = pending_result
                result_timer = 0
                play_sound("victory" if pending_result == "victory" else "warning")

            transition_phase = "in"
    else:
        transition_alpha -= 22
        if transition_alpha <= 0:
            transition_alpha = 0
            transition_active = False


def reset_game():
    global game_state, current_room, inventory, collected_items
    global player_x, player_y, player_direction, walk_frame, walk_timer, is_walking
    global interaction_message, message_timer
    global transition_active, transition_alpha, transition_phase
    global transition_target, transition_direction, pending_result, result_timer

    game_state = "game"
    current_room = "Main Lobby"
    inventory = []
    collected_items = set()

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
    transition_target = None
    transition_direction = None
    pending_result = None
    result_timer = 0

    for key in door_progress:
        door_progress[key] = 0.0


def handle_interaction():
    global interaction_message, message_timer

    interaction_type, value = nearest_interaction()

    if interaction_type == "item":
        if value not in collected_items:
            collected_items.add(value)
            inventory.append(value)
            play_sound("pickup")
            interaction_message = value.upper() + " RECOVERED"
            message_timer = 100

    elif interaction_type == "door":
        destination = rooms[current_room][value]
        start_room_transition(destination, value)

    else:
        interaction_message = "MOVE CLOSER TO A DOOR OR SECURITY TOOL"
        message_timer = 75

# --------------------------------------------------
# ROOM SHELL / COMMON WORLD ART
# --------------------------------------------------


def draw_room_shell(surface, accent):
    """Shared 2.5D room architecture: recessed wall, perspective floor, bevels, shadows."""
    # Outer room recess.
    pygame.draw.rect(surface, (8, 13, 23), ROOM_RECT)
    pygame.draw.rect(surface, (5, 9, 17), (ROOM_RECT.x + 2, ROOM_RECT.y + 2, ROOM_RECT.w - 4, ROOM_RECT.h - 4))

    wall = pygame.Rect(ROOM_RECT.x + 4, ROOM_RECT.y + 5, ROOM_RECT.w - 8, 63)
    pygame.draw.rect(surface, WALL, wall)

    # Side-wall shading produces depth instead of a flat poster wall.
    pygame.draw.polygon(surface, (23, 32, 47), [
        (wall.x, wall.y), (wall.x + 11, wall.y + 6), (wall.x + 11, wall.bottom), (wall.x, wall.bottom)
    ])
    pygame.draw.polygon(surface, (18, 27, 41), [
        (wall.right, wall.y), (wall.right - 11, wall.y + 6), (wall.right - 11, wall.bottom), (wall.right, wall.bottom)
    ])

    # Recessed ceiling with light strip and beveled lower edge.
    pygame.draw.polygon(surface, (34, 46, 62), [
        (wall.x + 10, wall.y), (wall.right - 10, wall.y), (wall.right - 16, wall.y + 8), (wall.x + 16, wall.y + 8)
    ])
    pygame.draw.line(surface, accent, (wall.x + 6, wall.y + 1), (wall.right - 6, wall.y + 1), 1)
    pygame.draw.line(surface, (49, 62, 80), (wall.x + 15, wall.y + 8), (wall.right - 15, wall.y + 8), 1)

    # Wall panel seams with alternating highlights/shadows.
    for x in (ROOM_RECT.x + 20, ROOM_RECT.x + 61, ROOM_RECT.x + 102, ROOM_RECT.x + 143, ROOM_RECT.x + 184):
        pygame.draw.line(surface, (18, 27, 41), (x, wall.y + 10), (x, wall.bottom - 2), 2)
        pygame.draw.line(surface, (39, 51, 69), (x + 2, wall.y + 10), (x + 2, wall.bottom - 2), 1)

    # Baseboard creates a horizon; floor becomes a perspective plane.
    horizon_y = ROOM_RECT.y + 72
    pygame.draw.rect(surface, (14, 20, 32), (ROOM_RECT.x + 3, horizon_y - 2, ROOM_RECT.w - 6, 4))
    pygame.draw.line(surface, accent, (ROOM_RECT.x + 5, horizon_y - 1), (ROOM_RECT.right - 5, horizon_y - 1), 1)

    floor_poly = [
        (ROOM_RECT.x + 3, horizon_y),
        (ROOM_RECT.right - 3, horizon_y),
        (ROOM_RECT.right - 7, ROOM_RECT.bottom - 3),
        (ROOM_RECT.x + 7, ROOM_RECT.bottom - 3),
    ]
    pygame.draw.polygon(surface, FLOOR, floor_poly)

    # Perspective floor lines converge toward the room center.
    vanish_x = ROOM_RECT.centerx
    for bottom_x in range(ROOM_RECT.x + 12, ROOM_RECT.right - 6, 24):
        pygame.draw.line(surface, FLOOR_LINE, (vanish_x, horizon_y), (bottom_x, ROOM_RECT.bottom - 4), 1)
    for y in (horizon_y + 8, horizon_y + 19, ROOM_RECT.bottom - 5):
        inset = int((y - horizon_y) * 0.18)
        pygame.draw.line(surface, FLOOR_LINE, (ROOM_RECT.x + 5 + inset, y), (ROOM_RECT.right - 5 - inset, y), 1)

    # Ceiling fixtures cast a tiny light pool to help the room feel occupied.
    for x in (37, 96, 155):
        pygame.draw.rect(surface, METAL, (x, ROOM_RECT.y + 10, 22, 3))
        pygame.draw.rect(surface, accent, (x + 5, ROOM_RECT.y + 11, 12, 1))
        pygame.draw.polygon(surface, mix_color(WALL, accent, 0.10), [
            (x + 4, ROOM_RECT.y + 14), (x + 18, ROOM_RECT.y + 14),
            (x + 22, horizon_y - 4), (x, horizon_y - 4)
        ])

def draw_status_monitor(surface, x, y, width=28, height=17, accent=CYAN, alert=False):
    pygame.draw.rect(surface, (6, 10, 18), (x, y, width, height))
    pygame.draw.rect(surface, METAL, (x - 2, y - 2, width + 4, height + 4))
    pygame.draw.rect(surface, accent, (x, y, width, height), 1)

    line_color = RED if alert else GREEN
    pygame.draw.rect(surface, line_color, (x + 4, y + 4, width - 11, 2))
    pygame.draw.rect(surface, accent, (x + 4, y + 9, width - 7, 2))
    pygame.draw.rect(surface, line_color, (x + 4, y + 13, width - 13, 1))


def draw_keyboard(surface, x, y, width=24):
    pygame.draw.rect(surface, (50, 59, 75), (x, y, width, 4))
    for key_x in range(x + 2, x + width - 2, 4):
        pygame.draw.rect(surface, (102, 115, 136), (key_x, y + 1, 2, 1))


def draw_warning_beacon(surface, x, y):
    on = (frame_counter // 18) % 2 == 0
    glow = RED if on else (105, 38, 43)
    pygame.draw.rect(surface, (72, 37, 33), (x - 2, y + 6, 18, 3))
    pygame.draw.rect(surface, glow, (x, y + 2, 14, 5))
    pygame.draw.rect(surface, (255, 149, 108) if on else (143, 69, 58), (x + 4, y + 2, 6, 1))
    if on:
        pygame.draw.line(surface, (110, 38, 43), (x - 5, y + 4), (x - 1, y + 4), 1)
        pygame.draw.line(surface, (110, 38, 43), (x + 15, y + 4), (x + 19, y + 4), 1)


def draw_access_reader(surface, x, y, dangerous=False, accent=CYAN):
    color = RED if dangerous else accent
    pygame.draw.rect(surface, (10, 16, 28), (x, y, 8, 17))
    pygame.draw.rect(surface, METAL, (x, y, 8, 17), 1)
    pygame.draw.rect(surface, color, (x + 2, y + 3, 4, 4))
    pygame.draw.rect(surface, CYAN, (x + 2, y + 9, 1, 2))
    pygame.draw.rect(surface, CYAN, (x + 5, y + 9, 1, 2))
    pygame.draw.rect(surface, CYAN, (x + 2, y + 13, 1, 2))
    pygame.draw.rect(surface, CYAN, (x + 5, y + 13, 1, 2))

# --------------------------------------------------
# DOOR ART
# --------------------------------------------------



def draw_door_sign(surface, direction, destination, accent):
    """Door text is rendered at native 960x540 resolution in draw_world_door_labels()."""
    return

def draw_sliding_door(surface, direction, progress, destination):
    rect = direction_door_rect(direction)

    control_door = destination == "Control Room"
    if control_door and len(collected_items) == 6:
        accent = GREEN
    elif control_door and "Access Card" in collected_items:
        accent = YELLOW
    elif control_door:
        accent = RED
    else:
        accent = ROOM_ACCENTS.get(current_room, CYAN)

    # Recess shadow makes the door sit inside the wall instead of on top of it.
    shadow_rect = rect.inflate(8, 6)
    pygame.draw.rect(surface, (4, 7, 13), shadow_rect)
    pygame.draw.rect(surface, (18, 26, 39), shadow_rect, 1)

    # Top and side faces create a chunky 2.5D metal frame.
    pygame.draw.polygon(surface, (85, 97, 117), [
        (rect.x - 3, rect.y - 3), (rect.right + 3, rect.y - 3),
        (rect.right, rect.y), (rect.x, rect.y)
    ])
    pygame.draw.polygon(surface, (45, 57, 76), [
        (rect.x - 3, rect.y - 3), (rect.x, rect.y),
        (rect.x, rect.bottom), (rect.x - 3, rect.bottom + 2)
    ])
    pygame.draw.polygon(surface, (27, 37, 53), [
        (rect.right, rect.y), (rect.right + 3, rect.y - 3),
        (rect.right + 3, rect.bottom + 2), (rect.right, rect.bottom)
    ])

    pygame.draw.rect(surface, (5, 8, 14), rect)
    pygame.draw.rect(surface, accent, rect, 1)
    pygame.draw.rect(surface, METAL_LIGHT, (rect.x + 4, rect.y + 3, rect.w - 8, 2))

    inner = pygame.Rect(rect.x + 4, rect.y + 6, rect.w - 8, rect.h - 10)
    pygame.draw.rect(surface, (5, 8, 15), inner)

    half = inner.w // 2
    slide = int(half * progress)
    left_panel = pygame.Rect(inner.x - slide, inner.y, half + 1, inner.h)
    right_panel = pygame.Rect(inner.centerx + slide, inner.y, half + 1, inner.h)

    for panel, shade in ((left_panel, (44, 56, 75)), (right_panel, (36, 48, 66))):
        clipped = panel.clip(inner)
        if clipped.w > 0:
            pygame.draw.rect(surface, shade, clipped)
            pygame.draw.rect(surface, (73, 86, 108), clipped, 1)
            for ry in range(inner.y + 7, inner.bottom - 3, 8):
                pygame.draw.line(surface, (54, 67, 87),
                                 (clipped.x + 1, ry), (clipped.right - 1, ry), 1)

    if progress < 0.92:
        pygame.draw.line(surface, (111, 125, 147), (inner.centerx, inner.y + 1),
                         (inner.centerx, inner.bottom - 2), 1)

    # Door track / floor light.
    threshold_color = GREEN if progress > 0.7 and not control_door else accent
    pygame.draw.rect(surface, (8, 12, 20), (rect.x + 2, rect.bottom - 3, rect.w - 4, 3))
    pygame.draw.rect(surface, threshold_color, (rect.x + 5, rect.bottom - 2, rect.w - 10, 1))

    reader_x = rect.right + 3 if direction != "east" else rect.x - 11
    reader_y = rect.y + rect.h // 2 - 8
    draw_access_reader(surface, reader_x, reader_y, control_door and len(collected_items) < 6, accent)

def draw_item_display(surface, item_name, x, y):
    """Secure equipment bay with 2.5D pedestal and a collectible that reads as an object."""
    color = ITEM_DATA[item_name]["color"]
    glow_strength = pulse(12, 0.18, 0.82)
    glow_color = mix_color((20, 28, 43), color, glow_strength * 0.22)

    # Ground shadow and pedestal front/side faces.
    pygame.draw.ellipse(surface, (5, 8, 14), (x - 6, y + 22, 31, 6))
    pygame.draw.polygon(surface, (31, 41, 57), [
        (x - 5, y + 16), (x + 23, y + 16), (x + 20, y + 23), (x - 2, y + 23)
    ])
    pygame.draw.polygon(surface, (18, 26, 39), [
        (x + 23, y + 16), (x + 26, y + 19), (x + 23, y + 25), (x + 20, y + 23)
    ])
    pygame.draw.polygon(surface, (42, 53, 71), [
        (x - 5, y + 16), (x - 2, y + 23), (x - 2, y + 25), (x - 7, y + 20)
    ])
    pygame.draw.line(surface, color, (x - 3, y + 17), (x + 21, y + 17), 1)

    # Glass/security enclosure.
    case = pygame.Rect(x, y - 6, 19, 22)
    pygame.draw.rect(surface, glow_color, case)
    pygame.draw.rect(surface, mix_color(METAL, color, 0.15), case, 1)
    pygame.draw.line(surface, mix_color(color, WHITE, 0.35),
                     (case.x + 2, case.y + 2), (case.x + 2, case.bottom - 3), 1)
    pygame.draw.line(surface, (83, 96, 116),
                     (case.right - 2, case.y + 3), (case.right - 2, case.bottom - 3), 1)

    # Icon remains readable but no longer dominates the room.
    draw_item_icon(surface, item_name, x, y - 1, color)
    pygame.draw.rect(surface, GREEN, (x + 21, y + 19, 2, 2))

def draw_main_lobby(surface):
    # Reception counter with monitor, keyboard, badge scanner, and chair.
    pygame.draw.rect(surface, (64, 50, 42), (47, 82, 59, 7))
    pygame.draw.rect(surface, (43, 34, 29), (51, 89, 5, 16))
    pygame.draw.rect(surface, (43, 34, 29), (96, 89, 5, 16))
    draw_status_monitor(surface, 59, 58, 29, 17, CYAN)
    draw_keyboard(surface, 61, 78, 23)
    pygame.draw.rect(surface, (16, 23, 35), (87, 74, 8, 8))
    pygame.draw.rect(surface, GREEN, (89, 76, 4, 2))
    pygame.draw.rect(surface, (25, 31, 44), (69, 93, 14, 8))
    pygame.draw.rect(surface, METAL, (73, 101, 6, 5))

    # Corporate directory kiosk.
    pygame.draw.rect(surface, (10, 16, 29), (46, 49, 23, 26))
    pygame.draw.rect(surface, CYAN, (46, 49, 23, 26), 1)
    pygame.draw.rect(surface, WHITE, (51, 54, 13, 2))
    pygame.draw.rect(surface, GREEN, (51, 60, 10, 2))
    pygame.draw.rect(surface, CYAN, (51, 66, 13, 2))
    pygame.draw.rect(surface, METAL, (54, 75, 6, 5))

    # Company shield mark.
    pygame.draw.rect(surface, (11, 18, 30), (115, 52, 19, 20))
    pygame.draw.rect(surface, METAL, (115, 52, 19, 20), 1)
    pygame.draw.polygon(surface, CYAN,
                        [(124, 55), (130, 58), (128, 66), (124, 69), (120, 66), (118, 58)], 1)
    pygame.draw.rect(surface, GREEN, (123, 59, 3, 5))

    # Intrusion panel and beacon.
    pygame.draw.rect(surface, (13, 20, 34), (145, 57, 28, 25))
    pygame.draw.rect(surface, METAL, (145, 57, 28, 25), 1)
    pygame.draw.rect(surface, RED, (151, 62, 16, 3))
    pygame.draw.rect(surface, GRAY, (151, 70, 9, 1))
    pygame.draw.rect(surface, GRAY, (151, 74, 14, 1))
    draw_warning_beacon(surface, 164, 47)

    # Camera aimed toward the final corridor.
    pygame.draw.rect(surface, METAL, (108, 47, 11, 4))
    pygame.draw.polygon(surface, (18, 25, 38), [(118, 49), (126, 52), (118, 55)])
    pygame.draw.circle(surface, RED if (frame_counter // 25) % 2 else GREEN, (122, 52), 1)



def draw_security_office(surface):
    # CCTV wall with feed numbers and varied alerts.
    feed_font = pygame.font.SysFont("consolas", 5, bold=True)
    monitor_positions = [(29, 53), (54, 53), (29, 70), (54, 70), (79, 53), (79, 70)]
    for index, (x, y) in enumerate(monitor_positions, start=1):
        pygame.draw.rect(surface, (5, 10, 18), (x, y, 20, 13))
        pygame.draw.rect(surface, GREEN, (x, y, 20, 13), 1)
        pygame.draw.rect(surface, GREEN if index % 3 else RED, (x + 3, y + 4, 5, 2))
        pygame.draw.line(surface, CYAN, (x + 3, y + 9), (x + 16, y + 9), 1)
        pygame.draw.rect(surface, (30, 46, 59), (x + 12, y + 4, 4, 3))
        surface.blit(feed_font.render(f"C{index}", True, GRAY), (x + 2, y + 1))

    # Security operator workstation.
    pygame.draw.rect(surface, (42, 46, 56), (26, 88, 84, 6))
    pygame.draw.rect(surface, METAL, (34, 94, 5, 15))
    pygame.draw.rect(surface, METAL, (99, 94, 5, 15))
    draw_status_monitor(surface, 111, 56, 23, 15, GREEN)
    draw_keyboard(surface, 112, 74, 20)
    pygame.draw.rect(surface, (24, 31, 43), (61, 95, 14, 8))
    pygame.draw.rect(surface, METAL, (65, 103, 6, 4))

    # Access-control map and camera hardware.
    pygame.draw.rect(surface, (8, 14, 25), (112, 87, 22, 18))
    pygame.draw.rect(surface, GREEN, (112, 87, 22, 18), 1)
    pygame.draw.line(surface, CYAN, (116, 99), (130, 92), 1)
    pygame.draw.rect(surface, GREEN, (115, 97, 2, 2))
    pygame.draw.rect(surface, RED, (129, 91, 2, 2))
    pygame.draw.rect(surface, METAL, (160, 52, 15, 4))
    pygame.draw.polygon(surface, (12, 19, 31), [(175, 52), (184, 57), (175, 60)])
    pygame.draw.circle(surface, RED, (180, 57), 1)



def draw_network_ops(surface):
    # Rack banks leave a broad center aisle. The south exit sits apart on the lower-left.
    for rack_x in (27, 52, 151, 176):
        pygame.draw.rect(surface, (6, 11, 20), (rack_x, 51, 18, 40))
        pygame.draw.rect(surface, BLUE, (rack_x, 51, 18, 40), 1)
        for row in range(5):
            y = 56 + row * 7
            light = GREEN if (frame_counter // 10 + row + rack_x) % 4 else RED
            pygame.draw.rect(surface, light, (rack_x + 4, y, 3, 2))
            pygame.draw.rect(surface, CYAN, (rack_x + 9, y, 6, 1))

    # Large live topology wall.
    board = pygame.Rect(76, 51, 54, 29)
    pygame.draw.rect(surface, (7, 13, 24), board)
    pygame.draw.rect(surface, BLUE, board, 1)
    pygame.draw.rect(surface, CYAN, (80, 55, 46, 2))
    nodes = [(83, 68), (94, 61), (106, 70), (118, 61), (124, 73), (95, 75)]
    connections = [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5), (5, 0)]
    for a, b in connections:
        pygame.draw.line(surface, CYAN, nodes[a], nodes[b], 1)
    for index, (nx, ny) in enumerate(nodes):
        color = GREEN if (frame_counter // 14 + index) % 3 else RED
        pygame.draw.rect(surface, color, (nx - 1, ny - 1, 3, 3))

    # Angled operator island away from the Firewall Key.
    pygame.draw.polygon(surface, (32, 41, 58), [(70, 90), (127, 90), (119, 98), (78, 98)])
    pygame.draw.polygon(surface, METAL, [(70, 90), (127, 90), (119, 98), (78, 98)], 1)
    pygame.draw.rect(surface, CYAN, (82, 92, 13, 1))
    pygame.draw.rect(surface, RED, (101, 92, 8, 1))
    pygame.draw.rect(surface, GREEN, (112, 92, 6, 1))

    # Overhead network trunk.
    pygame.draw.line(surface, BLUE, (28, 47), (190, 47), 2)
    for x in (36, 61, 159, 184):
        pygame.draw.line(surface, CYAN, (x, 47), (x, 51), 1)



def draw_it_office(surface):
    # Technician benches with diagnostic monitors and keyboards.
    for desk_x, alert in ((25, False), (78, True)):
        pygame.draw.rect(surface, (58, 49, 44), (desk_x, 82, 43, 6))
        pygame.draw.rect(surface, METAL, (desk_x + 6, 88, 4, 15))
        pygame.draw.rect(surface, METAL, (desk_x + 33, 88, 4, 15))
        draw_status_monitor(surface, desk_x + 9, 55, 25, 16, CYAN, alert=alert)
        draw_keyboard(surface, desk_x + 11, 76, 21)

    # Open repair chassis gives the room a clear technician-workbench identity.
    pygame.draw.rect(surface, (11, 18, 29), (119, 55, 24, 23))
    pygame.draw.rect(surface, METAL, (119, 55, 24, 23), 1)
    pygame.draw.rect(surface, CYAN, (123, 59, 8, 5))
    pygame.draw.rect(surface, GREEN, (133, 59, 5, 2))
    pygame.draw.rect(surface, ORANGE, (133, 64, 5, 2))
    pygame.draw.line(surface, METAL_LIGHT, (127, 78), (127, 84), 1)
    pygame.draw.line(surface, METAL_LIGHT, (135, 78), (135, 84), 1)

    # Diagnostic cable and tool drawers.
    pygame.draw.line(surface, METAL, (127, 44), (127, 52), 1)
    pygame.draw.line(surface, METAL, (127, 52), (132, 56), 1)
    pygame.draw.rect(surface, (52, 61, 78), (157, 52, 21, 34))
    for y in (57, 66, 75):
        pygame.draw.rect(surface, METAL_LIGHT, (161, y, 13, 2))
        pygame.draw.rect(surface, (24, 31, 45), (167, y + 3, 3, 1))

    # Spare hardware shelf.
    pygame.draw.rect(surface, (43, 50, 64), (31, 107, 44, 4))
    pygame.draw.rect(surface, (12, 19, 30), (35, 100, 8, 7))
    pygame.draw.rect(surface, (12, 19, 30), (48, 101, 11, 6))
    pygame.draw.rect(surface, (12, 19, 30), (64, 99, 7, 8))



def draw_server_room(surface):
    # Dense server aisle with no dead/erased gap in the middle.
    rack_positions = (29, 51, 73, 126, 148, 170)
    for idx, rack_x in enumerate(rack_positions):
        top = 51 + (idx % 2)
        pygame.draw.rect(surface, (5, 10, 18), (rack_x, top, 18, 42))
        pygame.draw.rect(surface, METAL, (rack_x, top, 18, 42), 1)
        pygame.draw.rect(surface, (26, 37, 52), (rack_x + 3, top + 2, 12, 3))
        for row in range(5):
            y = top + 8 + row * 6
            led = GREEN if (frame_counter // 11 + row + idx) % 5 else RED
            pygame.draw.rect(surface, led, (rack_x + 3, y, 2, 2))
            pygame.draw.rect(surface, CYAN, (rack_x + 8, y, 7, 1))

    # Central cooling / backup manifold fills the old blank-looking area.
    manifold = pygame.Rect(96, 51, 25, 42)
    pygame.draw.rect(surface, (12, 19, 31), manifold)
    pygame.draw.rect(surface, METAL_LIGHT, manifold, 1)
    pygame.draw.rect(surface, (31, 42, 58), (100, 55, 17, 7))
    pygame.draw.rect(surface, CYAN, (103, 58, 11, 2))
    pygame.draw.circle(surface, (23, 32, 45), (108, 75), 9)
    pygame.draw.circle(surface, METAL_LIGHT, (108, 75), 8, 1)
    pygame.draw.line(surface, METAL_LIGHT, (108, 67), (108, 83), 1)
    pygame.draw.line(surface, METAL_LIGHT, (100, 75), (116, 75), 1)
    pygame.draw.line(surface, METAL_LIGHT, (102, 69), (114, 81), 1)
    pygame.draw.line(surface, METAL_LIGHT, (114, 69), (102, 81), 1)
    pygame.draw.rect(surface, GREEN if (frame_counter // 14) % 2 else CYAN, (103, 87, 10, 2))

    # Overhead cable trays and bundled network lines.
    pygame.draw.line(surface, BLUE, (29, 46), (190, 46), 2)
    pygame.draw.line(surface, METAL, (29, 49), (190, 49), 1)
    for x in (42, 66, 91, 134, 158, 181):
        pygame.draw.line(surface, METAL, (x, 46), (x, 51), 1)
    pygame.draw.line(surface, CYAN, (35, 45), (94, 45), 1)
    pygame.draw.line(surface, PURPLE, (121, 45), (184, 45), 1)

    # Floor vents and status strips make the aisle feel occupied and intentional.
    for vent_x in (72, 121):
        pygame.draw.rect(surface, (45, 56, 74), (vent_x, 112, 18, 5))
        for line_x in range(vent_x + 3, vent_x + 16, 4):
            pygame.draw.line(surface, METAL_LIGHT, (line_x, 113), (line_x, 116), 1)
    pygame.draw.rect(surface, BLUE, (98, 111, 21, 2))


def draw_data_center(surface):
    # Data Center uses one dominant cryogenic core plus a separate crypto vault.
    # The old blue-plus motif is removed so the room reads as infrastructure,
    # not as a medical symbol or a random icon.
    pygame.draw.line(surface, PURPLE, (29, 46), (190, 46), 2)

    # Left/center cylindrical processing core.
    core_cx = 91
    pygame.draw.ellipse(surface, (11, 18, 33), (59, 50, 64, 15))
    pygame.draw.ellipse(surface, PURPLE, (59, 50, 64, 15), 1)
    pygame.draw.rect(surface, (10, 19, 35), (61, 57, 60, 42))
    pygame.draw.line(surface, PURPLE, (61, 57), (61, 99), 1)
    pygame.draw.line(surface, PURPLE, (121, 57), (121, 99), 1)
    pygame.draw.ellipse(surface, (15, 25, 44), (61, 91, 60, 16))
    pygame.draw.ellipse(surface, PURPLE, (61, 91, 60, 16), 1)

    # Animated coolant/data bands inside the transparent core.
    for i, yy in enumerate((62, 70, 78, 86)):
        wave = int(math.sin((frame_counter + i * 15) * 0.09) * 6)
        color = CYAN if i % 2 == 0 else GREEN
        pygame.draw.rect(surface, color, (69 + wave, yy, 32 - abs(wave), 2))
    pygame.draw.circle(surface, CYAN, (core_cx, 79), 10, 1)
    pygame.draw.circle(surface, mix_color(CYAN, WHITE, 0.35), (core_cx, 79), 4)

    # Fiber bundles visibly feed the core from the rear racks.
    for feed_x in (38, 48, 132, 172):
        pygame.draw.line(surface, CYAN, (feed_x, 47), (feed_x, 54), 1)
        pygame.draw.line(surface, PURPLE, (feed_x, 54), (core_cx, 69), 1)

    # Rear infrastructure towers frame the scene without competing with the vault.
    for idx, tower_x in enumerate((37, 128, 166)):
        pygame.draw.rect(surface, (7, 13, 24), (tower_x, 54, 22, 39))
        pygame.draw.rect(surface, PURPLE, (tower_x, 54, 22, 39), 1)
        pygame.draw.rect(surface, CYAN, (tower_x + 4, 60, 14, 3))
        pygame.draw.rect(surface, GREEN, (tower_x + 4, 69, 10, 2))
        pygame.draw.rect(surface, PURPLE, (tower_x + 4, 80, 14, 2))

    # Dedicated crypto vault on the right-center, safely away from Admin Office door.
    vault = pygame.Rect(104, 68, 34, 34)
    pygame.draw.ellipse(surface, (4, 8, 15), (101, 97, 40, 8))
    pygame.draw.polygon(surface, (28, 38, 55), [(104, 68), (138, 68), (135, 101), (107, 101)])
    pygame.draw.polygon(surface, YELLOW, [(104, 68), (138, 68), (135, 101), (107, 101)], 1)
    pygame.draw.rect(surface, (8, 14, 24), (108, 72, 26, 23))
    pygame.draw.rect(surface, mix_color(YELLOW, WHITE, 0.2), (110, 74, 22, 2))
    pygame.draw.rect(surface, (27, 36, 51), (107, 95, 28, 5))
    pygame.draw.rect(surface, GREEN if "Encryption Key" in collected_items else YELLOW, (131, 97, 2, 2))

    # Cooling infrastructure and a lower pressure strip.
    pygame.draw.line(surface, METAL, (27, 106), (188, 106), 3)
    for x in (48, 76, 104, 160):
        pygame.draw.line(surface, METAL_LIGHT, (x, 103), (x, 109), 1)
    pygame.draw.rect(surface, (10, 17, 29), (78, 111, 30, 7))
    pygame.draw.rect(surface, PURPLE, (78, 111, 30, 7), 1)
    pygame.draw.rect(surface, GREEN, (82, 114, 8, 1))
    pygame.draw.rect(surface, CYAN, (94, 114, 10, 1))


def draw_admin_office(surface):
    # Executive desk, computer, phone, and chair.
    pygame.draw.rect(surface, (76, 55, 39), (47, 80, 67, 8))
    pygame.draw.rect(surface, (49, 35, 27), (53, 88, 5, 16))
    pygame.draw.rect(surface, (49, 35, 27), (102, 88, 5, 16))
    draw_status_monitor(surface, 62, 56, 28, 17, YELLOW)
    draw_keyboard(surface, 64, 77, 23)
    pygame.draw.rect(surface, (13, 20, 31), (94, 68, 12, 7))
    pygame.draw.rect(surface, METAL, (94, 68, 12, 7), 1)
    pygame.draw.line(surface, YELLOW, (97, 71), (103, 71), 1)
    pygame.draw.rect(surface, (24, 31, 44), (72, 92, 15, 10))
    pygame.draw.rect(surface, METAL, (76, 102, 7, 4))

    # Secure wall safe.
    pygame.draw.rect(surface, PANEL_INNER, (118, 53, 25, 31))
    pygame.draw.rect(surface, METAL_LIGHT, (118, 53, 25, 31), 1)
    pygame.draw.circle(surface, YELLOW, (130, 67), 5, 1)
    pygame.draw.circle(surface, GREEN if (frame_counter // 20) % 2 else CYAN, (130, 67), 2)

    # Filing cabinet and policy display.
    pygame.draw.rect(surface, (53, 62, 78), (165, 52, 19, 35))
    for y in (57, 66, 75):
        pygame.draw.rect(surface, METAL_LIGHT, (169, y, 11, 2))
        pygame.draw.rect(surface, (27, 34, 49), (174, y + 3, 3, 1))
    pygame.draw.rect(surface, (8, 14, 26), (24, 52, 20, 18))
    pygame.draw.rect(surface, YELLOW, (24, 52, 20, 18), 1)
    pygame.draw.rect(surface, CYAN, (28, 57, 12, 2))
    pygame.draw.rect(surface, GREEN, (28, 62, 8, 2))

    # Control-room authorization changes as the toolkit is completed.
    auth_color = GREEN if len(collected_items) == 6 else (YELLOW if "Access Card" in collected_items else RED)
    pygame.draw.rect(surface, (8, 14, 24), (25, 91, 20, 11))
    pygame.draw.rect(surface, auth_color, (25, 91, 20, 11), 1)
    pygame.draw.rect(surface, auth_color, (29, 95, 12, 2))


def draw_room_props(surface, room_name):
    if room_name == "Main Lobby":
        draw_main_lobby(surface)
    elif room_name == "Security Office":
        draw_security_office(surface)
    elif room_name == "Network Operations Center":
        draw_network_ops(surface)
    elif room_name == "IT Office":
        draw_it_office(surface)
    elif room_name == "Server Room":
        draw_server_room(surface)
    elif room_name == "Data Center":
        draw_data_center(surface)
    elif room_name == "Admin Office":
        draw_admin_office(surface)


def draw_current_room(surface):
    accent = ROOM_ACCENTS.get(current_room, CYAN)
    draw_room_shell(surface, accent)
    draw_room_props(surface, current_room)

    room = rooms[current_room]

    for direction in ("north", "south", "west", "east"):
        if direction in room:
            progress = door_progress.get((current_room, direction), 0.0)
            draw_sliding_door(surface, direction, progress, room[direction])

    room_item = room.get("item")
    if room_item and room_item not in collected_items:
        x, y = item_position(current_room)
        draw_item_display(surface, room_item, x, y)

def draw_title_screen(surface, show_prompt):
    surface.fill(BACKGROUND)

    pygame.draw.rect(surface, CYAN, (7, 7, 306, 166), 2)
    pygame.draw.rect(surface, DARK_BLUE, (12, 12, 296, 156), 2)

    # Decorative cyber grid.
    for x in range(28, 294, 22):
        pygame.draw.rect(surface, (18, 32, 49), (x, 29, 1, 12))
    pygame.draw.rect(surface, PINK, (22, 31, 52, 2))
    pygame.draw.rect(surface, PINK, (246, 31, 52, 2))

    draw_pixel_lock(surface, 151, 21, YELLOW)

    title = pixel_title_font.render("CYBERSECURITY", False, CYAN)
    # Render ATTACK in two pieces so the middle T/T pair always has a clean
    # pixel gap. This preserves the approved font/size without changing the word.
    attack_left = pixel_title_font.render("AT", False, PINK)
    attack_right = pixel_title_font.render("TACK", False, PINK)
    attack_gap = 2
    attack_width = attack_left.get_width() + attack_gap + attack_right.get_width()
    attack_x = BASE_WIDTH // 2 - attack_width // 2
    subtitle = pixel_subtitle_font.render("TEXT ADVENTURE", False, WHITE)

    surface.blit(title, (BASE_WIDTH // 2 - title.get_width() // 2, 57))
    surface.blit(attack_left, (attack_x, 87))
    surface.blit(attack_right, (attack_x + attack_left.get_width() + attack_gap, 87))
    surface.blit(subtitle, (BASE_WIDTH // 2 - subtitle.get_width() // 2, 119))

def draw_bridge_screen(surface, rect, color, locked=False, secure=False, index=0):
    pygame.draw.rect(surface, (4, 8, 16), rect)
    pygame.draw.rect(surface, color, rect, 1)

    if locked:
        lock_x = rect.centerx - 4
        lock_y = rect.centery - 6
        draw_pixel_lock(surface, lock_x, lock_y, RED, 1)
    elif secure:
        pygame.draw.rect(surface, GREEN, (rect.x + 4, rect.y + 5, rect.w - 8, 2))
        pygame.draw.rect(surface, CYAN, (rect.x + 4, rect.y + 11, rect.w - 13, 2))
        pygame.draw.rect(surface, GREEN, (rect.x + 4, rect.y + 17, rect.w - 6, 1))
    else:
        signal = RED if (frame_counter // 9 + index) % 4 == 0 else CYAN
        pygame.draw.rect(surface, signal, (rect.x + 4, rect.y + 5, rect.w - 10, 2))
        pygame.draw.rect(surface, RED, (rect.x + 4, rect.y + 11, rect.w - 16, 2))
        pygame.draw.rect(surface, CYAN, (rect.x + 4, rect.y + 17, rect.w - 7, 1))



def draw_control_room_bridge(surface, mode="danger", intensity=0.0, stage=0):
    """Final-boss command bridge with layered depth and persistent animation."""
    surface.fill(BACKGROUND)

    secure = mode == "secure"
    defeat = mode == "defeat"
    border = GREEN if secure else RED
    accent = CYAN if secure else RED

    # Outer shell and deep inset chamber.
    pygame.draw.rect(surface, border, (7, 7, 306, 166), 2)
    pygame.draw.rect(surface, DARK_BLUE, (13, 13, 294, 154), 2)
    pygame.draw.rect(surface, (5, 10, 18), (18, 20, 284, 139))

    # Ceiling canopy / ribs create a cockpit rather than a flat wall.
    pygame.draw.polygon(surface, (18, 29, 44), [(25, 24), (295, 24), (284, 34), (36, 34)])
    pygame.draw.polygon(surface, border, [(25, 24), (295, 24), (284, 34), (36, 34)], 1)
    for x in (45, 82, 119, 156, 193, 230, 267):
        light = GREEN if secure else (RED if (frame_counter // 10 + x) % 3 else (79, 31, 42))
        pygame.draw.rect(surface, light, (x, 20, 18, 2))
        pygame.draw.line(surface, (37, 49, 66), (x + 9, 24), (x + 9, 31), 1)

    # Angled panoramic wall with a dominant central command screen.
    pygame.draw.polygon(surface, (13, 22, 35), [(31, 36), (289, 36), (278, 73), (42, 73)])
    pygame.draw.polygon(surface, border, [(31, 36), (289, 36), (278, 73), (42, 73)], 1)

    left_screen = pygame.Rect(40, 42, 51, 23)
    center_screen = pygame.Rect(104, 34, 112, 33)
    right_screen = pygame.Rect(229, 42, 51, 23)

    # Side screens always animate; center is kept visually quiet for crisp native text.
    draw_bridge_screen(surface, left_screen, border, defeat and intensity > 0.56, secure, 0)
    draw_bridge_screen(surface, right_screen, border, defeat and intensity > 0.56, secure, 2)
    pygame.draw.rect(surface, (3, 8, 15), center_screen)
    pygame.draw.rect(surface, border, center_screen, 1)
    pygame.draw.line(surface, accent, (center_screen.x + 5, center_screen.y + 6),
                     (center_screen.right - 5, center_screen.y + 6), 1)
    pygame.draw.line(surface, mix_color(accent, WHITE, 0.15),
                     (center_screen.x + 5, center_screen.bottom - 5),
                     (center_screen.right - 5, center_screen.bottom - 5), 1)

    # Living data traces behind the future title text.
    trace_color = GREEN if secure else (CYAN if not defeat else RED)
    trace_y = center_screen.y + 20
    points = []
    for idx in range(8):
        px = center_screen.x + 7 + idx * 14
        offset = int(math.sin((frame_counter + idx * 7) / 8.0) * (2 if secure else 3))
        py = trace_y + offset
        points.append((px, py))
    for a, b in zip(points[:-1], points[1:]):
        pygame.draw.line(surface, trace_color, a, b, 1)
    for px, py in points[::2]:
        pygame.draw.rect(surface, trace_color, (px - 1, py - 1, 2, 2))

    # Structural columns and wall accents.
    for x in (33, 94, 222, 283):
        pygame.draw.rect(surface, (27, 39, 56), (x, 38, 3, 36))
        pygame.draw.line(surface, METAL, (x, 39), (x, 72), 1)

    # Curved command desk: top, front face, and lower shadow.
    pygame.draw.polygon(surface, (45, 57, 76), [(48, 80), (272, 80), (250, 108), (70, 108)])
    pygame.draw.polygon(surface, (25, 35, 51), [(53, 84), (267, 84), (246, 103), (74, 103)])
    pygame.draw.polygon(surface, border, [(48, 80), (272, 80), (250, 108), (70, 108)], 1)
    pygame.draw.polygon(surface, (8, 14, 24), [(70, 108), (250, 108), (239, 115), (81, 115)])

    # Six integrated response modules. They read as hardware in the room, not floating cards.
    bay_positions = [(72, 91), (102, 87), (130, 85), (178, 85), (206, 87), (236, 91)]
    for index, (x, y) in enumerate(bay_positions):
        if secure:
            bay_color = ITEM_DATA[list(ITEM_DATA.keys())[index]]["color"]
        elif defeat and intensity > 0.30 + index * 0.06:
            bay_color = RED
        else:
            bay_color = CYAN if (frame_counter // 15 + index) % 4 else RED
        pts = [(x, y), (x + 14, y), (x + 12, y + 8), (x + 2, y + 8)]
        pygame.draw.polygon(surface, (5, 11, 19), pts)
        pygame.draw.polygon(surface, METAL, pts, 1)
        pygame.draw.rect(surface, bay_color, (x + 4, y + 2, 6, 2))
        pygame.draw.rect(surface, bay_color, (x + 9, y + 5, 2, 1))

    # Operator wing consoles, angled toward the center.
    for side in (-1, 1):
        if side < 0:
            pts = [(23, 78), (53, 84), (48, 111), (20, 105)]
            sx = 29
        else:
            pts = [(297, 78), (267, 84), (272, 111), (300, 105)]
            sx = 276
        pygame.draw.polygon(surface, (24, 35, 51), pts)
        pygame.draw.polygon(surface, METAL, pts, 1)
        pygame.draw.rect(surface, border, (sx, 88, 11, 2))
        pygame.draw.rect(surface, GREEN if secure else CYAN, (sx, 94, 14, 1))
        pygame.draw.rect(surface, GRAY, (sx, 100, 8, 1))
        # Chair/seat depth.
        seat_x = 18 if side < 0 else 287
        pygame.draw.polygon(surface, (38, 49, 66), [(seat_x, 107), (seat_x + 15, 107), (seat_x + 13, 120), (seat_x + 2, 120)])
        pygame.draw.polygon(surface, METAL, [(seat_x, 107), (seat_x + 15, 107), (seat_x + 13, 120), (seat_x + 2, 120)], 1)

    # Raised malware dais in front of the command deck.
    pygame.draw.polygon(surface, (15, 22, 35), [(137, 103), (183, 103), (190, 121), (130, 121)])
    pygame.draw.polygon(surface, border, [(137, 103), (183, 103), (190, 121), (130, 121)], 1)
    pygame.draw.rect(surface, (7, 12, 21), (143, 108, 34, 10))

    # Floor perspective + luminous runway leading from the entry hatch.
    pygame.draw.polygon(surface, (7, 12, 21), [(18, 116), (302, 116), (297, 158), (23, 158)])
    vanish = (160, 114)
    for x in (47, 82, 116, 144, 176, 204, 238, 273):
        pygame.draw.line(surface, (34, 47, 66), vanish, (x, 157), 1)
    for y in (126, 138, 149):
        inset = (y - 116) // 2
        pygame.draw.line(surface, (34, 47, 66), (24 + inset, y), (296 - inset, y), 1)

    # Entry hatch remains visible so the character feels physically present in the room.
    pygame.draw.polygon(surface, (12, 20, 31), [(142, 124), (178, 124), (188, 151), (132, 151)])
    hatch_color = GREEN if secure else (RED if defeat else CYAN)
    pygame.draw.polygon(surface, hatch_color, [(142, 124), (178, 124), (188, 151), (132, 151)], 1)

    # Animated floor guidance lights / restoration runway.
    for idx, y in enumerate((130, 137, 144, 151)):
        active = (frame_counter // 6 + idx) % 4
        c = GREEN if secure else (RED if defeat else CYAN)
        strength = 1.0 if active == 0 else 0.28
        light = mix_color((21, 29, 42), c, strength)
        pygame.draw.rect(surface, light, (157, y, 6, 1))

    if defeat:
        # Corruption scan and electrical faults keep the failure state moving.
        scan_y = 38 + int((frame_counter * 1.1) % 75)
        pygame.draw.line(surface, mix_color((70, 18, 30), RED, 0.7), (32, scan_y), (288, scan_y), 1)
        spark_count = int(4 + intensity * 12)
        for index in range(spark_count):
            gx = 35 + ((index * 41 + frame_counter * 2) % 245)
            gy = 48 + ((index * 17 + frame_counter) % 64)
            pygame.draw.rect(surface, RED if index % 2 else ORANGE, (gx, gy, 2 + index % 3, 1))
        if intensity > 0.60:
            for x in range(67, 250, 23):
                pygame.draw.line(surface, (125, 27, 42), (x, 103), (x + 8, 111), 1)
                pygame.draw.line(surface, (125, 27, 42), (x + 8, 111), (x + 17, 104), 1)

    if secure:
        # Healthy data packets continue flowing after victory so the final frame is alive.
        for index in range(11):
            px = 54 + ((index * 29 + frame_counter) % 214)
            py = 73 + ((index * 11 + frame_counter // 2) % 39)
            pygame.draw.rect(surface, GREEN if index % 2 else CYAN, (px, py, 1, 1))


def draw_ransomware_bot(surface, cx, cy, power=1.0, damage=0.0, defeated=False, cable_progress=1.0):
    """A corrupted security AI: visor face, lock-core chassis, cable tendrils, and a unique silhouette."""
    body_red = mix_color((112, 22, 37), RED, clamp(power, 0, 1))
    dark_red = (78, 17, 31)
    glow = RED if not defeated else (121, 57, 64)
    hover = int(math.sin(frame_counter / 8.0) * 2)
    cy += hover

    # Malware aura / shadow.
    pygame.draw.ellipse(surface, (44, 10, 22), (cx - 30, cy + 24, 60, 8), 1)
    pygame.draw.circle(surface, dark_red, (cx, cy - 1), 29, 1)

    # Six invasive data cables visibly plug into the command deck.
    cable_targets = [(79, 98), (108, 94), (136, 93), (184, 93), (212, 94), (241, 98)]
    cable_starts = [(cx - 15, cy + 13), (cx - 9, cy + 17), (cx - 3, cy + 18),
                    (cx + 3, cy + 18), (cx + 9, cy + 17), (cx + 15, cy + 13)]
    for start, target in zip(cable_starts, cable_targets):
        end = (int(lerp(start[0], target[0], cable_progress)),
               int(lerp(start[1], target[1], cable_progress)))
        pygame.draw.line(surface, dark_red, start, end, 2)
        pygame.draw.line(surface, (140, 28, 49), start, end, 1)
        if cable_progress > 0.35:
            pulse_step = ((frame_counter + target[0]) % 20) / 20.0
            pulse_x = int(lerp(start[0], end[0], pulse_step))
            pulse_y = int(lerp(start[1], end[1], pulse_step))
            pygame.draw.rect(surface, RED, (pulse_x, pulse_y, 2, 1))

    # Broad angular shoulders make the silhouette identifiable at a glance.
    pygame.draw.polygon(surface, body_red, [
        (cx - 28, cy - 4), (cx - 18, cy - 14), (cx - 13, cy - 9),
        (cx + 13, cy - 9), (cx + 18, cy - 14), (cx + 28, cy - 4),
        (cx + 21, cy + 6), (cx + 14, cy + 2), (cx + 13, cy + 18),
        (cx - 13, cy + 18), (cx - 14, cy + 2), (cx - 21, cy + 6)
    ])
    pygame.draw.polygon(surface, (14, 17, 28), [
        (cx - 16, cy - 8), (cx + 16, cy - 8), (cx + 13, cy + 19), (cx - 13, cy + 19)
    ])
    pygame.draw.polygon(surface, body_red, [
        (cx - 16, cy - 8), (cx + 16, cy - 8), (cx + 13, cy + 19), (cx - 13, cy + 19)
    ], 2)

    # Cable claws / malware tendrils.
    for side in (-1, 1):
        root_x = cx + side * 25
        claw_x = cx + side * 35
        pygame.draw.line(surface, body_red, (root_x, cy), (claw_x, cy + 7), 2)
        pygame.draw.line(surface, body_red, (claw_x, cy + 7), (claw_x + side * 5, cy + 2), 1)
        pygame.draw.line(surface, body_red, (claw_x, cy + 7), (claw_x + side * 4, cy + 12), 1)

    # Hooded visor head, distinct from the lock body.
    pygame.draw.polygon(surface, dark_red, [
        (cx - 16, cy - 31), (cx + 16, cy - 31), (cx + 20, cy - 24),
        (cx + 15, cy - 13), (cx - 15, cy - 13), (cx - 20, cy - 24)
    ])
    pygame.draw.polygon(surface, body_red, [
        (cx - 16, cy - 31), (cx + 16, cy - 31), (cx + 20, cy - 24),
        (cx + 15, cy - 13), (cx - 15, cy - 13), (cx - 20, cy - 24)
    ], 2)
    pygame.draw.rect(surface, (6, 10, 18), (cx - 13, cy - 27, 26, 9))

    eye_color = (86, 43, 50) if defeated else glow
    if defeated:
        pygame.draw.line(surface, eye_color, (cx - 9, cy - 23), (cx - 4, cy - 20), 1)
        pygame.draw.line(surface, eye_color, (cx + 9, cy - 23), (cx + 4, cy - 20), 1)
    else:
        pygame.draw.polygon(surface, eye_color, [(cx - 10, cy - 24), (cx - 3, cy - 23), (cx - 6, cy - 20)])
        pygame.draw.polygon(surface, eye_color, [(cx + 10, cy - 24), (cx + 3, cy - 23), (cx + 6, cy - 20)])
        pygame.draw.rect(surface, RED, (cx - 2, cy - 18, 4, 1))

    # Lock core is the unmistakable ransomware symbol.
    lock_color = YELLOW if not defeated else (111, 93, 59)
    pygame.draw.rect(surface, (6, 10, 18), (cx - 10, cy - 2, 20, 17))
    pygame.draw.rect(surface, body_red, (cx - 10, cy - 2, 20, 17), 1)
    pygame.draw.rect(surface, lock_color, (cx - 7, cy + 4, 14, 9))
    pygame.draw.rect(surface, (13, 15, 23), (cx - 3, cy + 7, 6, 4))
    pygame.draw.rect(surface, lock_color, (cx - 4, cy, 8, 3))
    pygame.draw.rect(surface, lock_color, (cx - 6, cy + 2, 3, 5))
    pygame.draw.rect(surface, lock_color, (cx + 3, cy + 2, 3, 5))
    pygame.draw.rect(surface, RED if not defeated else BLACK, (cx - 1, cy + 8, 3, 3))

    if damage > 0:
        crack_color = WHITE if damage > 0.45 else ORANGE
        pygame.draw.line(surface, crack_color, (cx, cy - 9), (cx - 4, cy + 1), 1)
        pygame.draw.line(surface, crack_color, (cx - 4, cy + 1), (cx + 2, cy + 9), 1)
        if damage > 0.65:
            pygame.draw.line(surface, crack_color, (cx + 7, cy - 13), (cx + 1, cy - 5), 1)
            pygame.draw.line(surface, crack_color, (cx - 10, cy + 14), (cx - 2, cy + 10), 1)

    # Controlled glitch fragments; enough to read as malware without obscuring the silhouette.
    glitch_count = int(3 + 8 * damage + 2 * power)
    for index in range(glitch_count):
        gx = cx - 36 + ((index * 19 + result_timer * 3) % 72)
        gy = cy - 31 + ((index * 13 + result_timer * 2) % 58)
        if index % 2 == 0 or damage > 0.55:
            pygame.draw.rect(surface, glow, (gx, gy, 2 + index % 3, 1))

def draw_tool_console_lights(surface, activated_count):
    item_order = list(ITEM_DATA.keys())
    positions = [(72, 91), (102, 87), (130, 86), (178, 86), (206, 87), (236, 91)]

    for index, item_name in enumerate(item_order):
        color = ITEM_DATA[item_name]["color"]
        active = index < activated_count
        edge = color if active else GRAY_DARK
        x, y = positions[index]

        pts = [(x, y), (x + 14, y), (x + 12, y + 7), (x + 2, y + 7)]
        pygame.draw.polygon(surface, (6, 12, 21), pts)
        pygame.draw.polygon(surface, edge, pts, 1)
        if active:
            pygame.draw.rect(surface, color, (x + 4, y + 2, 6, 2))
            pygame.draw.rect(surface, GREEN, (x + 10, y + 2, 1, 1))

def draw_victory_scene(surface):
    """Staged final encounter: enter -> deploy tools -> purge -> restore -> celebrate."""
    t = result_timer
    secure = t >= 260
    draw_control_room_bridge(surface, "secure" if secure else "danger", 0.0, t)

    # The analyst physically enters from the lower hatch instead of teleporting to center.
    if t < 48:
        enter_progress = t / 48.0
        py = int(lerp(137, 116, enter_progress))
        walk = (t // 7) % 2
        draw_player(surface, 149, py, "up", walk, True)
    elif t < 300:
        draw_player(surface, 149, 116, "up", 0, False)
    else:
        draw_player(surface, 149, 116, "down", (t // 7) % 2, True, celebrate=True)

    # Security modules deploy one by one; the player sees the toolkit matter.
    activated = min(6, max(0, (t - 52) // 12 + 1)) if t >= 52 else 0
    draw_tool_console_lights(surface, activated)

    if t < 70:
        draw_ransomware_bot(surface, 160, 78, power=0.72, damage=0.0, cable_progress=0.82)

    elif t < 125:
        power = 0.75 + 0.25 * ((t - 70) / 55.0)
        draw_ransomware_bot(surface, 160, 78, power=power, damage=0.0, cable_progress=1.0)

    elif t < 195:
        damage = clamp((t - 125) / 70.0, 0.0, 1.0)
        shake = int(math.sin(t * 0.75) * (1 + damage * 2))
        draw_ransomware_bot(surface, 160 + shake, 78, power=1.0, damage=damage, cable_progress=1.0)

        # Countermeasure streams come from the six built-in console modules.
        positions = [(79, 95), (109, 91), (137, 90), (183, 90), (211, 91), (241, 95)]
        item_order = list(ITEM_DATA.keys())
        for index in range(activated):
            start = positions[index]
            beam_color = ITEM_DATA[item_order[index]]["color"]
            progress = ((frame_counter + index * 7) % 18) / 18.0
            mid = (int(lerp(start[0], 160, progress)), int(lerp(start[1], 82, progress)))
            pygame.draw.line(surface, mix_color(beam_color, WHITE, 0.18), start, (160, 82), 1)
            pygame.draw.rect(surface, WHITE, (mid[0], mid[1], 2, 1))

    elif t < 240:
        collapse = clamp((t - 195) / 45.0, 0.0, 1.0)
        if collapse < 0.58:
            draw_ransomware_bot(surface, 160, 78, power=0.45, damage=1.0, defeated=True, cable_progress=1.0 - collapse)
        for index in range(34):
            angle = (index / 34.0) * math.tau + t * 0.03
            radius = 4 + collapse * (12 + (index % 7) * 4)
            px = int(160 + math.cos(angle) * radius)
            py = int(78 + math.sin(angle) * radius * 0.58)
            fragment_color = RED if index % 4 else YELLOW
            pygame.draw.rect(surface, fragment_color, (px, py, 1 + index % 2, 1 + (index + 1) % 2))

    elif t < 300:
        # A restoration wave visibly clears the room from top to bottom.
        restore = clamp((t - 240) / 60.0, 0.0, 1.0)
        wave_y = int(36 + restore * 100)
        pygame.draw.line(surface, GREEN, (25, wave_y), (295, wave_y), 2)
        for index in range(14):
            px = 36 + ((index * 23 + frame_counter) % 246)
            py = wave_y - 3 - (index % 4)
            pygame.draw.rect(surface, CYAN if index % 2 else GREEN, (px, py, 1, 1))

    else:
        draw_tool_console_lights(surface, 6)
        # Network particles continue moving so the final state never becomes a dead poster.
        for index in range(16):
            px = 50 + ((index * 31 + frame_counter) % 220)
            py = 78 + ((index * 9 + frame_counter // 2) % 38)
            pygame.draw.rect(surface, GREEN if index % 2 else CYAN, (px, py, 1, 1))


def draw_defeat_scene(surface):
    """Staged takeover: enter -> bot wakes -> systems encrypt -> analyst collapses."""
    t = result_timer
    intensity = clamp((t - 38) / 130.0, 0.0, 1.0)
    draw_control_room_bridge(surface, "defeat", intensity, t)

    # Player walks in first; the failure happens in front of them.
    if t < 45:
        enter_progress = t / 45.0
        py = int(lerp(137, 117, enter_progress))
        draw_player(surface, 149, py, "up", (t // 7) % 2, True)
    elif t < 128:
        draw_player(surface, 149, 116, "up", 0, False)
    elif t < 166:
        stagger = int(lerp(116, 124, (t - 128) / 38.0))
        draw_player(surface, 149, stagger, "down", 0, False)
    else:
        draw_player(surface, 149, 127, "down", 0, False, defeated=True)

    if t < 42:
        draw_ransomware_bot(surface, 160, 80, power=0.45, damage=0.0, cable_progress=0.0)
    elif t < 108:
        wake = clamp((t - 42) / 66.0, 0.0, 1.0)
        bot_y = int(lerp(82, 75, wake))
        draw_ransomware_bot(surface, 160, bot_y, power=0.5 + wake * 0.5,
                            damage=0.0, cable_progress=wake)
    else:
        rage = 0.92 + 0.08 * ((math.sin(frame_counter / 7.0) + 1.0) / 2.0)
        draw_ransomware_bot(surface, 160, 75, power=rage, damage=0.0, cable_progress=1.0)

    # Modules fail sequentially as encryption spreads across the command deck.
    if t > 82:
        failed = min(6, 1 + (t - 82) // 13)
        positions = [(72, 91), (102, 87), (130, 85), (178, 85), (206, 87), (236, 91)]
        for index, (x, y) in enumerate(positions):
            edge = RED if index < failed else GRAY_DARK
            pts = [(x, y), (x + 14, y), (x + 12, y + 8), (x + 2, y + 8)]
            pygame.draw.polygon(surface, (5, 11, 19), pts)
            pygame.draw.polygon(surface, edge, pts, 1)
            if index < failed:
                pygame.draw.rect(surface, RED, (x + 4, y + 2, 6, 2))
                if (frame_counter + index) % 12 < 5:
                    pygame.draw.rect(surface, ORANGE, (x + 9, y + 5, 2, 1))

    # Encryption sweep makes the room visibly succumb instead of simply changing text.
    if 105 <= t < 175:
        sweep = (t - 105) / 70.0
        scan_y = int(41 + sweep * 105)
        pygame.draw.line(surface, RED, (26, scan_y), (294, scan_y), 2)
        pygame.draw.line(surface, (126, 27, 42), (31, scan_y + 3), (289, scan_y + 3), 1)


def draw_game_panels(surface):
    surface.fill(BACKGROUND)

    pygame.draw.rect(surface, DARK_BLUE, HEADER_RECT)
    pygame.draw.rect(surface, CYAN, (5, 5, 310, 171), 2)

    pygame.draw.rect(surface, PANEL_BLUE, MISSION_RECT)
    pygame.draw.rect(surface, CYAN, MISSION_RECT, 1)
    pygame.draw.rect(surface, PANEL_INNER,
                     (MISSION_RECT.x + 3, MISSION_RECT.y + 3, MISSION_RECT.w - 6, MISSION_RECT.h - 6))

    pygame.draw.rect(surface, PANEL_BLUE, INVENTORY_RECT)
    pygame.draw.rect(surface, CYAN, INVENTORY_RECT, 1)
    pygame.draw.line(surface, CYAN, (68, 144), (68, 172), 1)



def draw_inventory_slots(surface):
    item_order = list(ITEM_DATA.keys())
    start_x = 71
    slot_w = 39

    for index, item_name in enumerate(item_order):
        x = start_x + index * slot_w
        collected = item_name in collected_items
        color = ITEM_DATA[item_name]["color"] if collected else GRAY_DARK

        # Hardware-card styling: bevel, inset face, compact icon area, clean text area.
        pygame.draw.rect(surface, (3, 7, 13), (x + 1, 146, 35, 27))
        pygame.draw.rect(surface, (7, 13, 23), (x, 145, 35, 27))
        pygame.draw.rect(surface, color, (x, 145, 35, 27), 1)
        pygame.draw.line(surface, mix_color(color, WHITE, 0.22), (x + 2, 147), (x + 32, 147), 1)

        if collected:
            pygame.draw.rect(surface, mix_color((9, 15, 25), color, 0.12), (x + 3, 149, 29, 11))
            draw_inventory_glyph(surface, item_name, x + 12, 149, color)
            pygame.draw.rect(surface, GREEN, (x + 30, 148, 2, 2))
        else:
            pygame.draw.rect(surface, GRAY_DARK, (x + 14, 151, 7, 7), 1)
            pygame.draw.rect(surface, GRAY_DARK, (x + 16, 148, 3, 4), 1)


def draw_game_screen(surface):
    draw_game_panels(surface)
    draw_current_room(surface)
    draw_inventory_slots(surface)

# --------------------------------------------------
# HIGH-RESOLUTION GAMEPLAY TEXT
# --------------------------------------------------


def draw_room_header_text(surface):
    max_width = 620
    font = fit_hud_text(current_room.upper(), max_width, start_size=37, min_size=23, bold=True)
    title = font.render(current_room.upper(), True, CYAN)
    surface.blit(title, (34, 36))


def draw_status_chip(surface):
    chip_rect = pygame.Rect(766, 39, 166, 35)
    pygame.draw.rect(surface, (49, 17, 27), chip_rect)
    pygame.draw.rect(surface, RED, chip_rect, 1)

    pulse_color = RED if (frame_counter // 20) % 2 == 0 else (130, 48, 57)
    pygame.draw.circle(surface, pulse_color, (782, 56), 4)
    text = hud_status_font.render("COMPROMISED", True, RED)
    surface.blit(text, (795, 46))


def draw_mission_panel_text(surface):
    panel_x = 638
    panel_y = 108
    max_width = 278

    heading = hud_heading_font.render("MISSION STATUS", True, YELLOW)
    surface.blit(heading, (panel_x, panel_y))

    room = rooms[current_room]
    y = panel_y + 57

    for sentence in room.get("description", []):
        font = fit_hud_text(sentence, max_width, start_size=15, min_size=11)
        for line in wrap_text(sentence, font, max_width):
            rendered = font.render(line, True, WHITE)
            surface.blit(rendered, (panel_x, y))
            y += 22
        y += 3

    item = room.get("item")
    if current_room == "Main Lobby":
        objective = f"Recover all 6 tools ({len(inventory)}/6 secured)."
    elif item and item not in collected_items:
        objective = "Objective: recover the " + item + "."
    elif item:
        objective = "Tool recovered. Continue the response."
    else:
        objective = "Proceed only when all tools are secured."

    objective_font = fit_hud_text(objective, max_width, start_size=14, min_size=10, bold=True)
    objective_lines = wrap_text(objective, objective_font, max_width)
    for line in objective_lines:
        surface.blit(objective_font.render(line, True, CYAN), (panel_x, y))
        y += 20

    y += 9
    exits_heading = hud_heading_font.render("EXITS", True, GREEN)
    surface.blit(exits_heading, (panel_x, y))
    y += 42

    for direction in ("north", "south", "west", "east"):
        if direction not in room:
            continue
        destination = room[direction]
        prefix = direction.upper() + "  >  "
        whole = prefix + destination
        font = fit_hud_text(whole, max_width, start_size=14, min_size=10, bold=True)
        prefix_surface = font.render(prefix, True, ROOM_ACCENTS.get(current_room, CYAN))
        destination_surface = font.render(destination, True, WHITE)
        surface.blit(prefix_surface, (panel_x, y))
        surface.blit(destination_surface, (panel_x + prefix_surface.get_width(), y))
        y += 25


def draw_interaction_prompt(surface):
    interaction_type, value = nearest_interaction()

    if interaction_type == "item":
        prompt_text = "E  -  RECOVER " + value.upper()
        prompt_color = ITEM_DATA[value]["color"]
    elif interaction_type == "door":
        destination = rooms[current_room][value]
        prompt_text = "E  -  ENTER " + destination.upper()
        prompt_color = RED if destination == "Control Room" else GREEN
    else:
        prompt_text = "ARROW KEYS / WASD TO MOVE      E TO INTERACT"
        prompt_color = GRAY

    font = fit_hud_text(prompt_text, 540, start_size=14, min_size=11, bold=True)
    prompt = font.render(prompt_text, True, prompt_color)
    x = 316 - prompt.get_width() // 2
    pygame.draw.rect(surface, (5, 9, 16), (x - 9, 398, prompt.get_width() + 18, 23))
    surface.blit(prompt, (x, 402))

    if interaction_message and message_timer > 0:
        message_font = fit_hud_text(interaction_message, 510, start_size=14, min_size=10, bold=True)
        message = message_font.render(interaction_message, True, CYAN)
        mx = 316 - message.get_width() // 2
        pygame.draw.rect(surface, (8, 15, 26), (mx - 10, 365, message.get_width() + 20, 24))
        pygame.draw.rect(surface, CYAN, (mx - 10, 365, message.get_width() + 20, 24), 1)
        surface.blit(message, (mx, 369))



def draw_inventory_text(surface):
    title = hud_small_font.render("SECURITY", True, YELLOW)
    title2 = hud_small_font.render("TOOLKIT", True, YELLOW)
    progress_color = GREEN if len(inventory) == 6 else GRAY
    progress = hud_tiny_font.render(f"{len(inventory)} / 6 RECOVERED", True, progress_color)

    surface.blit(title, (31, 438))
    surface.blit(title2, (31, 456))
    surface.blit(progress, (31, 487))

    item_names = list(ITEM_DATA.keys())
    for idx in range(6):
        seg_color = ITEM_DATA[item_names[idx]]["color"] if item_names[idx] in collected_items else GRAY_DARK
        pygame.draw.rect(surface, seg_color, (31 + idx * 22, 507, 17, 3))

    start_x = 213
    slot_w = 117
    display_names = {
        "MFA Token": "MFA TOKEN",
        "Firewall Key": "FIREWALL KEY",
        "Security Patch": "SECURITY PATCH",
        "Backup Drive": "BACKUP DRIVE",
        "Encryption Key": "ENCRYPTION KEY",
        "Access Card": "ACCESS CARD",
    }

    for index, item_name in enumerate(item_names):
        collected = item_name in collected_items
        color = ITEM_DATA[item_name]["color"] if collected else GRAY_DARK
        center_x = start_x + index * slot_w + 52

        label_font = fit_hud_text(display_names[item_name], 102, start_size=9, min_size=8, bold=True)
        label = label_font.render(display_names[item_name], True, color)
        surface.blit(label, (center_x - label.get_width() // 2, 482))

        status = "RECOVERED" if collected else "LOCKED"
        status_font = pygame.font.SysFont("consolas", 8, bold=True)
        status_surface = status_font.render(status, True, color if collected else GRAY_DARK)
        surface.blit(status_surface, (center_x - status_surface.get_width() // 2, 504))

def door_sign_screen_rect(direction, destination):
    """Return a native-resolution plaque above the actual door frame."""
    rect = direction_door_rect(direction)
    label = destination.upper()
    arrow = {"north": "↑", "south": "↓", "west": "←", "east": "→"}[direction]
    full = f"{arrow}  {label}" if direction in ("north", "west") else f"{label}  {arrow}"

    font = hud_door_font
    max_w = 205
    if font.size(full)[0] > max_w:
        font = hud_door_small_font
    text_w = min(max_w, font.size(full)[0])
    width = text_w + 20
    height = 24

    center_x = rect.centerx * SCALE
    x = center_x - width // 2
    y = rect.y * SCALE - 28

    room_left = ROOM_RECT.x * SCALE + 6
    room_right = ROOM_RECT.right * SCALE - 6
    x = int(clamp(x, room_left, room_right - width))
    y = max(100, y)
    return pygame.Rect(x, y, width, height), font, full


def draw_world_door_labels(surface):
    """Crisp architectural plaques rendered behind the separate player layer."""
    room = rooms[current_room]
    for direction in ("north", "south", "west", "east"):
        if direction not in room:
            continue
        destination = room[direction]
        accent = RED if destination == "Control Room" and len(collected_items) < 6 else ROOM_ACCENTS.get(current_room, CYAN)
        if destination == "Control Room" and len(collected_items) == 6:
            accent = GREEN

        plaque, font, full = door_sign_screen_rect(direction, destination)
        shadow = plaque.move(3, 3)
        pygame.draw.rect(surface, (4, 7, 13), shadow)
        pygame.draw.rect(surface, (11, 18, 30), plaque)
        pygame.draw.rect(surface, accent, plaque, 1)
        pygame.draw.line(surface, mix_color(accent, WHITE, 0.25),
                         (plaque.x + 4, plaque.y + 3), (plaque.right - 4, plaque.y + 3), 1)
        label = font.render(full, True, WHITE)
        surface.blit(label, (plaque.centerx - label.get_width() // 2,
                             plaque.centery - label.get_height() // 2 + 1))


def draw_character_screen_layer(surface):
    character_canvas.fill((0, 0, 0, 0))
    draw_player(character_canvas, player_x, player_y, player_direction, walk_frame, is_walking)
    scaled_character = pygame.transform.scale(character_canvas, (WINDOW_WIDTH, WINDOW_HEIGHT))
    surface.blit(scaled_character, (0, 0))


def draw_title_hud(surface, show_prompt):
    if not show_prompt:
        return
    prompt = hud_prompt_large_font.render("PRESS ENTER TO START", True, GREEN)
    # Crisp prompt is intentionally separate from the pixel-art title layer.
    box = pygame.Rect(WINDOW_WIDTH // 2 - prompt.get_width() // 2 - 18, 441,
                      prompt.get_width() + 36, 38)
    pygame.draw.rect(surface, (5, 10, 18), box)
    pygame.draw.rect(surface, GREEN, box, 1)
    surface.blit(prompt, (WINDOW_WIDTH // 2 - prompt.get_width() // 2, 448))


def draw_game_hud(surface):
    draw_room_header_text(surface)
    draw_status_chip(surface)
    draw_mission_panel_text(surface)
    draw_interaction_prompt(surface)
    draw_inventory_text(surface)

# --------------------------------------------------
# HIGH-RESOLUTION RESULT TEXT
# --------------------------------------------------



def draw_result_hud(surface):
    """Native-resolution cinematic copy anchored to the command bridge display."""
    # Matches the low-res center screen at (104, 34, 112, 33).
    screen_rect = pygame.Rect(312, 102, 336, 99)
    center_x = screen_rect.centerx

    if game_state == "victory":
        if result_timer < 48:
            label = "FINAL RESPONSE"
            sub = "6 SECURITY TOOLS READY"
            color = CYAN
        elif result_timer < 125:
            label = "SECURITY MODULES ONLINE"
            sub = "DEPLOYING COUNTERMEASURES"
            color = CYAN
        elif result_timer < 195:
            label = "PURGING RANSOMWARE"
            sub = "MALWARE CORE DESTABILIZING"
            color = ORANGE
        elif result_timer < 240:
            label = "CORE COLLAPSING"
            sub = "THREAT PROCESS TERMINATING"
            color = RED
        elif result_timer < 300:
            label = "RESTORING NETWORK"
            sub = "VALIDATING SERVICES"
            color = CYAN
        else:
            label = "SYSTEM RESTORED"
            sub = "RANSOMWARE BOT NEUTRALIZED"
            color = GREEN

        title_font = fit_hud_text(label, screen_rect.w - 28, start_size=22, min_size=13, bold=True)
        title = title_font.render(label, True, color)
        subtitle_font = fit_hud_text(sub, screen_rect.w - 32, start_size=12, min_size=9, bold=True)
        subtitle = subtitle_font.render(sub, True, WHITE)
        surface.blit(title, (center_x - title.get_width() // 2, screen_rect.y + 12))
        surface.blit(subtitle, (center_x - subtitle.get_width() // 2, screen_rect.y + 48))

        if result_timer >= 300:
            status = pygame.font.SysFont("consolas", 18, bold=True).render("ALL SYSTEMS SECURE", True, GREEN)
            surface.blit(status, (WINDOW_WIDTH // 2 - status.get_width() // 2, 452))
            if result_timer >= 350:
                prompt = hud_prompt_large_font.render("PRESS R TO PLAY AGAIN", True, YELLOW)
                box = pygame.Rect(WINDOW_WIDTH // 2 - prompt.get_width() // 2 - 18, 493,
                                  prompt.get_width() + 36, 35)
                pygame.draw.rect(surface, (4, 8, 14), box)
                pygame.draw.rect(surface, GREEN, box, 1)
                surface.blit(prompt, (WINDOW_WIDTH // 2 - prompt.get_width() // 2, 499))

    elif game_state == "defeat":
        if result_timer < 42:
            label = "UNAUTHORIZED ENTRY"
            sub = "SECURITY TOOLKIT INCOMPLETE"
        elif result_timer < 108:
            label = "RANSOMWARE BOT ACTIVE"
            sub = "COMMAND SYSTEMS COMPROMISED"
        elif result_timer < 166:
            label = "ENCRYPTION IN PROGRESS"
            sub = "FILES AND SERVICES LOCKING"
        else:
            label = "SYSTEM ENCRYPTED"
            sub = "RANSOMWARE CONTROL ESTABLISHED"

        title_font = fit_hud_text(label, screen_rect.w - 28, start_size=22, min_size=13, bold=True)
        title = title_font.render(label, True, RED)
        subtitle_font = fit_hud_text(sub, screen_rect.w - 32, start_size=12, min_size=9, bold=True)
        subtitle = subtitle_font.render(sub, True, WHITE)
        surface.blit(title, (center_x - title.get_width() // 2, screen_rect.y + 12))
        surface.blit(subtitle, (center_x - subtitle.get_width() // 2, screen_rect.y + 48))

        if result_timer >= 166:
            missing = 6 - len(collected_items)
            message = f"RESPONSE FAILED  •  {missing} SECURITY TOOL{'S' if missing != 1 else ''} MISSING"
            body_font = fit_hud_text(message, 600, start_size=14, min_size=10, bold=True)
            body = body_font.render(message, True, GRAY)
            surface.blit(body, (WINDOW_WIDTH // 2 - body.get_width() // 2, 452))
            if result_timer >= 240:
                prompt = hud_prompt_large_font.render("PRESS R TO TRY AGAIN", True, YELLOW)
                box = pygame.Rect(WINDOW_WIDTH // 2 - prompt.get_width() // 2 - 18, 493,
                                  prompt.get_width() + 36, 35)
                pygame.draw.rect(surface, (4, 8, 14), box)
                pygame.draw.rect(surface, RED, box, 1)
                surface.blit(prompt, (WINDOW_WIDTH // 2 - prompt.get_width() // 2, 499))


# --------------------------------------------------
# MODERN NATIVE-RESOLUTION FINAL ENCOUNTER
# --------------------------------------------------

cinematic_title_font = pygame.font.SysFont("segoeui", 30, bold=True)
cinematic_subtitle_font = pygame.font.SysFont("consolas", 15, bold=True)
cinematic_label_font = pygame.font.SysFont("segoeui", 13, bold=True)
cinematic_small_font = pygame.font.SysFont("consolas", 12)
cinematic_micro_font = pygame.font.SysFont("consolas", 10, bold=True)
cinematic_prompt_font = pygame.font.SysFont("segoeui", 22, bold=True)


def draw_alpha_panel(surface, rect, fill, alpha=180, border=None, border_width=1, radius=10):
    """Draw a translucent rounded panel without forcing the whole scene onto the pixel canvas."""
    panel = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
    pygame.draw.rect(panel, (*fill, alpha), panel.get_rect(), border_radius=radius)
    if border:
        pygame.draw.rect(panel, (*border, min(255, alpha + 55)), panel.get_rect(), border_width,
                         border_radius=radius)
    surface.blit(panel, rect.topleft)


def draw_soft_glow(glow_surface, center, radius, color, strength=110):
    """Layered bloom used for screens, the bot core, and restoration lighting."""
    for factor, alpha in ((1.0, strength // 5), (0.72, strength // 4), (0.46, strength // 3), (0.24, strength)):
        r = max(2, int(radius * factor))
        pygame.draw.circle(glow_surface, (*color, max(0, min(255, alpha))), center, r)


def draw_glow_line(glow_surface, start, end, color, width=3, alpha=110):
    pygame.draw.line(glow_surface, (*color, max(0, min(255, alpha // 3))), start, end, width + 8)
    pygame.draw.line(glow_surface, (*color, max(0, min(255, alpha // 2))), start, end, width + 4)
    pygame.draw.line(glow_surface, (*color, max(0, min(255, alpha))), start, end, width)


def draw_native_gradient(surface, top, bottom, bands=26):
    h = WINDOW_HEIGHT / bands
    for i in range(bands):
        amount = i / max(1, bands - 1)
        c = mix_color(top, bottom, amount)
        pygame.draw.rect(surface, c, (0, int(i * h), WINDOW_WIDTH, int(h) + 2))


def draw_native_network_graph(surface, rect, color, t, healthy=False, severity=0.0):
    """A living line graph rather than decorative static bars."""
    pygame.draw.rect(surface, (5, 11, 20), rect, border_radius=8)
    pygame.draw.rect(surface, mix_color(color, WHITE, 0.18), rect, 1, border_radius=8)
    for y in range(rect.y + 18, rect.bottom - 8, 18):
        pygame.draw.line(surface, (24, 35, 50), (rect.x + 12, y), (rect.right - 12, y), 1)
    points = []
    samples = 18
    for i in range(samples):
        px = rect.x + 12 + int(i * (rect.w - 24) / (samples - 1))
        wave = math.sin((i * 0.75) + t * 0.045) * (5 if healthy else 9)
        jitter = 0 if healthy else math.sin((i * 2.1) + t * 0.11) * (4 + severity * 7)
        py = int(rect.centery + wave + jitter)
        points.append((px, py))
    if len(points) > 1:
        pygame.draw.lines(surface, color, False, points, 2)
    for px, py in points[::4]:
        pygame.draw.circle(surface, mix_color(color, WHITE, 0.35), (px, py), 3)


def draw_native_service_screen(surface, rect, color, t, secure=False, encrypted=False):
    draw_alpha_panel(surface, rect, (7, 14, 25), 225, border=color, border_width=1, radius=9)
    title = cinematic_micro_font.render("SERVICE MATRIX", True, mix_color(color, WHITE, 0.25))
    surface.blit(title, (rect.x + 12, rect.y + 10))
    labels = ["AUTH", "FIREWALL", "ENDPOINT", "BACKUP"]
    for i, label in enumerate(labels):
        y = rect.y + 34 + i * 21
        status_color = GREEN if secure else (RED if encrypted or ((t // 20 + i) % 4 == 0) else CYAN)
        surface.blit(cinematic_micro_font.render(label, True, GRAY), (rect.x + 12, y))
        pygame.draw.rect(surface, (25, 35, 50), (rect.x + 78, y + 2, rect.w - 96, 6), border_radius=3)
        fraction = 0.9 if secure else (0.25 + ((i * 17 + t) % 55) / 100.0)
        if encrypted:
            fraction = 0.12 + (i % 2) * 0.12
        pygame.draw.rect(surface, status_color,
                         (rect.x + 78, y + 2, int((rect.w - 96) * fraction), 6), border_radius=3)


def draw_native_hex(surface, center, radius, color, width=2, rotation=0.0):
    pts = []
    for i in range(6):
        angle = rotation + math.tau * i / 6.0
        pts.append((int(center[0] + math.cos(angle) * radius), int(center[1] + math.sin(angle) * radius)))
    pygame.draw.polygon(surface, color, pts, width)
    return pts


def draw_modern_command_room(surface, theme, t, secure_level=0.0, corruption=0.0):
    """Dense, live spaceship-style command bridge used by both ending outcomes."""
    secure = secure_level > 0.62
    danger = theme == "defeat" or (theme == "victory" and not secure)
    accent = GREEN if secure else (RED if danger else CYAN)
    secondary = CYAN if secure else (RED if danger else BLUE)
    glow = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

    draw_native_gradient(surface, (2, 6, 14), (8, 17, 31), 36)

    # Room shell: angled hull, ceiling, and deep rear wall.
    outer = [(24, 18), (936, 18), (958, 58), (944, 506), (16, 506), (2, 58)]
    inner = [(44, 38), (916, 38), (934, 68), (920, 488), (40, 488), (26, 68)]
    pygame.draw.polygon(surface, (11, 20, 34), outer)
    pygame.draw.polygon(surface, (46, 62, 82), outer, 2)
    pygame.draw.polygon(surface, (6, 13, 25), inner)
    pygame.draw.polygon(surface, mix_color(accent, WHITE, 0.12), inner, 2)

    pygame.draw.polygon(surface, (18, 31, 49), [(58, 48), (902, 48), (860, 115), (100, 115)])
    pygame.draw.polygon(surface, (58, 73, 94), [(58, 48), (902, 48), (860, 115), (100, 115)], 2)
    for x in range(104, 856, 94):
        pygame.draw.rect(surface, (33, 47, 67), (x, 58, 70, 9), border_radius=4)
        pygame.draw.rect(surface, (70, 83, 105), (x + 7, 60, 56, 3), border_radius=2)
        pygame.draw.line(surface, (34, 49, 69), (x + 35, 68), (x + 35, 108), 2)

    # FINAL CEILING LIGHT PASS: recessed rectangular fixtures with visible
    # vertical triangle rays. No circular lamp bodies or circular halo glows.
    lamp_color = GREEN if secure else RED
    lamps = [(176, 70), (480, 66), (784, 70)]
    for idx, (lx, ly) in enumerate(lamps):
        pulse = 0.78 + 0.22 * ((math.sin(t * 0.10 + idx * 1.6) + 1) / 2)
        fixture_edge = mix_color((83, 94, 112), lamp_color, 0.28 * pulse)
        lens = mix_color(lamp_color, WHITE, 0.44)

        # Compact recessed ceiling housing: deliberately rectangular.
        housing = pygame.Rect(lx - 24, ly - 8, 48, 13)
        pygame.draw.rect(surface, (8, 13, 22), housing, border_radius=3)
        pygame.draw.rect(surface, (64, 77, 96), housing, 2, border_radius=3)
        pygame.draw.rect(surface, fixture_edge, (lx - 17, ly - 4, 34, 6), border_radius=2)
        pygame.draw.rect(surface, lens, (lx - 11, ly - 2, 22, 2), border_radius=1)

        # Strong vertical triangle ray. The top begins as a narrow slit and the
        # beam widens steadily toward the floor, exactly like a stage spotlight.
        beam = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        beam_bottom = 392 if idx == 1 else 374
        half_width = 82 if idx == 1 else 72
        outer_alpha = 42 if secure else int(50 + 18 * max(corruption, 0.25))
        inner_alpha = 26 if secure else int(32 + 12 * max(corruption, 0.25))
        outer_points = [
            (lx - 4, ly + 4), (lx + 4, ly + 4),
            (lx + half_width, beam_bottom), (lx - half_width, beam_bottom)
        ]
        inner_points = [
            (lx - 2, ly + 4), (lx + 2, ly + 4),
            (lx + half_width // 2, beam_bottom - 18),
            (lx - half_width // 2, beam_bottom - 18)
        ]
        pygame.draw.polygon(beam, (*lamp_color, outer_alpha), outer_points)
        pygame.draw.polygon(beam, (*mix_color(lamp_color, WHITE, 0.26), inner_alpha), inner_points)
        # Fine edge rays make the triangle silhouette readable even on dark monitors.
        pygame.draw.line(beam, (*lens, 84), outer_points[0], outer_points[3], 2)
        pygame.draw.line(beam, (*lens, 84), outer_points[1], outer_points[2], 2)
        surface.blit(beam, (0, 0))

    # Rear screen wall.
    center_screen = pygame.Rect(300, 100, 360, 142)
    left_screen = pygame.Rect(82, 118, 184, 118)
    right_screen = pygame.Rect(694, 118, 184, 118)
    for rect, border in ((center_screen, accent), (left_screen, secondary), (right_screen, secondary)):
        draw_alpha_panel(surface, rect, (3, 9, 17), 246, border=border, border_width=2, radius=10)
        pygame.draw.rect(surface, (25, 38, 57), (rect.x + 10, rect.y + 10, rect.w - 20, 8), border_radius=4)

    # Left threat/network display.
    graph_rect = pygame.Rect(left_screen.x + 13, left_screen.y + 38, left_screen.w - 26, 58)
    pygame.draw.rect(surface, (7, 15, 27), graph_rect, border_radius=6)
    pygame.draw.rect(surface, secondary, graph_rect, 1, border_radius=6)
    pts = []
    for i in range(14):
        px = graph_rect.x + 7 + i * 11
        amp = 8 if secure else 18
        py = graph_rect.centery + int(math.sin((t + i * 13) * 0.09) * amp) + (0 if secure else ((i * 7) % 15 - 7))
        pts.append((px, py))
    if len(pts) > 1:
        pygame.draw.lines(surface, GREEN if secure else RED, False, pts, 3)
    for pt in pts[::3]:
        pygame.draw.circle(surface, CYAN if secure else ORANGE, pt, 3)

    # Right service matrix.
    services = ("AUTH", "FIREWALL", "ENDPOINT", "BACKUP")
    for i, label in enumerate(services):
        y = right_screen.y + 37 + i * 18
        img = cinematic_micro_font.render(label, True, GRAY)
        surface.blit(img, (right_screen.x + 14, y))
        pygame.draw.rect(surface, (20, 31, 47), (right_screen.x + 93, y + 2, 66, 8), border_radius=4)
        good = secure or (theme == "victory" and secure_level > 0.22 + i * 0.11)
        c = GREEN if good else RED
        fill = 52 if good else 12 + ((t + i * 17) % 22)
        pygame.draw.rect(surface, c, (right_screen.x + 96, y + 4, fill, 4), border_radius=2)

    # Center display live rails; finale text is drawn later.
    for i in range(4):
        yy = center_screen.y + 26 + i * 23
        c = GREEN if secure else (RED if danger and i % 2 else CYAN)
        width = 190 + int(math.sin((t + i * 19) * 0.04) * 45)
        pygame.draw.rect(surface, mix_color((26, 40, 58), c, 0.72), (center_screen.centerx - width // 2, yy, width, 3), border_radius=2)

    # Detailed side operator desks with monitors, buttons, and lower cabinets.
    def operator_station(x, y, side, station_accent, index):
        body = [(x, y + 56), (x + 132, y + 56), (x + 118, y + 120), (x + 12, y + 120)]
        pygame.draw.polygon(surface, (18, 28, 43), body)
        pygame.draw.polygon(surface, (70, 84, 105), body, 2)
        pygame.draw.line(surface, station_accent, (x + 15, y + 68), (x + 116, y + 68), 3)
        mx = x + (70 if side > 0 else 20)
        pygame.draw.rect(surface, (40, 53, 72), (mx + 24, y + 43, 7, 17))
        monitor = pygame.Rect(mx, y, 78, 49)
        pygame.draw.rect(surface, (5, 10, 18), monitor, border_radius=6)
        pygame.draw.rect(surface, (87, 102, 126), monitor, 2, border_radius=6)
        pygame.draw.rect(surface, station_accent, (monitor.x + 7, monitor.y + 7, monitor.w - 14, 4), border_radius=2)
        for row in range(3):
            c = station_accent if row != 1 else (GREEN if secure else RED)
            pygame.draw.rect(surface, c, (monitor.x + 10, monitor.y + 17 + row * 8, 22 + ((index + row) % 3) * 11, 3), border_radius=1)
        for j, c in enumerate((CYAN, GREEN, ORANGE, RED, PURPLE)):
            bx = x + 16 + j * 18
            by = y + 82 + (j % 2) * 10
            pygame.draw.rect(surface, (8, 13, 23), (bx, by, 13, 7), border_radius=2)
            pygame.draw.rect(surface, c if secure or (j + index) % 3 else RED, (bx + 3, by + 2, 7, 3), border_radius=1)
        for d in range(3):
            dx = x + 16 + d * 35
            pygame.draw.rect(surface, (10, 17, 28), (dx, y + 96, 29, 20), border_radius=2)
            pygame.draw.rect(surface, (52, 65, 84), (dx, y + 96, 29, 20), 1, border_radius=2)
            pygame.draw.rect(surface, station_accent, (dx + 20, y + 102, 4, 3), border_radius=1)

    operator_station(32, 240, -1, secondary, 0)
    operator_station(176, 255, -1, accent, 1)
    operator_station(752, 240, 1, secondary, 2)
    operator_station(608, 255, 1, accent, 3)

    # Central command desk and raised boss platform.
    deck_top = [(205, 285), (755, 285), (714, 354), (246, 354)]
    deck_front = [(246, 354), (714, 354), (687, 389), (273, 389)]
    pygame.draw.polygon(surface, (35, 48, 66), deck_top)
    pygame.draw.polygon(surface, (13, 22, 36), deck_front)
    pygame.draw.polygon(surface, (84, 98, 119), deck_top, 2)
    pygame.draw.line(surface, mix_color(accent, WHITE, 0.18), (230, 297), (730, 297), 2)
    pygame.draw.ellipse(surface, (4, 8, 14), (362, 232, 236, 98))
    pygame.draw.ellipse(surface, (65, 79, 101), (372, 241, 216, 80), 2)
    pygame.draw.ellipse(surface, accent, (394, 253, 172, 57), 2)

    # Six integrated recovery modules.
    module_centers = [(278, 329), (358, 315), (435, 307), (525, 307), (602, 315), (682, 329)]
    item_names = list(ITEM_DATA.keys())
    for i, (mx, my) in enumerate(module_centers):
        item_color = ITEM_DATA[item_names[i]]["color"]
        rect = pygame.Rect(mx - 27, my - 18, 54, 36)
        pygame.draw.rect(surface, (6, 12, 21), rect, border_radius=6)
        pygame.draw.rect(surface, mix_color(item_color, GRAY_DARK, 0.25), rect, 2, border_radius=6)
        pygame.draw.rect(surface, (24, 34, 49), (rect.x + 5, rect.y + 5, rect.w - 10, 15), border_radius=4)
        draw_item_icon(surface, item_names[i], mx - 16, my - 11, item_color, 1)
        led = GREEN if secure else (RED if theme == "defeat" and corruption > 0.18 + i * 0.08 else GRAY_DARK)
        pygame.draw.circle(surface, led, (rect.right - 7, rect.y + 7), 3)

    # Reflective floor panels and lit central walkway.
    horizon = 354
    pygame.draw.polygon(surface, (6, 12, 22), [(36, horizon), (924, horizon), (952, 510), (8, 510)])
    vanish = (480, 344)
    for x in (30, 110, 195, 280, 365, 430, 530, 595, 680, 765, 850, 930):
        pygame.draw.line(surface, (27, 41, 59), vanish, (x, 510), 2)
    for yy in (379, 406, 435, 465, 494):
        inset = int((yy - horizon) * 0.40)
        pygame.draw.line(surface, (32, 46, 64), (30 + inset, yy), (930 - inset, yy), 2)
    runway = [(425, 356), (535, 356), (597, 510), (363, 510)]
    pygame.draw.polygon(surface, (11, 18, 30), runway)
    pygame.draw.polygon(surface, mix_color(accent, (45, 60, 78), 0.45), runway, 2)
    for i, yy in enumerate((374, 397, 424, 455, 489)):
        half = 9 + i * 10
        c = accent if ((t // 7 + i) % 3 == 0) else (46, 61, 80)
        pygame.draw.rect(surface, c, (480 - half, yy, half * 2, 4), border_radius=2)
        pygame.draw.rect(glow, (*c, 28), (480 - half - 4, yy + 4, half * 2 + 8, 10), border_radius=5)

    # Purpose-built floor equipment pods replace the old ambiguous rectangles.
    # Each reads as a compact cooling/power/server unit with an angled top,
    # status display, vent bank, cable port, side depth, and floor feet.
    def floor_equipment_pod(x, y, side, pod_accent, index):
        w, h = 124, 62
        shell = [(x + 8, y), (x + w - 16, y), (x + w, y + 14),
                 (x + w - 7, y + h - 8), (x + 14, y + h - 8), (x, y + 14)]
        # Main shell plus a darker side face gives each pod real 2.5D depth.
        pygame.draw.polygon(surface, (18, 28, 43), shell)
        side_face = (
            [(x, y + 14), (x + 14, y + h - 8), (x + 14, y + h - 2), (x + 4, y + h - 10)]
            if side < 0 else
            [(x + w, y + 14), (x + w - 7, y + h - 8), (x + w - 7, y + h - 2), (x + w + 2, y + h - 10)]
        )
        pygame.draw.polygon(surface, (9, 16, 27), side_face)
        pygame.draw.polygon(surface, (67, 82, 103), shell, 2)
        # Angled service lid.
        pygame.draw.polygon(surface, (31, 44, 62), [
            (x + 12, y + 6), (x + w - 20, y + 6),
            (x + w - 31, y + 18), (x + 22, y + 18)
        ])
        pygame.draw.line(surface, pod_accent, (x + 20, y + 10), (x + w - 31, y + 10), 3)
        # Small system-status display.
        display = pygame.Rect(x + (16 if side < 0 else 70), y + 23, 38, 20)
        pygame.draw.rect(surface, (5, 11, 20), display, border_radius=3)
        pygame.draw.rect(surface, (79, 94, 116), display, 1, border_radius=3)
        status = GREEN if secure else (RED if danger else CYAN)
        pygame.draw.rect(surface, status, (display.x + 5, display.y + 5, 20, 3), border_radius=1)
        pygame.draw.rect(surface, pod_accent, (display.x + 5, display.y + 11, 27, 2), border_radius=1)
        # Cooling vent bank plus a small visible fan grille.
        vent_x = x + (64 if side < 0 else 16)
        for row in range(4):
            pygame.draw.rect(surface, (7, 13, 22), (vent_x, y + 24 + row * 6, 40, 3), border_radius=1)
            pygame.draw.rect(surface, (45, 58, 76), (vent_x + 2, y + 25 + row * 6, 31, 1))
        fan_x = vent_x + 34
        fan_y = y + 47
        pygame.draw.circle(surface, (5, 10, 18), (fan_x, fan_y), 7)
        pygame.draw.circle(surface, (70, 84, 103), (fan_x, fan_y), 7, 1)
        pygame.draw.line(surface, (48, 62, 80), (fan_x - 4, fan_y), (fan_x + 4, fan_y), 1)
        pygame.draw.line(surface, (48, 62, 80), (fan_x, fan_y - 4), (fan_x, fan_y + 4), 1)
        # Circular power/cable coupling makes the purpose visually obvious.
        port_x = x + (109 if side < 0 else 15)
        pygame.draw.circle(surface, (6, 12, 21), (port_x, y + 46), 8)
        pygame.draw.circle(surface, pod_accent, (port_x, y + 46), 8, 2)
        pygame.draw.circle(surface, status, (port_x, y + 46), 3)
        # Damage/restoration indicators.
        leds = [status, pod_accent, ORANGE if danger and index % 2 else GREEN]
        for j, c in enumerate(leds):
            pygame.draw.circle(surface, c, (x + 22 + j * 12, y + 49), 2)
        if danger and corruption > 0.55:
            pygame.draw.line(surface, RED, (x + 50, y + 20), (x + 63, y + 31), 2)
            pygame.draw.line(surface, ORANGE, (x + 63, y + 31), (x + 55, y + 40), 2)
        # Floor feet and subtle connection cable.
        pygame.draw.rect(surface, (6, 11, 19), (x + 18, y + h - 8, 22, 6), border_radius=2)
        pygame.draw.rect(surface, (6, 11, 19), (x + w - 42, y + h - 8, 22, 6), border_radius=2)
        cable_end = (430 if side < 0 else 530, 471)
        pygame.draw.line(surface, (25, 37, 52), (x + w//2, y + h - 3), cable_end, 2)

    floor_equipment_pod(48, 419, -1, secondary, 0)
    floor_equipment_pod(184, 432, -1, accent, 1)
    floor_equipment_pod(788, 419, 1, secondary, 2)
    floor_equipment_pod(652, 432, 1, accent, 3)

    particle_color = GREEN if secure else (RED if danger else CYAN)
    for i in range(32):
        px = 58 + ((i * 83 + t * (1 + i % 3)) % 844)
        py = 118 + ((i * 37 + t // 2) % 315)
        pygame.draw.circle(surface, mix_color((21, 31, 46), particle_color, 0.68), (px, py), 1 + (i % 2))

    # Keep only a restrained platform glow. In the secure state the shield
    # hologram supplies the centerpiece, so this must never become a green orb.
    platform_radius = 42 if secure else 68
    platform_alpha = 18 if secure else 30
    draw_soft_glow(glow, (480, 302), platform_radius, accent, platform_alpha)
    surface.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    return center_screen, module_centers

def draw_modern_ransomware_bot(surface, center, t, power=1.0, damage=0.0, cable_strength=1.0, collapse=0.0):
    """Large mechanical ransomware boss: head, torso, arms, fists, legs, and lock core."""
    cx, cy = center
    glow = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    red = mix_color((128, 21, 35), RED, clamp(power, 0.0, 1.0))
    hot = mix_color(RED, WHITE, 0.20 + 0.42 * damage)
    steel = (48, 57, 72)
    steel_dark = (22, 29, 40)
    steel_light = (104, 116, 139)
    hover = int(math.sin(t * 0.07) * 2 * (1.0 - collapse))
    cy += hover

    # Malware cables behind the robot.
    targets = [(278, 329), (358, 315), (435, 307), (525, 307), (602, 315), (682, 329)]
    for i, target in enumerate(targets):
        prog = clamp(cable_strength - i * 0.035, 0.0, 1.0)
        if prog <= 0:
            continue
        sx = cx + (-72 + i * 29)
        sy = cy + 42
        ex = int(lerp(sx, target[0], prog))
        ey = int(lerp(sy, target[1], prog))
        mid_a = (int(lerp(sx, ex, 0.33)), sy + 35 + (i % 2) * 9)
        mid_b = (int(lerp(sx, ex, 0.72)), ey - 28 - (i % 3) * 5)
        pts = [(sx, sy), mid_a, mid_b, (ex, ey)]
        pygame.draw.lines(surface, (8, 5, 11), False, pts, 12)
        pygame.draw.lines(surface, mix_color((80, 14, 28), red, 0.84), False, pts, 5)
        q = (t * 0.018 + i * 0.15) % 1.0
        if q < prog:
            if q < 0.34:
                a, b, local = pts[0], pts[1], q / 0.34
            elif q < 0.72:
                a, b, local = pts[1], pts[2], (q - 0.34) / 0.38
            else:
                a, b, local = pts[2], pts[3], (q - 0.72) / 0.28
            px = int(lerp(a[0], b[0], local))
            py = int(lerp(a[1], b[1], local))
            pygame.draw.circle(surface, hot, (px, py), 4)
            draw_soft_glow(glow, (px, py), 18, RED, 54)

    # Piece-separation offsets during destruction.
    def sep(side=0, vertical=0, amount=1.0):
        return int(side * collapse * 72 * amount), int(vertical * collapse * 64 * amount)

    pygame.draw.ellipse(surface, (1, 4, 9), (cx - 96, cy + 92, 192, 28))

    # Legs / feet.
    for side in (-1, 1):
        dx, dy = sep(side, 1, 0.55)
        hip = (cx + side * 34 + dx, cy + 46 + dy)
        knee = (cx + side * 42 + dx, cy + 82 + dy)
        foot = (cx + side * 48 + dx, cy + 109 + dy)
        pygame.draw.line(surface, steel_dark, hip, knee, 20)
        pygame.draw.line(surface, steel_light, hip, knee, 6)
        pygame.draw.line(surface, steel_dark, knee, foot, 18)
        pygame.draw.line(surface, red, knee, foot, 4)
        fr = pygame.Rect(foot[0] - 18, foot[1] - 7, 36, 16)
        pygame.draw.rect(surface, (12, 17, 26), fr, border_radius=5)
        pygame.draw.rect(surface, steel_light, fr, 3, border_radius=5)
        pygame.draw.rect(surface, red, (fr.x + 6, fr.y + 4, 24, 3), border_radius=2)

    # Torso and layered armor.
    tdx, tdy = sep(0, -1, 0.12)
    tcx, tcy = cx + tdx, cy + tdy
    torso = [(tcx - 64, tcy - 30), (tcx - 45, tcy - 55), (tcx + 45, tcy - 55),
             (tcx + 64, tcy - 30), (tcx + 55, tcy + 52), (tcx + 32, tcy + 65),
             (tcx - 32, tcy + 65), (tcx - 55, tcy + 52)]
    pygame.draw.polygon(surface, steel_dark, torso)
    pygame.draw.polygon(surface, steel, torso, 8)
    pygame.draw.polygon(surface, red, torso, 3)
    chest = [(tcx - 45, tcy - 28), (tcx + 45, tcy - 28), (tcx + 35, tcy + 45), (tcx - 35, tcy + 45)]
    pygame.draw.polygon(surface, (18, 24, 34), chest)
    pygame.draw.polygon(surface, steel_light, chest, 3)

    # Shoulders, articulated arms, and heavy fists.
    arm_swing = int(math.sin(t * 0.07) * 5)
    for side in (-1, 1):
        dx, dy = sep(side, -1 if side < 0 else 1, 0.78)
        shoulder = (cx + side * 76 + dx, cy - 25 + dy)
        elbow = (cx + side * 112 + dx, cy + 12 + arm_swing * side + dy)
        hand = (cx + side * 138 + dx, cy + 53 + dy)
        pygame.draw.circle(surface, steel_dark, shoulder, 30)
        pygame.draw.circle(surface, steel_light, shoulder, 30, 5)
        pygame.draw.arc(surface, red, pygame.Rect(shoulder[0]-25, shoulder[1]-25, 50, 50), 0.25, 2.85, 4)
        pygame.draw.line(surface, steel_dark, shoulder, elbow, 24)
        pygame.draw.line(surface, steel_light, shoulder, elbow, 9)
        pygame.draw.line(surface, red, shoulder, elbow, 4)
        pygame.draw.circle(surface, (11, 16, 25), elbow, 13)
        pygame.draw.circle(surface, red, elbow, 13, 3)
        pygame.draw.line(surface, steel_dark, elbow, hand, 22)
        pygame.draw.line(surface, steel_light, elbow, hand, 8)
        pygame.draw.line(surface, red, elbow, hand, 3)
        pygame.draw.circle(surface, (8, 12, 19), hand, 17)
        pygame.draw.circle(surface, steel_light, hand, 17, 4)
        pygame.draw.circle(surface, hot, hand, 8, 2)
        pygame.draw.line(surface, hot, hand, (hand[0] + side * 22, hand[1] - 15), 4)
        pygame.draw.line(surface, hot, hand, (hand[0] + side * 24, hand[1]), 4)
        pygame.draw.line(surface, hot, hand, (hand[0] + side * 22, hand[1] + 15), 4)

    # Head / visor.
    hdx, hdy = sep(0, -1, 0.55)
    hcx, hcy = cx + hdx, cy - 88 + hdy
    pygame.draw.rect(surface, steel_dark, (hcx - 17, hcy + 29, 34, 25), border_radius=8)
    pygame.draw.rect(surface, red, (hcx - 10, hcy + 34, 20, 5), border_radius=2)
    helmet = [(hcx - 52, hcy - 21), (hcx - 38, hcy - 39), (hcx + 38, hcy - 39),
              (hcx + 52, hcy - 21), (hcx + 45, hcy + 30), (hcx - 45, hcy + 30)]
    pygame.draw.polygon(surface, steel_dark, helmet)
    pygame.draw.polygon(surface, steel_light, helmet, 6)
    pygame.draw.polygon(surface, red, helmet, 3)
    visor = pygame.Rect(hcx - 38, hcy - 18, 76, 34)
    pygame.draw.rect(surface, (2, 4, 9), visor, border_radius=7)
    ey = visor.centery - 3
    pygame.draw.polygon(surface, hot, [(hcx-29, ey-5), (hcx-8, ey-2), (hcx-17, ey+7)])
    pygame.draw.polygon(surface, hot, [(hcx+29, ey-5), (hcx+8, ey-2), (hcx+17, ey+7)])
    pygame.draw.line(surface, red, (hcx - 11, visor.bottom - 7), (hcx + 11, visor.bottom - 7), 3)

    # Ransomware lock core.
    core_y = tcy + 8
    pygame.draw.circle(surface, (5, 9, 16), (tcx, core_y), 37)
    pygame.draw.circle(surface, steel_light, (tcx, core_y), 37, 4)
    pygame.draw.circle(surface, hot if damage > 0.6 else YELLOW, (tcx, core_y), 30, 4)
    draw_pixel_lock(surface, tcx - 18, core_y - 22, hot if damage > 0.68 else YELLOW, 2)
    draw_soft_glow(glow, (tcx, core_y), 70, RED if damage < 0.8 else ORANGE, 70)

    # Cracks, sparks, and destruction fragments.
    if damage > 0.08:
        crack = WHITE if damage > 0.72 else ORANGE
        pygame.draw.line(surface, crack, (tcx - 20, tcy - 5), (tcx + 3, tcy + 14), 4)
        pygame.draw.line(surface, crack, (tcx + 3, tcy + 14), (tcx - 12, tcy + 38), 3)
        pygame.draw.line(surface, crack, (hcx + 24, hcy - 6), (hcx + 7, hcy + 10), 3)
        for i in range(int(8 + damage * 18)):
            a = i * 2.31 + t * 0.04
            rr = 72 + (i % 5) * 13
            px = int(cx + math.cos(a) * rr)
            py = int(cy + math.sin(a) * rr * 0.7)
            pygame.draw.rect(surface, ORANGE if i % 3 == 0 else RED, (px, py, 3 + i % 3, 3))
    if collapse > 0.02:
        for i in range(34):
            a = i * 2.399 + t * 0.02
            rr = 58 + collapse * (55 + (i % 9) * 12)
            px = int(cx + math.cos(a) * rr)
            py = int(cy + math.sin(a) * rr * 0.72)
            c = [RED, ORANGE, CYAN, WHITE][i % 4]
            pygame.draw.rect(surface, c, (px, py, 3 + i % 4, 3 + (i + 1) % 3))

    surface.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

def draw_cinematic_player_native(surface, x, y, facing="up", pose="idle", frame=0):
    """Crisp native-resolution cinematic sprite; consistent proportions across poses."""
    u = 3
    skin = (232, 184, 145)
    skin_light = (249, 211, 176)
    skin_shadow = (183, 123, 89)
    hair = (68, 40, 25)
    hair_dark = (43, 25, 19)
    hair_light = (113, 72, 41)
    # Match the gameplay sprite: maroon-red hoodie with warm highlights.
    hoodie = (122, 51, 66)
    hoodie_dark = (49, 20, 29)
    hoodie_light = (158, 72, 88)
    shirt = (37, 211, 220)
    pants = (15, 24, 39)
    shoes = (124, 138, 160)
    eye = (16, 17, 21)
    mouth = (115, 65, 60)

    ox = int(x - 11 * u)
    oy = int(y - 16 * u)
    bob = -2 * u if pose == "celebrate" and (result_timer // 7) % 6 in (1, 2) else 0
    oy += bob

    def r(px, py, w, h, c):
        pygame.draw.rect(surface, c, (ox + px * u, oy + py * u, w * u, h * u))

    # Ground shadow changes with pose.
    shadow_w = 42 if pose not in ("defeated", "celebrate") else (50 if pose == "defeated" else 32)
    pygame.draw.ellipse(surface, (2, 5, 10), (x - shadow_w // 2, y + 44 - bob, shadow_w, 10))

    if pose == "defeated":
        # Kneeling, bowed head, readable closed eyes; no symbolic face marks.
        r(4, 17, 14, 9, hoodie)
        r(7, 18, 8, 7, hoodie_dark)
        r(4, 25, 6, 4, pants)
        r(12, 25, 6, 4, pants)
        r(2, 22, 3, 6, hoodie)
        r(17, 22, 3, 6, hoodie)
        r(2, 27, 3, 2, skin)
        r(17, 27, 3, 2, skin)
        r(4, 29, 7, 2, shoes)
        r(11, 29, 7, 2, shoes)
        r(4, 5, 14, 4, hair_dark)
        r(3, 7, 16, 4, hair)
        r(5, 11, 12, 5, skin_shadow)
        pygame.draw.line(surface, (49, 31, 24), (ox + 6*u, oy + 13*u), (ox + 9*u, oy + 13*u), u)
        pygame.draw.line(surface, (49, 31, 24), (ox + 12*u, oy + 13*u), (ox + 15*u, oy + 13*u), u)
        pygame.draw.line(surface, mouth, (ox + 9*u, oy + 15*u), (ox + 12*u, oy + 15*u), u)
        return

    # Shared legs and lower body.
    leg_shift = u if frame and pose == "walk" else 0
    r(5, 25, 5, 5, pants)
    r(12, 25 + (1 if leg_shift else 0), 5, 5, pants)
    r(4, 30, 7, 2, shoes)
    r(11, 30 + (1 if leg_shift else 0), 7, 2, shoes)
    r(6, 30, 3, 1, WHITE)
    r(13, 30 + (1 if leg_shift else 0), 3, 1, WHITE)

    if facing == "up":
        # Cinematic version of approved Option 3: layered, slightly longer rear
        # hair with an irregular natural edge. Front-facing art is unchanged.
        pygame.draw.polygon(surface, hair_dark, [
            (ox + 5*u, oy + 3*u), (ox + 8*u, oy + 1*u),
            (ox + 14*u, oy + 1*u), (ox + 17*u, oy + 3*u),
            (ox + 19*u, oy + 6*u), (ox + 18*u, oy + 10*u),
            (ox + 16*u, oy + 12*u), (ox + 15*u, oy + 14*u),
            (ox + 13*u, oy + 13*u), (ox + 11*u, oy + 15*u),
            (ox + 9*u, oy + 13*u), (ox + 7*u, oy + 14*u),
            (ox + 5*u, oy + 11*u), (ox + 3*u, oy + 10*u),
            (ox + 3*u, oy + 6*u)
        ])
        pygame.draw.polygon(surface, hair, [
            (ox + 6*u, oy + 3*u), (ox + 9*u, oy + 2*u),
            (ox + 14*u, oy + 2*u), (ox + 17*u, oy + 4*u),
            (ox + 18*u, oy + 7*u), (ox + 16*u, oy + 10*u),
            (ox + 15*u, oy + 12*u), (ox + 13*u, oy + 11*u),
            (ox + 12*u, oy + 13*u), (ox + 10*u, oy + 12*u),
            (ox + 8*u, oy + 13*u), (ox + 7*u, oy + 11*u),
            (ox + 5*u, oy + 11*u), (ox + 4*u, oy + 8*u),
            (ox + 5*u, oy + 5*u)
        ])
        r(7, 3, 4, 1, hair_light)
        r(12, 3, 3, 1, hair_light)
        r(15, 5, 2, 1, hair_light)
        pygame.draw.line(surface, hair_dark, (ox + 7*u, oy + 6*u), (ox + 6*u, oy + 10*u), u)
        pygame.draw.line(surface, hair_dark, (ox + 10*u, oy + 5*u), (ox + 9*u, oy + 12*u), u)
        pygame.draw.line(surface, hair_dark, (ox + 13*u, oy + 5*u), (ox + 12*u, oy + 12*u), u)
        pygame.draw.line(surface, hair_dark, (ox + 16*u, oy + 6*u), (ox + 15*u, oy + 11*u), u)
        r(3, 8, 2, 3, skin_shadow)
        r(17, 8, 2, 3, skin_shadow)
        r(8, 12, 6, 5, skin_shadow)
        r(9, 13, 4, 4, skin)
        pygame.draw.polygon(surface, hoodie_light, [
            (ox + 7*u, oy + 14*u), (ox + 15*u, oy + 14*u),
            (ox + 20*u, oy + 19*u), (ox + 18*u, oy + 23*u),
            (ox + 4*u, oy + 23*u), (ox + 2*u, oy + 19*u)
        ])
        pygame.draw.polygon(surface, hoodie, [
            (ox + 6*u, oy + 17*u), (ox + 16*u, oy + 17*u),
            (ox + 16*u, oy + 28*u), (ox + 6*u, oy + 28*u)
        ])
        pygame.draw.arc(surface, hoodie_dark, (ox + 7*u, oy + 17*u, 8*u, 7*u), 0, math.pi, u)
        pygame.draw.line(surface, hoodie_light, (ox + 7*u, oy + 27*u), (ox + 15*u, oy + 27*u), u)
        arm = 1 if frame else 0
        r(2, 19 + arm, 3, 8, hoodie)
        r(17, 19 + (1-arm), 3, 8, hoodie)
        r(2, 27 + arm, 3, 2, skin)
        r(17, 27 + (1-arm), 3, 2, skin)
        return

    # Front face is tapered instead of a square block.
    pygame.draw.polygon(surface, skin_shadow, [
        (ox + 5*u, oy + 6*u), (ox + 17*u, oy + 6*u),
        (ox + 18*u, oy + 11*u), (ox + 15*u, oy + 15*u),
        (ox + 7*u, oy + 15*u), (ox + 4*u, oy + 11*u)
    ])
    pygame.draw.polygon(surface, skin, [
        (ox + 6*u, oy + 5*u), (ox + 16*u, oy + 5*u),
        (ox + 17*u, oy + 11*u), (ox + 14*u, oy + 15*u),
        (ox + 8*u, oy + 15*u), (ox + 5*u, oy + 11*u)
    ])
    r(3, 9, 2, 4, skin)
    r(17, 9, 2, 4, skin)
    r(6, 6, 3, 2, skin_light)
    # Hair.
    r(5, 1, 11, 2, hair_dark)
    r(3, 3, 16, 3, hair)
    r(3, 5, 3, 6, hair)
    r(16, 5, 3, 5, hair)
    r(8, 5, 7, 1, hair)
    r(7, 2, 5, 1, hair_light)
    # Face.
    r(7, 8, 2, 2, eye)
    r(13, 8, 2, 2, eye)
    r(7, 8, 1, 1, WHITE)
    r(13, 8, 1, 1, WHITE)
    r(10, 10, 1, 2, skin_shadow)
    pygame.draw.line(surface, mouth, (ox + 9*u, oy + 13*u), (ox + 13*u, oy + 13*u), u)
    # Neck and hoodie overlap slightly so the head reads as physically attached.
    r(8, 14, 6, 4, skin_shadow)
    r(9, 14, 4, 4, skin)
    pygame.draw.polygon(surface, hoodie_light, [
        (ox + 7*u, oy + 15*u), (ox + 15*u, oy + 15*u),
        (ox + 20*u, oy + 20*u), (ox + 18*u, oy + 24*u),
        (ox + 4*u, oy + 24*u), (ox + 2*u, oy + 20*u)
    ])
    r(6, 18, 10, 10, hoodie)
    r(8, 18, 1, 5, WHITE)
    r(14, 18, 1, 5, WHITE)
    # Clean hoodie front: no ID badge.
    pygame.draw.line(surface, hoodie_dark, (ox + 8*u, oy + 26*u), (ox + 14*u, oy + 26*u), u)

    if pose == "celebrate":
        r(1, 13, 3, 9, hoodie)
        r(18, 13, 3, 9, hoodie)
        r(1, 10, 3, 3, skin)
        r(18, 10, 3, 3, skin)
    else:
        arm = 1 if frame else 0
        r(2, 20 + arm, 3, 7, hoodie)
        r(17, 20 + (1-arm), 3, 7, hoodie)
        r(2, 27 + arm, 3, 2, skin)
        r(17, 27 + (1-arm), 3, 2, skin)


def draw_victory_shield_hologram(surface, center, t, strength=1.0):
    """Approved Option B: cyan/green shield + checkmark hologram.

    Drawn as live Pygame geometry (not a pasted image). It uses layered scan
    rings, translucent shield faces, a projector base, and restrained particles
    so the player remains readable in front of it.
    """
    strength = clamp(strength, 0.0, 1.0)
    if strength <= 0.01:
        return

    cx, cy = center
    holo = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    pulse = (math.sin(t * 0.09) + 1.0) * 0.5
    cyan = mix_color(CYAN, GREEN, 0.42)
    bright = mix_color(cyan, WHITE, 0.28 + 0.18 * pulse)
    alpha = int(62 + 54 * strength)

    # Projector base on the floor.
    pygame.draw.ellipse(surface, (2, 8, 14), (cx - 88, cy + 118, 176, 28))
    pygame.draw.ellipse(surface, (28, 48, 60), (cx - 68, cy + 120, 136, 19))
    pygame.draw.ellipse(surface, cyan, (cx - 54, cy + 122, 108, 14), 3)
    pygame.draw.ellipse(surface, bright, (cx - 30, cy + 125, 60, 7), 2)

    # Vertical projection volume, deliberately narrower than the old green orb.
    pygame.draw.polygon(holo, (*cyan, int(22 * strength)), [
        (cx - 34, cy + 124), (cx + 34, cy + 124),
        (cx + 62, cy - 104), (cx - 62, cy - 104)
    ])

    # Shield silhouette: broad shoulders, tapered lower point.
    shield = [
        (cx, cy - 104), (cx + 67, cy - 82), (cx + 60, cy - 10),
        (cx + 43, cy + 42), (cx, cy + 78),
        (cx - 43, cy + 42), (cx - 60, cy - 10), (cx - 67, cy - 82)
    ]
    inner = [
        (cx, cy - 88), (cx + 52, cy - 70), (cx + 46, cy - 14),
        (cx + 33, cy + 31), (cx, cy + 58),
        (cx - 33, cy + 31), (cx - 46, cy - 14), (cx - 52, cy - 70)
    ]
    pygame.draw.polygon(holo, (*cyan, int(alpha * 0.34)), shield)
    pygame.draw.polygon(holo, (*bright, int(alpha * 0.95)), shield, 4)
    pygame.draw.polygon(holo, (*cyan, int(alpha * 0.82)), inner, 2)

    # Check mark is unmistakable at a glance.
    check = [(cx - 30, cy - 7), (cx - 8, cy + 16), (cx + 37, cy - 36)]
    pygame.draw.lines(holo, (*bright, int(220 * strength)), False, check, 10)
    pygame.draw.lines(holo, (*WHITE, int(105 * strength)), False, check, 3)

    # Horizontal hologram scanlines contained inside the shield.
    for i in range(9):
        yy = cy - 73 + i * 15
        width = int(48 - abs(yy - (cy - 5)) * 0.22)
        if width > 12:
            flicker = 0.55 + 0.45 * ((math.sin(t * 0.13 + i * 1.7) + 1) / 2)
            pygame.draw.line(holo, (*cyan, int(42 * strength * flicker)),
                             (cx - width, yy), (cx + width, yy), 2)

    # Restrained security arcs frame the shield without recreating a circular orb.
    for radius, speed, phase in ((92, 0.045, 0.0), (110, -0.034, 1.8)):
        a = t * speed + phase
        left = (cx - radius, cy - 8)
        right = (cx + radius, cy - 8)
        pygame.draw.arc(holo, (*cyan, int(54 * strength)),
                        (cx - radius, cy - 34, radius * 2, 64),
                        math.radians(205), math.radians(335), 2)
        px = int(cx + math.cos(a) * radius)
        py = int(cy - 3 + math.sin(a) * 21)
        pygame.draw.circle(holo, (*bright, int(185 * strength)), (px, py), 3)

    # Sparse holographic particles.
    for i in range(18):
        a = i * 2.399 + t * 0.025
        rr = 78 + (i % 4) * 11
        px = int(cx + math.cos(a) * rr)
        py = int(cy - 8 + math.sin(a) * rr * 0.72)
        if (i + t // 8) % 3 != 0:
            pygame.draw.rect(holo, (*([CYAN, GREEN, WHITE][i % 3]), int(105 * strength)),
                             (px, py, 3 + i % 2, 3))

    surface.blit(holo, (0, 0))


def draw_modern_finale_native(surface, outcome, t):
    """Final boss cinematic for both outcomes; the room stays alive after the result."""
    item_names = list(ITEM_DATA.keys())

    if outcome == "victory":
        if t < 50:
            stage = "entry"
        elif t < 118:
            stage = "authorize"
        elif t < 195:
            stage = "counter"
        elif t < 265:
            stage = "destroy"
        elif t < 330:
            stage = "restore"
        else:
            stage = "secure"

        secure_level = clamp((t - 270) / 72.0, 0.0, 1.0)
        center_screen, module_centers = draw_modern_command_room(surface, "victory", t, secure_level, 0.0)

        if t < 50:
            p = t / 50.0
            draw_cinematic_player_native(surface, 480, int(548 - p * 116), "up", "walk", (t // 7) % 2)
        elif t < 330:
            draw_cinematic_player_native(surface, 480, 432, "up", "idle", 0)
        else:
            draw_cinematic_player_native(surface, 480, 432, "down", "celebrate", (t // 7) % 2)

        activated = 0 if t < 50 else min(6, 1 + (t - 50) // 10)
        for i, pos in enumerate(module_centers):
            if i >= activated:
                continue
            c = ITEM_DATA[item_names[i]]["color"]
            pulse = 18 + int(5 * ((math.sin((t + i * 11) * 0.17) + 1) / 2))
            pygame.draw.circle(surface, mix_color(c, WHITE, 0.25), pos, pulse, 2)
            pygame.draw.circle(surface, c, (pos[0] + 19, pos[1] - 12), 4)

        if t < 118:
            draw_modern_ransomware_bot(surface, (480, 276), t, 0.86, 0.0, 1.0)
        elif t < 195:
            damage = clamp((t - 118) / 77.0, 0.0, 1.0)
            draw_modern_ransomware_bot(surface, (480, 276), t, 1.0, damage, 1.0)
            for i in range(activated):
                startp = module_centers[i]
                c = ITEM_DATA[item_names[i]]["color"]
                mid = ((startp[0] + 480)//2, startp[1] - 45 - (i % 2) * 18)
                pygame.draw.lines(surface, mix_color(c, WHITE, 0.28), False, [startp, mid, (480, 284)], 3)
                q = (t * 0.032 + i * 0.16) % 1.0
                if q < 0.5:
                    px = int(lerp(startp[0], mid[0], q * 2)); py = int(lerp(startp[1], mid[1], q * 2))
                else:
                    px = int(lerp(mid[0], 480, (q - 0.5) * 2)); py = int(lerp(mid[1], 284, (q - 0.5) * 2))
                pygame.draw.circle(surface, WHITE, (px, py), 4)
        elif t < 265:
            collapse = clamp((t - 195) / 70.0, 0.0, 1.0)
            draw_modern_ransomware_bot(surface, (480, 276), t, 0.65, 1.0, 1.0-collapse, collapse)
            for j in range(2):
                rr = int(55 + collapse * (85 + j * 60))
                pygame.draw.circle(surface, CYAN if j == 0 else GREEN, (480, 284), rr, 3)
        elif t < 330:
            p = (t - 265) / 65.0
            y = int(150 + p * 290)
            pygame.draw.line(surface, GREEN, (78, y), (882, y), 4)
            pygame.draw.line(surface, CYAN, (100, y - 9), (860, y - 9), 2)

        if stage == "entry":
            title, sub, color = "RANSOMWARE CORE DETECTED", "FINAL RESPONSE SEQUENCE INITIALIZED", RED
        elif stage == "authorize":
            title, sub, color = "SECURITY TOOLCHAIN AUTHORIZED", "SIX RECOVERY MODULES ONLINE", CYAN
        elif stage == "counter":
            title, sub, color = "COUNTERMEASURES DEPLOYED", "DESTABILIZING RANSOMWARE CORE", ORANGE
        elif stage == "destroy":
            title, sub, color = "MALWARE CORE FAILING", "TERMINATING MALICIOUS PROCESS", RED
        elif stage == "restore":
            title, sub, color = "RESTORING COMPANY SYSTEMS", "VALIDATING NETWORK • BACKUPS • ACCESS", CYAN
        else:
            title, sub, color = "SYSTEM RESTORED", "RANSOMWARE BOT NEUTRALIZED • NETWORK SECURE", GREEN
        title_font = pygame.font.SysFont("segoeui", 25, bold=True)
        timg = title_font.render(title, True, color)
        simg = cinematic_subtitle_font.render(sub, True, WHITE)
        surface.blit(timg, (center_screen.centerx - timg.get_width()//2, center_screen.y + 37))
        surface.blit(simg, (center_screen.centerx - simg.get_width()//2, center_screen.y + 78))

        # Approved Option B replaces the old circular/sphere centerpiece.
        # It fades in during restoration and remains behind the celebrating player.
        if t >= 265:
            shield_strength = clamp((t - 265) / 70.0, 0.0, 1.0)
            draw_victory_shield_hologram(surface, (480, 300), t, shield_strength)
            if t < 330:
                draw_cinematic_player_native(surface, 480, 432, "up", "idle", 0)
            else:
                draw_cinematic_player_native(surface, 480, 432, "down", "celebrate", (t // 7) % 2)

        # Side confetti cannons after restoration.
        if t >= 330:
            colors = [GREEN, CYAN, YELLOW, ORANGE, PURPLE, PINK, WHITE]
            for side in (-1, 1):
                origin_x = 72 if side < 0 else 888
                for i in range(28):
                    age = (t - 330 + i * 5) % 145
                    vx = (2.2 + (i % 5) * 0.45) * (1 if side < 0 else -1)
                    x = int(origin_x + vx * age)
                    y = int(390 - (3.2 + (i % 4) * 0.35) * age + 0.022 * age * age)
                    if 55 < x < 905 and 90 < y < 500:
                        pygame.draw.rect(surface, colors[i % len(colors)], (x, y, 5 + i % 3, 3 + (i+1) % 3))

        if t >= 390:
            prompt = cinematic_prompt_font.render("R  •  PLAY AGAIN", True, YELLOW)
            pbox = pygame.Rect(WINDOW_WIDTH//2 - prompt.get_width()//2 - 28, 500, prompt.get_width() + 56, 34)
            draw_alpha_panel(surface, pbox, (3, 10, 18), 238, border=GREEN, border_width=1, radius=12)
            surface.blit(prompt, (WINDOW_WIDTH//2 - prompt.get_width()//2, 504))

    else:
        if t < 50:
            stage = "entry"
        elif t < 115:
            stage = "wake"
        elif t < 185:
            stage = "override"
        elif t < 250:
            stage = "encrypt"
        else:
            stage = "lost"

        corruption = clamp((t - 42) / 185.0, 0.0, 1.0)
        center_screen, module_centers = draw_modern_command_room(surface, "defeat", t, 0.0, corruption)

        if t < 50:
            p = t / 50.0
            draw_cinematic_player_native(surface, 480, int(548 - p * 116), "up", "walk", (t // 7) % 2)
        elif t < 185:
            draw_cinematic_player_native(surface, 480, 432, "up", "idle", 0)
        elif t < 250:
            draw_cinematic_player_native(surface, 480 + int(math.sin(t * 0.2) * 7), 437, "down", "idle", 0)
        else:
            draw_cinematic_player_native(surface, 480, 445, "down", "defeated", 0)

        if t < 50:
            draw_modern_ransomware_bot(surface, (480, 276), t, 0.55, 0.0, 0.15)
        elif t < 115:
            wake = (t - 50) / 65.0
            draw_modern_ransomware_bot(surface, (480, 276), t, 0.55 + 0.45*wake, 0.0, wake)
        else:
            draw_modern_ransomware_bot(surface, (480, 276), t, 1.0, 0.0, 1.0)

        failed = 0 if t < 105 else min(6, 1 + (t - 105)//11)
        for i, pos in enumerate(module_centers):
            if i >= failed:
                continue
            pygame.draw.circle(surface, RED, pos, 20, 2)
            pygame.draw.line(surface, RED, (pos[0]-12, pos[1]-12), (pos[0]+12, pos[1]+12), 3)
            pygame.draw.line(surface, RED, (pos[0]+12, pos[1]-12), (pos[0]-12, pos[1]+12), 3)

        if 160 <= t < 260:
            p = (t - 160) / 100.0
            y = int(135 + p * 330)
            pygame.draw.line(surface, RED, (60, y), (900, y), 4)
            pygame.draw.line(surface, (136, 23, 42), (85, y + 10), (875, y + 10), 2)

        if stage == "entry":
            title, sub = "SECURITY TOOLKIT INCOMPLETE", "ALL SIX RECOVERY TOOLS ARE REQUIRED"
        elif stage == "wake":
            title, sub = "RANSOMWARE BOT ONLINE", "MALWARE HAS DETECTED THE ANALYST"
        elif stage == "override":
            title, sub = "COMMAND SYSTEM OVERRIDE", "SECURITY MODULES ARE BEING DISABLED"
        elif stage == "encrypt":
            title, sub = "ENCRYPTION ACTIVE", "FILES • SERVICES • BACKUPS ARE BEING LOCKED"
        else:
            title, sub = "SYSTEM ENCRYPTED", "RANSOMWARE CONTROL ESTABLISHED"
        title_font = pygame.font.SysFont("segoeui", 25, bold=True)
        timg = title_font.render(title, True, RED)
        simg = cinematic_subtitle_font.render(sub, True, WHITE)
        surface.blit(timg, (center_screen.centerx - timg.get_width()//2, center_screen.y + 37))
        surface.blit(simg, (center_screen.centerx - simg.get_width()//2, center_screen.y + 78))

        if t >= 105:
            for i in range(26):
                x = 70 + ((i * 97 + t * (2 + i % 2)) % 820)
                y = 120 + ((i * 41 + t) % 320)
                if (i + t//8) % 3 == 0:
                    pygame.draw.rect(surface, RED if i % 2 else ORANGE, (x, y, 4 + i % 4, 2))

        if t >= 315:
            message = cinematic_subtitle_font.render("SECURITY RESPONSE FAILED • REQUIRED TOOLS MISSING", True, GRAY)
            surface.blit(message, (WINDOW_WIDTH//2 - message.get_width()//2, 470))
            prompt = cinematic_prompt_font.render("R  •  TRY AGAIN", True, YELLOW)
            pbox = pygame.Rect(WINDOW_WIDTH//2 - prompt.get_width()//2 - 28, 500, prompt.get_width() + 56, 34)
            draw_alpha_panel(surface, pbox, (3, 10, 18), 238, border=RED, border_width=1, radius=12)
            surface.blit(prompt, (WINDOW_WIDTH//2 - prompt.get_width()//2, 504))

def draw_transition_overlay(surface):
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
    global interaction_message, message_timer, result_timer

    running = True
    blink_timer = 0
    show_prompt = True

    while running:
        frame_counter += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    toggle_mute()
                    continue

                if game_state == "title":
                    if event.key == pygame.K_RETURN:
                        play_sound("ui_click")
                        reset_game()

                elif game_state == "game":
                    if event.key == pygame.K_ESCAPE:
                        play_sound("ui_click")
                        game_state = "title"
                    elif event.key == pygame.K_e and not transition_active:
                        handle_interaction()

                elif game_state in ("victory", "defeat"):
                    if event.key == pygame.K_ESCAPE:
                        play_sound("ui_click")
                        game_state = "title"
                    elif event.key == pygame.K_r:
                        ready = result_timer >= 390 if game_state == "victory" else result_timer >= 315
                        if ready and not transition_active:
                            play_sound("ui_click")
                            reset_game()

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
            player_x = clamp(player_x + move_x, PLAY_MIN_X, PLAY_MAX_X)
            player_y = clamp(player_y + move_y, PLAY_MIN_Y, PLAY_MAX_Y)

            if is_walking:
                walk_timer += 1
                if walk_timer >= 9:
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

        if game_state in ("victory", "defeat"):
            result_timer += 1

        # ------------------------------
        # LOW-RESOLUTION PIXEL ART LAYER
        # ------------------------------

        if game_state == "title":
            blink_timer += 1
            if blink_timer >= 30:
                show_prompt = not show_prompt
                blink_timer = 0
            draw_title_screen(canvas, show_prompt)

        elif game_state == "game":
            draw_game_screen(canvas)

        elif game_state in ("victory", "defeat"):
            # The final encounter is rendered natively at 960x540 below.
            canvas.fill(BACKGROUND)

        scaled_canvas = pygame.transform.scale(canvas, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Regular-room canvas stays perfectly stable. The native finale handles
        # its own visual intensity without shaking the readable UI.
        shake_x = 0
        shake_y = 0

        screen.fill(BACKGROUND)
        screen.blit(scaled_canvas, (shake_x, shake_y))

        # ------------------------------
        # CRISP NATIVE-RESOLUTION LAYERING
        # ------------------------------

        if game_state == "title":
            draw_title_hud(screen, show_prompt)
        elif game_state == "game":
            # Architectural text is drawn first; player is a separate pixel layer on top.
            draw_world_door_labels(screen)
            draw_character_screen_layer(screen)
            draw_game_hud(screen)
        elif game_state in ("victory", "defeat"):
            draw_modern_finale_native(screen, game_state, result_timer)

        # Fade always renders last, including the final Control Room transition.
        draw_transition_overlay(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
