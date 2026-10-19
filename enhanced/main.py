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

CYAN = (54, 238, 255)
GREEN = (78, 255, 132)
WHITE = (240, 240, 240)
GRAY = (135, 145, 165)

PINK = (255, 73, 173)
YELLOW = (255, 222, 89)
RED = (255, 77, 77)

# --------------------------------------------------
# TITLE SCREEN FONTS
# These are intentionally pixelated.
# --------------------------------------------------

title_font = pygame.font.Font(None, 42)
subtitle_font = pygame.font.Font(None, 22)
small_pixel_font = pygame.font.Font(None, 14)

# --------------------------------------------------
# HIGH-RESOLUTION HUD FONTS
# These are rendered after scaling for readability.
# --------------------------------------------------

hud_heading_font = pygame.font.SysFont("consolas", 27, bold=True)
hud_body_font = pygame.font.SysFont("consolas", 18)
hud_body_bold = pygame.font.SysFont("consolas", 18, bold=True)
hud_small_font = pygame.font.SysFont("consolas", 16, bold=True)
hud_status_font = pygame.font.SysFont("consolas", 20, bold=True)
hud_inventory_font = pygame.font.SysFont("consolas", 17, bold=True)

# --------------------------------------------------
# GAME DATA
# --------------------------------------------------

game_state = "title"

current_room = "Main Lobby"
inventory = []

rooms = {
    "Main Lobby": {
        "description": [
            "Emergency lights flicker.",
            "Building under attack.",
            "Find all 6 security tools."
        ],
        "north": "Control Room",
        "west": "Security Office"
    }
}

# --------------------------------------------------
# PIXEL ART
# --------------------------------------------------


def draw_pixel_lock(surface, x, y):
    """Draw a simple pixel-style cybersecurity lock."""

    pygame.draw.rect(surface, YELLOW, (x, y + 8, 24, 20))
    pygame.draw.rect(surface, BACKGROUND, (x + 9, y + 15, 6, 8))

    pygame.draw.rect(surface, YELLOW, (x + 5, y + 2, 14, 4))
    pygame.draw.rect(surface, YELLOW, (x + 3, y + 4, 4, 8))
    pygame.draw.rect(surface, YELLOW, (x + 17, y + 4, 4, 8))


def draw_player(surface, x, y):
    """Draw a temporary pixel cybersecurity analyst."""

    # Head
    pygame.draw.rect(surface, WHITE, (x + 4, y, 8, 7))

    # Hair
    pygame.draw.rect(surface, DARK_BLUE, (x + 3, y, 10, 3))

    # Body
    pygame.draw.rect(surface, CYAN, (x + 2, y + 7, 12, 10))

    # Equipment
    pygame.draw.rect(surface, PANEL_BLUE, (x + 5, y + 9, 6, 5))
    pygame.draw.rect(surface, GREEN, (x + 7, y + 10, 2, 2))

    # Legs
    pygame.draw.rect(surface, WHITE, (x + 3, y + 17, 4, 6))
    pygame.draw.rect(surface, WHITE, (x + 9, y + 17, 4, 6))


def draw_lobby_scene(surface):
    """Draw the pixel-art Main Lobby."""

    # Room area
    pygame.draw.rect(surface, (18, 22, 34), (12, 35, 190, 94))

    # Wall
    pygame.draw.rect(surface, (31, 41, 58), (16, 39, 182, 58))

    # Floor
    pygame.draw.rect(surface, (24, 29, 42), (16, 97, 182, 28))

    # Floor tiles
    for x in range(16, 198, 22):
        pygame.draw.line(
            surface,
            (40, 48, 66),
            (x, 97),
            (x, 125)
        )

    pygame.draw.line(
        surface,
        (40, 48, 66),
        (16, 111),
        (198, 111)
    )

    # Control Room doorway
    pygame.draw.rect(surface, (8, 10, 18), (82, 54, 48, 43))
    pygame.draw.rect(surface, CYAN, (82, 54, 48, 3))


    # Security terminal
    pygame.draw.rect(surface, (10, 14, 22), (25, 65, 28, 22))
    pygame.draw.rect(surface, CYAN, (29, 69, 20, 11))
    pygame.draw.rect(surface, GREEN, (31, 71, 5, 2))
    pygame.draw.rect(surface, GREEN, (31, 75, 12, 2))

    # Warning light
    pygame.draw.rect(surface, RED, (166, 48, 12, 6))
    pygame.draw.rect(surface, (100, 30, 30), (163, 54, 18, 2))

    # Player
    draw_player(surface, 99, 92)


# --------------------------------------------------
# TITLE SCREEN
# --------------------------------------------------


def draw_title_screen(surface, show_prompt):
    """Draw the retro title screen."""

    surface.fill(BACKGROUND)

    pygame.draw.rect(surface, CYAN, (8, 8, 304, 164), 2)
    pygame.draw.rect(surface, DARK_BLUE, (12, 12, 296, 156), 2)

    pygame.draw.rect(surface, PINK, (22, 30, 55, 3))
    pygame.draw.rect(surface, PINK, (243, 30, 55, 3))

    draw_pixel_lock(surface, 148, 20)

    title_1 = title_font.render(
        "CYBERSECURITY",
        False,
        CYAN
    )

    title_2 = title_font.render(
        "ATTACK",
        False,
        PINK
    )

    surface.blit(
        title_1,
        (
            BASE_WIDTH // 2 - title_1.get_width() // 2,
            58
        )
    )

    surface.blit(
        title_2,
        (
            BASE_WIDTH // 2 - title_2.get_width() // 2,
            88
        )
    )

    subtitle = subtitle_font.render(
        "TEXT ADVENTURE",
        False,
        WHITE
    )

    surface.blit(
        subtitle,
        (
            BASE_WIDTH // 2 - subtitle.get_width() // 2,
            121
        )
    )

    if show_prompt:
        prompt = small_pixel_font.render(
            "PRESS ENTER TO START",
            False,
            GREEN
        )

        surface.blit(
            prompt,
            (
                BASE_WIDTH // 2 - prompt.get_width() // 2,
                148
            )
        )


