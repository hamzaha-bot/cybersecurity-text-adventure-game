"""High-resolution animated Control Room endings for the enhanced game."""

import math
import pygame


INK = (5, 11, 24)
WALL = (10, 23, 43)
STEEL = (24, 48, 72)
CYAN = (67, 235, 255)
WHITE = (225, 250, 255)
RED = (255, 48, 75)
GREEN = (82, 255, 178)
GOLD = (255, 213, 105)


def _glow(surface, color, center, radius, alpha=38):
    """Paint a soft, bounded halo behind an important light source."""
    halo = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
    origin = (radius * 2, radius * 2)
    for scale, opacity in ((1.0, int(alpha * 0.25)),
                           (0.63, int(alpha * 0.55)), (0.28, alpha)):
        r = max(1, int(radius * scale))
        tint = tuple(int(channel * opacity / 255) for channel in color)
        pygame.draw.circle(halo, (*tint, opacity), origin, r)
    surface.blit(halo, (int(center[0] - radius * 2), int(center[1] - radius * 2)),
                 special_flags=pygame.BLEND_RGBA_ADD)


def _label(surface, font, text, pos, color, shadow=True):
    if shadow:
        surface.blit(font.render(text, True, (0, 0, 0)), (pos[0] + 2, pos[1] + 2))
    surface.blit(font.render(text, True, color), pos)


