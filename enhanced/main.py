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

# Player position inside the room.
player_x = 95
player_y = 91

# Player movement settings.
player_speed = 1
player_direction = "down"

# Walking animation.
walk_frame = 0
walk_timer = 0
is_walking = False

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
    """Draw the pixel-art cybersecurity analyst."""

    # Character palette
    skin = (232, 184, 145)
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

    # --------------------------------------------------
    # SHADOW
    # --------------------------------------------------

    pygame.draw.rect(
        surface,
        (10, 13, 21),
        (x + 4, y + 29, 15, 2)
    )

    # --------------------------------------------------
    # EARS
    # --------------------------------------------------

    pygame.draw.rect(
        surface,
        skin_shadow,
        (x + 3, y + 7, 2, 4)
    )

    pygame.draw.rect(
        surface,
        skin_shadow,
        (x + 17, y + 7, 2, 4)
    )

    # --------------------------------------------------
    # FACE
    # --------------------------------------------------

    pygame.draw.rect(
        surface,
        skin,
        (x + 5, y + 4, 12, 11)
    )

    # Face shadow
    pygame.draw.rect(
        surface,
        skin_shadow,
        (x + 5, y + 13, 12, 2)
    )

    # Small face highlight
    pygame.draw.rect(
        surface,
        (244, 199, 158),
        (x + 6, y + 5, 3, 2)
    )

    # --------------------------------------------------
    # HAIR
    # --------------------------------------------------

    # Main top shape
    pygame.draw.rect(
        surface,
        hair,
        (x + 5, y, 11, 2)
    )

    pygame.draw.rect(
        surface,
        hair,
        (x + 3, y + 2, 15, 3)
    )

    # Left side
    pygame.draw.rect(
        surface,
        hair,
        (x + 3, y + 4, 3, 5)
    )

    # Right side
    pygame.draw.rect(
        surface,
        hair,
        (x + 16, y + 4, 3, 4)
    )

    # Uneven fringe so the hair does not look like a helmet
    pygame.draw.rect(
        surface,
        hair,
        (x + 6, y + 4, 4, 2)
    )

    pygame.draw.rect(
        surface,
        hair,
        (x + 13, y + 4, 3, 1)
    )

    # Hair highlights
    pygame.draw.rect(
        surface,
        hair_light,
        (x + 6, y + 1, 4, 1)
    )

    pygame.draw.rect(
        surface,
        hair_light,
        (x + 4, y + 3, 3, 1)
    )

    # --------------------------------------------------
    # FACE DETAILS
    # --------------------------------------------------

    # Eyebrows
    pygame.draw.rect(
        surface,
        hair,
        (x + 7, y + 7, 2, 1)
    )

    pygame.draw.rect(
        surface,
        hair,
        (x + 13, y + 7, 2, 1)
    )

    # Eyes
    pygame.draw.rect(
        surface,
        eye,
        (x + 7, y + 8, 2, 2)
    )

    pygame.draw.rect(
        surface,
        eye,
        (x + 13, y + 8, 2, 2)
    )

    # Eye highlights
    pygame.draw.rect(
        surface,
        WHITE,
        (x + 7, y + 8, 1, 1)
    )

    pygame.draw.rect(
        surface,
        WHITE,
        (x + 13, y + 8, 1, 1)
    )

    # Nose
    pygame.draw.rect(
        surface,
        skin_shadow,
        (x + 10, y + 10, 2, 2)
    )

    # Mouth
    pygame.draw.rect(
        surface,
        (116, 65, 58),
        (x + 9, y + 13, 4, 1)
    )

    # --------------------------------------------------
    # NECK
    # --------------------------------------------------

    pygame.draw.rect(
        surface,
        skin_shadow,
        (x + 9, y + 15, 4, 2)
    )

    # --------------------------------------------------
    # HOODIE
    # --------------------------------------------------

    # Shoulders / hood
    pygame.draw.rect(
        surface,
        hoodie_light,
        (x + 3, y + 16, 16, 3)
    )

    # Torso
    pygame.draw.rect(
        surface,
        hoodie,
        (x + 4, y + 18, 14, 8)
    )

    # Hoodie edge highlights
    pygame.draw.rect(
        surface,
        hoodie_light,
        (x + 4, y + 18, 2, 7)
    )

    pygame.draw.rect(
        surface,
        hoodie_light,
        (x + 16, y + 18, 2, 7)
    )

    # Shirt visible underneath
    pygame.draw.rect(
        surface,
        shirt,
        (x + 9, y + 18, 4, 6)
    )

    pygame.draw.rect(
        surface,
        shirt_dark,
        (x + 10, y + 20, 2, 3)
    )

    # Hoodie drawstrings
    pygame.draw.rect(
        surface,
        WHITE,
        (x + 8, y + 18, 1, 3)
    )

    pygame.draw.rect(
        surface,
        WHITE,
        (x + 13, y + 18, 1, 3)
    )

    # --------------------------------------------------
    # ARMS
    # --------------------------------------------------

    pygame.draw.rect(
        surface,
        hoodie,
        (x + 1, y + 18, 3, 7)
    )

    pygame.draw.rect(
        surface,
        hoodie,
        (x + 18, y + 18, 3, 7)
    )

    # Cuffs
    pygame.draw.rect(
        surface,
        hoodie_light,
        (x + 1, y + 23, 3, 2)
    )

    pygame.draw.rect(
        surface,
        hoodie_light,
        (x + 18, y + 23, 3, 2)
    )

    # Hands
    pygame.draw.rect(
        surface,
        skin,
        (x + 1, y + 25, 3, 2)
    )

    pygame.draw.rect(
        surface,
        skin,
        (x + 18, y + 25, 3, 2)
    )

    # --------------------------------------------------
    # CYBERSECURITY BADGE
    # --------------------------------------------------

    pygame.draw.rect(
        surface,
        CYAN,
        (x + 14, y + 20, 3, 4)
    )

    pygame.draw.rect(
        surface,
        GREEN,
        (x + 15, y + 21, 1, 1)
    )

    # --------------------------------------------------
    # PANTS
    # --------------------------------------------------

    pygame.draw.rect(
        surface,
        pants,
        (x + 6, y + 26, 5, 4)
    )

    pygame.draw.rect(
        surface,
        pants,
        (x + 12, y + 26, 5, 4)
    )

    # --------------------------------------------------
    # SHOES
    # --------------------------------------------------

    pygame.draw.rect(
        surface,
        shoes,
        (x + 5, y + 29, 6, 2)
    )

    pygame.draw.rect(
        surface,
        shoes,
        (x + 12, y + 29, 6, 2)
    )

    # Light pixels on shoes
    pygame.draw.rect(
        surface,
        WHITE,
        (x + 6, y + 29, 2, 1)
    )

    pygame.draw.rect(
        surface,
        WHITE,
        (x + 13, y + 29, 2, 1)
    )


def draw_lobby_scene(surface, player_x, player_y):
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
    draw_player(surface, player_x, player_y)


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

    draw_lobby_scene(surface, player_x, player_y)
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

    # --------------------------------------------------
    # EVENTS
    # --------------------------------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            # Start game from title screen.
            if game_state == "title":
                if event.key == pygame.K_RETURN:
                    game_state = "game"

            # Return to title screen.
            elif game_state == "game":
                if event.key == pygame.K_ESCAPE:
                    game_state = "title"

    # --------------------------------------------------
    # PLAYER MOVEMENT
    # --------------------------------------------------

    if game_state == "game":

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

        player_x += move_x
        player_y += move_y

        # Keep player inside the visible Main Lobby.
        player_x = max(18, min(player_x, 177))
        player_y = max(68, min(player_y, 94))

        # Walking animation timer.
        if is_walking:
            walk_timer += 1

            if walk_timer >= 10:
                walk_frame = 1 - walk_frame
                walk_timer = 0

        else:
            walk_frame = 0
            walk_timer = 0

    # --------------------------------------------------
    # TITLE SCREEN
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
    # GAME SCREEN
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

    # Draw readable HUD text after scaling.
    if game_state == "game":
        draw_hud_text(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()