# --------------------------------------------------
# GAME SCREEN PIXEL ELEMENTS
# --------------------------------------------------


def draw_inventory_boxes(surface):
    """Draw inventory panel and empty item slots."""

    pygame.draw.rect(
        surface,
        PANEL_BLUE,
        (8, 139, 304, 33)
    )

    pygame.draw.rect(
        surface,
        CYAN,
        (8, 139, 304, 33),
        1
    )

    start_x = 72

    for index in range(6):
        slot_x = start_x + index * 38

        pygame.draw.rect(
            surface,
            (12, 16, 28),
            (slot_x, 144, 33, 20)
        )

        pygame.draw.rect(
            surface,
            GRAY,
            (slot_x, 144, 33, 20),
            1
        )


def draw_room_panel(surface):
    """Draw the mission information panel."""

    pygame.draw.rect(
        surface,
        PANEL_BLUE,
        (208, 35, 104, 94)
    )

    pygame.draw.rect(
        surface,
        CYAN,
        (208, 35, 104, 94),
        1
    )


def draw_game_screen(surface):
    """Draw pixel artwork for the current room."""

    surface.fill(BACKGROUND)

    # Outer border
    pygame.draw.rect(
        surface,
        CYAN,
        (5, 5, 310, 170),
        2
    )

    # Header
    pygame.draw.rect(
        surface,
        DARK_BLUE,
        (8, 8, 304, 22)
    )

    # Pixel room title
    room_font = pygame.font.Font(None, 26)

    room_name = room_font.render(
        current_room.upper(),
        False,
        CYAN
    )

    surface.blit(
        room_name,
        (14, 11)
    )

    draw_lobby_scene(surface)
    draw_room_panel(surface)
    draw_inventory_boxes(surface)


# --------------------------------------------------
# HIGH-RESOLUTION TEXT
# --------------------------------------------------


def draw_hud_text(surface):
    """Draw readable text on top of the pixel artwork."""

    # Control Room door label
    control_label = hud_small_font.render(
        "CONTROL",
        True,
        RED
    )

    door_center_x = 318

    surface.blit(
        control_label,
        (
        door_center_x - control_label.get_width() // 2,
        185
        )
    )
    
    # System status
    status = hud_status_font.render(
        "SYSTEM: COMPROMISED",
        True,
        RED
    )

    surface.blit(
        status,
        (
            925 - status.get_width(),
            47
        )
    )

    # Mission heading
    heading = hud_heading_font.render(
        "MISSION STATUS",
        True,
        YELLOW
    )

    surface.blit(
        heading,
        (650, 132)
    )

    # Mission description
    room = rooms[current_room]

    y = 185

    for line in room["description"]:
        text = hud_body_font.render(
            line,
            True,
            WHITE
        )

        surface.blit(
            text,
            (650, y)
        )

        y += 31

    # Exits heading
    exits_heading = hud_heading_font.render(
        "EXITS",
        True,
        GREEN
    )

    surface.blit(
        exits_heading,
        (650, 288)
    )

    north_text = hud_body_bold.render(
        "NORTH: Control Room",
        True,
        WHITE
    )

    west_text = hud_body_bold.render(
        "WEST : Security Office",
        True,
        WHITE
    )

    surface.blit(
        north_text,
        (650, 330)
    )

    surface.blit(
        west_text,
        (650, 360)
    )

    # Movement hint
    controls = hud_small_font.render(
        "ARROW KEYS / WASD TO MOVE",
        True,
        GRAY
    )

    surface.blit(
        controls,
        (
            WINDOW_WIDTH // 2 - controls.get_width() // 2,
            389
        )
    )

    # Inventory heading
    inventory_heading = hud_heading_font.render(
        "INVENTORY",
        True,
        YELLOW
    )

    surface.blit(
        inventory_heading,
        (39, 441)
    )

    # Inventory labels
    labels = [
        "MFA",
        "FW",
        "PATCH",
        "BACKUP",
        "ENC",
        "CARD"
    ]

    start_x = 216

    for index, label in enumerate(labels):
        slot_center_x = start_x + index * 114 + 49

        text = hud_inventory_font.render(
            label,
            True,
            GRAY
        )

        surface.blit(
            text,
            (
                slot_center_x - text.get_width() // 2,
                460
            )
        )


# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

running = True

blink_timer = 0
show_prompt = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == "title":

                if event.key == pygame.K_RETURN:
                    game_state = "game"

            elif game_state == "game":

                if event.key == pygame.K_ESCAPE:
                    game_state = "title"

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    if game_state == "title":

        blink_timer += 1

        if blink_timer >= 30:
            show_prompt = not show_prompt
            blink_timer = 0

        draw_title_screen(
            canvas,
            show_prompt
        )

    # --------------------------------------------------
    # GAME
    # --------------------------------------------------

    elif game_state == "game":

        draw_game_screen(canvas)

    # --------------------------------------------------
    # SCALE PIXEL GRAPHICS
    # --------------------------------------------------

    scaled_canvas = pygame.transform.scale(
        canvas,
        (WINDOW_WIDTH, WINDOW_HEIGHT)
    )

    screen.blit(
        scaled_canvas,
        (0, 0)
    )

    # Draw readable HUD text AFTER scaling.
    if game_state == "game":
        draw_hud_text(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()