def _panel(surface, rect, accent, fill=(7, 17, 34), width=2):
    rect = pygame.Rect(rect)
    pygame.draw.rect(surface, fill, rect, border_radius=5)
    pygame.draw.rect(surface, (*accent, 65), rect.inflate(8, 8), 1, border_radius=8)
    pygame.draw.rect(surface, accent, rect, width, border_radius=5)
    x, y, w, h = rect
    for px, py, sx, sy in ((x, y, 1, 1), (x + w, y, -1, 1),
                           (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        pygame.draw.line(surface, WHITE, (px + sx * 3, py + sy * 11),
                         (px + sx * 3, py + sy * 3), 1)


def _draw_room(surface, won, tick):
    """Layer a deep, cinematic command deck with converging perspective."""
    alarm = (math.sin(tick * 0.15) + 1) / 2
    danger = (255, int(26 + 15 * alarm), int(49 + 22 * alarm))
    accent = GREEN if won else danger
    surface.fill((4, 10, 22))

    # The curved command-deck ceiling and rear bulkhead.
    pygame.draw.polygon(surface, (8, 22, 44),
                        [(0, 65), (118, 20), (842, 20), (960, 65), (960, 313), (0, 313)])
    pygame.draw.polygon(surface, (14, 36, 61),
                        [(0, 67), (115, 30), (845, 30), (960, 67), (960, 101), (0, 101)])
    for x in (62, 206, 352, 608, 754, 898):
        pygame.draw.line(surface, (25, 64, 91), (x, 44), (x, 295), 2)
        pygame.draw.line(surface, (12, 34, 57), (x + 7, 47), (x + 7, 292), 1)
        pygame.draw.circle(surface, CYAN if won else danger, (x + 3, 83), 3)
        pygame.draw.circle(surface, (18, 52, 77), (x + 3, 83), 8, 1)
    pygame.draw.line(surface, (61, 161, 194), (24, 102), (936, 102), 2)
    pygame.draw.line(surface, (21, 76, 111), (24, 107), (936, 107), 1)

    # Overhead strips and red rotating alert beacons.
    for x in (90, 276, 684, 870):
        pygame.draw.polygon(surface, (28, 62, 86), [(x, 46), (x + 78, 46),
                                                   (x + 66, 56), (x + 12, 56)])
        pygame.draw.line(surface, accent, (x + 13, 57), (x + 64, 57), 3)
    for x in (35, 128, 832, 925):
        pulse = int(135 + 110 * alarm)
        lamp = danger if not won else (49, 190 + int(55 * alarm), 163)
        _glow(surface, lamp, (x, 120), 28, 24 + int(28 * alarm))
        pygame.draw.ellipse(surface, (55, 75, 99), (x - 18, 110, 36, 17))
        pygame.draw.ellipse(surface, lamp, (x - 12, 111, 24, 10))
        pygame.draw.line(surface, (255, pulse, pulse), (x - 7, 113), (x + 5, 113), 2)

    # Wall terminal bank: individual animated charts, warning indicators,
    # frame bevels and teal glass.
    _panel(surface, (172, 119, 616, 104), accent, (5, 13, 28), 3)
    pygame.draw.rect(surface, (9, 34, 54), (185, 132, 590, 72), border_radius=3)
    # Thin telemetry traces sit beneath the crisp status lettering.
    for i in range(40):
        x = 190 + (i * 97) % 572
        y = 126 + (i * 41) % 74
        col = accent if i % 5 == 0 else (21, 77, 98)
        pygame.draw.line(surface, col, (x, y), (x + 8 + i % 13, y), 1)
    if won:
        _label(surface, pygame.font.SysFont("consolas", 23, bold=True),
               "SYSTEM RESTORED", (375, 136), GREEN)
        _label(surface, pygame.font.SysFont("consolas", 13, bold=True),
               "NETWORK SECURE  /  ENCRYPTION KEYS REVOKED", (299, 164), WHITE)
    else:
        _label(surface, pygame.font.SysFont("consolas", 23, bold=True),
               "SYSTEM ENCRYPTED", (377, 136), danger)
        _label(surface, pygame.font.SysFont("consolas", 13, bold=True),
               "RANSOMWARE CONTROL ESTABLISHED  /  NETWORK LOCKED", (278, 164), WHITE)
    for i, (name, stat) in enumerate((("FIREWALL", "ONLINE" if won else "BREACHED"),
                                      ("BACKUPS", "RESTORED" if won else "LOCKED"),
                                      ("ACCESS", "SECURE" if won else "DENIED"))):
        bx = 222 + i * 188
        col = GREEN if won else danger
        pygame.draw.rect(surface, (6, 19, 31), (bx, 186, 169, 26), border_radius=2)
        pygame.draw.circle(surface, col, (bx + 12, 199), 4)
        _label(surface, pygame.font.SysFont("consolas", 11, bold=True),
               f"{name}  /  {stat}", (bx + 23, 192), col, False)

    # Side equipment cabinets with vents, screen faces, tiny buttons and glass.
    for x in (24, 88, 814, 878):
        pygame.draw.rect(surface, (14, 29, 47), (x, 152, 48, 171), border_radius=3)
        pygame.draw.rect(surface, (36, 63, 83), (x, 152, 48, 171), 2, border_radius=3)
        pygame.draw.rect(surface, (3, 10, 21), (x + 7, 162, 34, 42), border_radius=2)
        pygame.draw.rect(surface, (18, 47, 62), (x + 10, 165, 28, 34), border_radius=1)
        pygame.draw.line(surface, accent, (x + 12, 188 + (tick // 6 + x) % 9),
                         (x + 33, 180 + (tick // 6 + x) % 9), 2)
        pygame.draw.rect(surface, (31, 48, 66), (x + 7, 214, 34, 78), border_radius=2)
        for row in range(7):
            vy = 222 + row * 9
            pygame.draw.line(surface, (71, 93, 111), (x + 12, vy), (x + 35, vy), 2)
            color = (GREEN, CYAN, danger)[(row + x // 64 + tick // 14) % 3]
            pygame.draw.circle(surface, color, (x + 14, vy + 4), 2)
            pygame.draw.circle(surface, (31, 109, 139), (x + 34, vy + 4), 2)
        pygame.draw.rect(surface, (4, 12, 23), (x + 3, 304, 42, 7))
        pygame.draw.line(surface, accent, (x + 8, 307), (x + 39, 307), 1)

    # The central core sits inside a layered containment portal.
    core_center = (480, 307)
    core_color = (45, 255, 226) if won else (255, 38, 61)
    _glow(surface, core_color, core_center, 100, 33 if won else int(34 + alarm * 22))
    for ring, phase in ((82, 0), (69, 1.8), (54, 3.7)):
        rect = pygame.Rect(0, 0, ring * 2, ring * 2)
        rect.center = core_center
        arc_color = GREEN if won and phase == 1.8 else core_color
        pygame.draw.arc(surface, arc_color, rect, tick * .025 + phase,
                        tick * .025 + phase + 4.7, 3 if ring == 82 else 2)
        for side in range(6):
            a = tick * .02 * (1 if side % 2 == 0 else -1) + side * math.tau / 6
            p = (int(core_center[0] + ring * math.cos(a)),
                 int(core_center[1] + ring * math.sin(a)))
            pygame.draw.circle(surface, WHITE if side == 0 else arc_color, p, 3 if ring == 82 else 2)
    pygame.draw.circle(surface, (6, 22, 40), core_center, 38)
    pygame.draw.circle(surface, core_color, core_center, 33, 2)
    pygame.draw.circle(surface, core_color, core_center, 22, 2)
    pygame.draw.circle(surface, (217, 255, 255), core_center, 11)
    pygame.draw.circle(surface, core_color, core_center, 7)
    for spoke in range(8):
        a = tick * .008 + spoke * math.tau / 8
        start = (int(core_center[0] + 17 * math.cos(a)),
                 int(core_center[1] + 17 * math.sin(a)))
        end = (int(core_center[0] + 29 * math.cos(a)),
               int(core_center[1] + 29 * math.sin(a)))
        pygame.draw.line(surface, WHITE if won else RED, start, end, 2)

    # Symmetrical operator consoles in the foreground planes.
    for side in (-1, 1):
        points = ([(12, 266), (166, 275), (215, 349), (0, 362)] if side < 0 else
                  [(948, 266), (794, 275), (745, 349), (960, 362)])
        pygame.draw.polygon(surface, (12, 25, 42), points)
        pygame.draw.lines(surface, (38, 108, 139), True, points, 2)
        pygame.draw.polygon(surface, (16, 49, 68),
                            ([(20, 278), (156, 284), (187, 318), (14, 324)] if side < 0 else
                             [(940, 278), (804, 284), (773, 318), (946, 324)]))
        for j in range(4):
            cx = (42 + j * 34) if side < 0 else (918 - j * 34)
            screenrect = (cx - 12, 283 + j * 4, 23, 16)
            pygame.draw.rect(surface, (2, 10, 22), screenrect, border_radius=2)
            pygame.draw.rect(surface, accent, screenrect, 1, border_radius=2)
            pygame.draw.line(surface, CYAN, (cx - 8, 291 + j * 4),
                             (cx + 8, 288 + j * 4), 1)
            for led in range(3):
                pygame.draw.circle(surface, (GREEN, GOLD, danger)[(led + j + tick // 15) % 3],
                                   (cx - 7 + led * 7, 305 + j * 3), 2)
            pygame.draw.line(surface, (65, 88, 105), (cx - 8, 316 + j * 3),
                             (cx + 8, 319 + j * 3), 2)

    # Perspective floor panels converge on the portal; reflections sit on top.
    pygame.draw.polygon(surface, (8, 18, 33), [(0, 339), (260, 293), (700, 293),
                                                (960, 339), (960, 540), (0, 540)])
    pygame.draw.polygon(surface, (13, 29, 48), [(0, 348), (280, 309), (680, 309),
                                                 (960, 348), (960, 540), (0, 540)])
    pygame.draw.line(surface, accent, (0, 347), (268, 309), 3)
    pygame.draw.line(surface, accent, (960, 347), (692, 309), 3)
    for i in range(13):
        x = i * 80
        pygame.draw.line(surface, (29, 52, 73), (480, 314), (x, 539), 1)
    for y in (353, 372, 397, 430, 473, 529):
        taper = (y - 309) * .36
        pygame.draw.line(surface, (24, 48, 69),
                         (int(480 - taper), y), (int(480 + taper), y), 1)
    # Cyan/green and alarm-red specular streaks reflected across the polished deck.
    refl = (24, 192, 177) if won else (160, 26, 45)
    for i in range(10):
        offset = (tick * (2 if i % 2 else -1) + i * 71) % 168
        y = 346 + offset
        spread = 18 + (y - 346) // 4
        x = 480 + (1 if i % 2 else -1) * spread
        pygame.draw.line(surface, (*refl,), (x, y), (x + (1 if i % 2 else -1) * 31, y + 1),
                         1 if i % 3 else 2)

    # Repaint the portal's base and lower hardware over the floor reflection.
    pygame.draw.ellipse(surface, (8, 38, 55), (394, 337, 172, 24))
    pygame.draw.ellipse(surface, accent, (400, 339, 160, 12), 2)
    for x in range(414, 555, 20):
        pygame.draw.line(surface, CYAN if (x // 20 + tick // 9) % 2 else accent,
                         (x, 343), (x + 7, 343), 2)

    # Return the portal's core and orbit above the deck plane so its complete
    # silhouette reads as a holographic restoration reactor, not a half-ring.
    for ring, phase in ((82, 0), (69, 1.8), (54, 3.7)):
        rect = pygame.Rect(0, 0, ring * 2, ring * 2)
        rect.center = core_center
        arc_color = GREEN if won and phase == 1.8 else core_color
        pygame.draw.arc(surface, arc_color, rect, tick * .025 + phase,
                        tick * .025 + phase + 4.7, 3 if ring == 82 else 2)
        for side in range(6):
            a = tick * .02 * (1 if side % 2 == 0 else -1) + side * math.tau / 6
            point = (int(core_center[0] + ring * math.cos(a)),
                     int(core_center[1] + ring * math.sin(a)))
            pygame.draw.circle(surface, WHITE if side == 0 else arc_color, point,
                               3 if ring == 82 else 2)
    pygame.draw.circle(surface, (7, 27, 43), core_center, 33)
    pygame.draw.circle(surface, core_color, core_center, 33, 2)
    pygame.draw.circle(surface, core_color, core_center, 22, 2)
    pygame.draw.circle(surface, (206, 255, 250), core_center, 11)
    pygame.draw.circle(surface, core_color, core_center, 7)


def _draw_bot(surface, won, tick, phase):
    """A plated, articulated ransomware machine, falling apart on victory."""
    enemy = (255, 58, 76)
    cyan = (82, 225, 255)
    center_x = 480
    if won:
        fall = min(44, phase * 0.36)
        shake = int(math.sin(tick * .7) * max(0, 6 - phase * .08))
    else:
        fall = 0
        shake = int(math.sin(tick * .5) * 3)
    cx = center_x + shake
    cy = int(280 + fall)
    _glow(surface, enemy if not won else cyan, (cx, cy), 75, 25)
    if won and phase > 125:
        # Floating armor fragments disperse, then fade naturally.
        for i in range(12):
            angle = i * math.tau / 12 + tick * .015
            dist = 52 + min(75, phase * .27) + (i * 9) % 24
            px = int(cx + math.cos(angle) * dist)
            py = int(cy + math.sin(angle) * dist)
            color = (enemy[0], max(35, enemy[1] - i * 8), 68) if i % 2 else (96, 230, 247)
            pygame.draw.polygon(surface, color, [(px, py), (px + 9, py + 3), (px + 4, py + 12)])
            pygame.draw.circle(surface, GOLD, (px + 2, py + 2), 1)
    if won and phase > 175:
        # At the peak of the restoration burst only scattered armor remains.
        return

    # Legs, hydraulic joints and shadow.
    pygame.draw.ellipse(surface, (1, 7, 14), (cx - 59, 327 + int(fall), 118, 20))
    for side in (-1, 1):
        knee = (cx + side * 23, cy + 40)
        foot = (cx + side * 40, cy + 60)
        pygame.draw.line(surface, (46, 60, 80), (cx + side * 15, cy + 16), knee, 15)
        pygame.draw.line(surface, enemy, (cx + side * 15, cy + 16), knee, 3)
        pygame.draw.circle(surface, (168, 61, 72), knee, 8)
        pygame.draw.circle(surface, (30, 43, 59), knee, 4)
        pygame.draw.line(surface, (52, 73, 90), knee, foot, 10)
        pygame.draw.line(surface, (124, 145, 153), knee, foot, 2)
        pygame.draw.polygon(surface, (31, 47, 62),
                            [(foot[0] - 13, foot[1] - 3), (foot[0] + 14, foot[1] - 3),
                             (foot[0] + 19, foot[1] + 8), (foot[0] - 10, foot[1] + 8)])
        pygame.draw.line(surface, enemy, (foot[0] - 8, foot[1] + 5),
                         (foot[0] + 14, foot[1] + 5), 2)

    # Torso with overlapping armor, beveled edges, bolts and central lock.
    pygame.draw.polygon(surface, (30, 44, 62),
                        [(cx - 43, cy - 22), (cx - 25, cy - 43), (cx + 25, cy - 43),
                         (cx + 43, cy - 22), (cx + 36, cy + 19), (cx + 20, cy + 31),
                         (cx - 20, cy + 31), (cx - 36, cy + 19)])
    pygame.draw.polygon(surface, (108, 124, 137),
                        [(cx - 43, cy - 22), (cx - 25, cy - 43), (cx - 14, cy - 38),
                         (cx - 19, cy + 9), (cx - 36, cy + 19)])
    pygame.draw.lines(surface, (190, 204, 212), False,
                      [(cx - 43, cy - 22), (cx - 25, cy - 43), (cx + 25, cy - 43),
                       (cx + 43, cy - 22)], 2)
    pygame.draw.polygon(surface, (18, 28, 44),
                        [(cx - 17, cy - 29), (cx + 17, cy - 29),
                         (cx + 22, cy + 11), (cx, cy + 22), (cx - 22, cy + 11)])
    pygame.draw.circle(surface, enemy if not won else cyan, (cx, cy - 7), 17)
    pygame.draw.circle(surface, (12, 20, 32), (cx, cy - 7), 12)
    pygame.draw.rect(surface, enemy if not won else cyan, (cx - 10, cy - 10, 20, 13), 2, border_radius=3)
    pygame.draw.arc(surface, enemy if not won else cyan,
                    pygame.Rect(cx - 7, cy - 19, 14, 17), math.pi, math.tau, 2)
    pygame.draw.circle(surface, WHITE, (cx, cy - 5), 2)
    for side in (-1, 1):
        shoulder = (cx + side * 44, cy - 18)
        elbow = (cx + side * 68, cy + 2 + int(math.sin(tick * .16 + side) * 5))
        hand = (cx + side * 76, cy + 26 + int(math.sin(tick * .19 + side) * 7))
        pygame.draw.line(surface, (42, 56, 73), shoulder, elbow, 15)
        pygame.draw.line(surface, (136, 149, 157), shoulder, elbow, 3)
        pygame.draw.circle(surface, enemy, shoulder, 11, 3)
        pygame.draw.circle(surface, (145, 158, 165), elbow, 9)
        pygame.draw.line(surface, enemy, elbow, hand, 7)
        for finger in (-1, 0, 1):
            pygame.draw.line(surface, (174, 188, 194), hand,
                             (hand[0] + side * 5, hand[1] + 10 + finger * 5), 2)
        pygame.draw.circle(surface, enemy, (cx + side * 55, cy + 1), 5)

    # Head, brow, jaw and animated scanning eyes.
    pygame.draw.polygon(surface, (39, 54, 71),
                        [(cx - 31, cy - 54), (cx - 20, cy - 75), (cx + 18, cy - 75),
                         (cx + 31, cy - 54), (cx + 25, cy - 38), (cx - 25, cy - 38)])
    pygame.draw.lines(surface, (177, 192, 199), False,
                      [(cx - 31, cy - 54), (cx - 20, cy - 75), (cx + 18, cy - 75),
                       (cx + 31, cy - 54)], 2)
    visor = (enemy if not won else cyan)
    pygame.draw.polygon(surface, (4, 9, 18),
                        [(cx - 23, cy - 59), (cx - 15, cy - 68),
                         (cx + 15, cy - 68), (cx + 23, cy - 59),
                         (cx + 18, cy - 52), (cx - 18, cy - 52)])
    _glow(surface, visor, (cx, cy - 60), 17, 48)
    pygame.draw.line(surface, visor, (cx - 15, cy - 59), (cx - 4, cy - 59), 4)
    pygame.draw.line(surface, visor, (cx + 4, cy - 59), (cx + 15, cy - 59), 4)
    pygame.draw.polygon(surface, (12, 17, 28),
                        [(cx - 11, cy - 50), (cx + 11, cy - 50),
                         (cx + 6, cy - 42), (cx - 6, cy - 42)])
    for x in (-25, 25):
        pygame.draw.circle(surface, (213, 220, 224), (cx + x, cy - 48), 3)


def _draw_analyst(surface, won, tick, phase):
    """Back-facing analyst with a clean tapered French crop and expressive pose."""
    x, floor_y = 480, 451
    if won:
        # A relieved rise from the crouch; upright settles into a quiet salute.
        crouch = max(0, 1 - min(phase, 150) / 150)
        raise_body = int(crouch * 13)
        lean = int(crouch * 5)
        y = floor_y - raise_body
    else:
        # Defeated, folded shoulders and dropped arms. Keep the French crop visible.
        recoil = 1 if tick % 104 < 31 and tick % 12 < 6 else 0
        lean = 9 + recoil * 3
        y = floor_y + 10 + recoil * 2
    bob = int(math.sin(tick * .09) * 2) if won and phase > 145 else 0
    y += bob
    _glow(surface, (20, 188, 202) if won else (221, 28, 48), (x, y - 35), 38, 18)
    pygame.draw.ellipse(surface, (2, 6, 13), (x - 34, y + 1, 68, 11))

    # Consistent compact legs, illuminated boot soles.
    pygame.draw.polygon(surface, (20, 31, 47),
                        [(x - 19, y - 39), (x - 1, y - 37), (x - 4, y - 6),
                         (x - 22, y - 6)])
    pygame.draw.polygon(surface, (25, 39, 57),
                        [(x + 1, y - 37), (x + 19, y - 39), (x + 22, y - 6),
                         (x + 4, y - 6)])
    for side in (-1, 1):
        pygame.draw.ellipse(surface, (18, 27, 41), (x + side * 21 - 6, y - 9, 22, 12))
        pygame.draw.line(surface, CYAN if won else (107, 46, 57),
                         (x + side * 21 - 2, y - 1), (x + side * 21 + 11, y - 1), 2)

    # Backpack silhouette and hood fall behind shoulder line.
    pygame.draw.polygon(surface, (24, 38, 56),
                        [(x - 17, y - 78), (x - 22, y - 70), (x - 20, y - 48),
                         (x - 14, y - 41), (x + 14, y - 41), (x + 20, y - 48),
                         (x + 22, y - 70), (x + 17, y - 78)])
    pygame.draw.polygon(surface, (47, 67, 89),
                        [(x - 14, y - 76), (x, y - 71), (x + 14, y - 76),
                         (x + 18, y - 51), (x, y - 45), (x - 18, y - 51)])
    pygame.draw.line(surface, (83, 116, 139), (x - 13, y - 73), (x - 9, y - 51), 2)
    pygame.draw.line(surface, (83, 116, 139), (x + 13, y - 73), (x + 9, y - 51), 2)
    pygame.draw.rect(surface, CYAN if won else (177, 44, 60),
                     (x - 8, y - 62, 16, 11), 2, border_radius=3)
    pygame.draw.circle(surface, WHITE if won else (245, 95, 105), (x, y - 57), 2)

    # Jacket panels, realistic shoulder shape and arms.
    pygame.draw.polygon(surface, (29, 44, 62),
                        [(x - 17, y - 79), (x - 29, y - 68 + lean),
                         (x - 21, y - 47 + lean), (x - 13, y - 44),
                         (x + 13, y - 44), (x + 21, y - 47 + lean),
                         (x + 29, y - 68 + lean), (x + 17, y - 79)])
    pygame.draw.line(surface, (83, 111, 133), (x - 13, y - 77), (x - 20, y - 53), 2)
    pygame.draw.line(surface, (83, 111, 133), (x + 13, y - 77), (x + 20, y - 53), 2)
    pygame.draw.polygon(surface, (16, 33, 47),
                        [(x - 5, y - 75), (x, y - 69), (x + 5, y - 75),
                         (x + 4, y - 53), (x, y - 49), (x - 4, y - 53)])
    # Shoulder tabs and a luminous SECURITY insignia.
    for side in (-1, 1):
        pygame.draw.rect(surface, (51, 73, 93), (x + side * 22 - 3, y - 69 + lean, 7, 4))
        pygame.draw.line(surface, CYAN if won else (181, 54, 69),
                         (x + side * 25, y - 64 + lean),
                         (x + side * 25, y - 57 + lean), 2)
    pygame.draw.circle(surface, (45, 221, 210) if won else (207, 63, 76),
                       (x, y - 61), 4, 1)
    pygame.draw.line(surface, WHITE if won else RED, (x - 2, y - 61), (x + 2, y - 61), 1)

    for side in (-1, 1):
        shoulder = (x + side * 25, y - 65 + lean)
        wrist = (x + side * 30, y - 40 + lean)
        if won and phase > 145 and side == 1:
            wrist = (x + 21, y - 104)
        elif not won:
            wrist = (x + side * 31, y - 35 + lean)
        pygame.draw.line(surface, (30, 45, 64), shoulder, wrist, 10)
        pygame.draw.line(surface, (78, 105, 126), shoulder, wrist, 2)
        pygame.draw.circle(surface, (213, 174, 139), wrist, 4)

    # A fitted tapered French crop viewed from behind: tidy fade at nape/temples,
    # layered textured crown and short broken fringe along the hairline.
    head_y = y - 103
    pygame.draw.rect(surface, (168, 120, 91), (x - 8, head_y + 18, 16, 10))
    pygame.draw.rect(surface, (204, 151, 112), (x - 10, head_y + 20, 20, 5))
    pygame.draw.polygon(surface, (46, 34, 29),
                        [(x - 14, head_y + 16), (x - 14, head_y + 7),
                         (x - 10, head_y + 1), (x - 4, head_y - 2),
                         (x + 5, head_y - 2), (x + 12, head_y + 2),
                         (x + 15, head_y + 10), (x + 14, head_y + 17),
                         (x + 9, head_y + 17), (x + 7, head_y + 12),
                         (x - 7, head_y + 12), (x - 10, head_y + 18)])
    pygame.draw.polygon(surface, (86, 58, 42),
                        [(x - 11, head_y + 3), (x - 4, head_y - 1),
                         (x + 4, head_y - 1), (x + 10, head_y + 3),
                         (x + 8, head_y + 9), (x - 8, head_y + 9)])
    # Fine strands and a distinct textured crop, not a flat block of hair.
    for dx, dy in ((-7, 1), (-3, -1), (1, -2), (5, 0), (8, 3),
                   (-9, 4), (-4, 3), (2, 2), (6, 4), (-6, 6), (0, 5)):
        pygame.draw.line(surface, (133, 88, 57), (x + dx, head_y + dy),
                         (x + dx + 2, head_y + dy - 1), 1)
    pygame.draw.line(surface, (161, 113, 71), (x - 6, head_y + 1), (x - 2, head_y), 1)
    pygame.draw.line(surface, (34, 27, 26), (x - 13, head_y + 13), (x + 13, head_y + 13), 2)


def _draw_particles(surface, won, tick, phase):
    """Deterministic pixel debris, sparks and celebration confetti."""
    for i in range(34):
        seed_x = (i * 181 + 73) % 960
        seed_y = (i * 97 + 31) % 520
        speed = 1 + i % 4
        x = (seed_x + (tick * speed * (1 if i % 2 else -1))) % 960
        y = (seed_y + tick * speed) % 520
        if 235 < x < 725 and 220 < y < 370 and i % 3:
            continue
        if won:
            colors = (CYAN, GREEN, WHITE, GOLD, (111, 196, 255))
            color = colors[(i + tick // 16) % len(colors)]
            pygame.draw.rect(surface, color, (int(x), int(y), 4 if i % 4 else 6, 3))
            if i % 7 == 0:
                pygame.draw.line(surface, color, (int(x), int(y)), (int(x + 4), int(y - 7)), 1)
        else:
            color = (RED if i % 3 else (255, 117, 126))
            pygame.draw.rect(surface, color, (int(x), int(y), 2 + i % 4, 2))
            if i % 5 == 0:
                pygame.draw.line(surface, (115, 31, 53), (int(x), int(y + 3)),
                                 (int(x + 13), int(y + 3)), 1)
    if not won and tick % 104 < 31:
        # A timed electrical lash makes the attack legible before the
        # takeover is permanent, then discharges across the analyst's station.
        jitter = math.sin(tick * 0.8) * 13
        bolt = [(551, 307), (535, 328), (551, 338), (518, 358),
                (535, 370), (490 + int(jitter), 398)]
        pygame.draw.lines(surface, (105, 23, 47), False, bolt, 9)
        pygame.draw.lines(surface, (255, 44, 70), False, bolt, 4)
        pygame.draw.lines(surface, (255, 204, 197), False, bolt, 1)
        _glow(surface, RED, bolt[-1], 28, 58)
        pygame.draw.circle(surface, (255, 83, 92), bolt[-1], 8, 2)


def draw_result_scene(surface, won, tick, missing_items=6):
    """Paint an animated, full-resolution ending while leaving game logic intact."""
    tick = int(tick)
    phase = min(tick, 360)
    _draw_room(surface, won, tick)
    _draw_particles(surface, won, tick, phase)
    _draw_bot(surface, won, tick, phase)
    _draw_analyst(surface, won, tick, phase)
    if not won and tick % 104 < 31:
        # Put the live attack in the foreground so its impact reads clearly
        # against the analyst's silhouette instead of disappearing behind it.
        jitter = math.sin(tick * 0.8) * 13
        bolt = [(552, 305), (535, 327), (551, 339), (518, 358),
                (535, 370), (490 + int(jitter), 399)]
        pygame.draw.lines(surface, (73, 19, 41), False, bolt, 9)
        pygame.draw.lines(surface, (255, 49, 74), False, bolt, 4)
        pygame.draw.lines(surface, (255, 210, 207), False, bolt, 1)
        pygame.draw.circle(surface, (255, 62, 82), bolt[-1], 9, 2)

    # High-resolution, readable mission typography and fixed restart cue.
    sub = pygame.font.SysFont("consolas", 15, bold=True)
    tiny = pygame.font.SysFont("consolas", 12, bold=True)
    accent = GREEN if won else (255, 64, 81)
    header = "CONTROL ROOM  /  VICTORY" if won else "CONTROL ROOM  /  LOSS  ·  TOOLS MISSING"
    _panel(surface, (18, 16, 442 if won else 478, 32), accent, (4, 13, 27), 2)
    _label(surface, sub, header, (32, 25), accent)

    # Tool verification rails flank the reactor, echoing the supplied concept.
    for side in (-1, 1):
        px = 33 if side < 0 else 759
        _panel(surface, (px, 227, 169, 95), GREEN if won else (92, 52, 68),
               (5, 14, 29), 1)
        for row, label in enumerate(("FIREWALL", "SEC PATCH", "MFA TOKEN", "BACKUP CORE")):
            yy = 238 + row * 19
            ok = won
            col = GREEN if ok else (255, 73, 88)
            pygame.draw.rect(surface, (11, 24, 39), (px + 9, yy, 10, 10), border_radius=2)
            pygame.draw.rect(surface, col, (px + 9, yy, 10, 10), 1, border_radius=2)
            if ok:
                pygame.draw.lines(surface, col, False,
                                  [(px + 11, yy + 5), (px + 13, yy + 8), (px + 17, yy + 2)], 2)
            else:
                pygame.draw.line(surface, col, (px + 11, yy + 2), (px + 17, yy + 8), 2)
                pygame.draw.line(surface, col, (px + 17, yy + 2), (px + 11, yy + 8), 2)
            _label(surface, tiny, label, (px + 26, yy), WHITE, False)
            _label(surface, tiny, "ONLINE" if ok else "LOCKED",
                   (px + 108, yy), col, False)

    # Lower mission transcript is crisply overlaid at native 960×540 resolution.
    message = "All systems restored — ransomware threat neutralized." if won else \
        f"Security response failed — {missing_items} recovery tools missing."
    msg_font = pygame.font.SysFont("consolas", 14, bold=True)
    msg = msg_font.render(message, True, WHITE)
    pygame.draw.rect(surface, (4, 10, 21), (480 - msg.get_width() // 2 - 15, 462,
                                             msg.get_width() + 30, 26), border_radius=4)
    pygame.draw.line(surface, accent, (349, 462), (611, 462), 1)
    surface.blit(msg, msg.get_rect(center=(480, 475)))

    prompt = pygame.font.SysFont("consolas", 21, bold=True)
    button = prompt.render("R  ·  PLAY AGAIN" if won else "R  ·  TRY AGAIN", True, GOLD)
    _panel(surface, (369, 493, 222, 35), GOLD, (5, 12, 24), 2)
    surface.blit(button, button.get_rect(center=(480, 511)))
