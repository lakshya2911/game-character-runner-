import pygame
import random
import math

pygame.init()

# ============================================================
# WINDOW
# ============================================================

WIDTH = 1200
HEIGHT = 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Naruto Dragon Runner")

clock = pygame.time.Clock()

# ============================================================
# COLORS
# ============================================================

WHITE = (255, 255, 255)
BLACK = (8, 8, 12)

SKIN = (218, 158, 115)
SKIN_LIGHT = (238, 185, 140)
SKIN_DARK = (155, 95, 65)

HAIR = (245, 190, 35)
HAIR_LIGHT = (255, 215, 65)

ORANGE = (235, 95, 20)
ORANGE_LIGHT = (255, 125, 30)
ORANGE_DARK = (170, 55, 15)

NAVY = (25, 40, 70)
NAVY_LIGHT = (45, 65, 105)

# Black clothing shades
CLOTHES_DARK = (8, 8, 10)
CLOTHES = (22, 22, 26)
CLOTHES_LIGHT = (42, 42, 48)

BLUE_EYE = (45, 150, 230)

RED = (190, 35, 40)
RED_LIGHT = (240, 60, 55)

METAL = (130, 135, 145)
METAL_LIGHT = (190, 195, 205)

DRAGON_RED = (125, 25, 25)
DRAGON_DARK = (50, 12, 15)
DRAGON_LIGHT = (185, 45, 40)

FIRE = (255, 100, 15)
FIRE_YELLOW = (255, 220, 50)

GROUND = (35, 40, 43)
GRASS = (35, 65, 45)

# ============================================================
# FONTS
# ============================================================

FONT_BIG = pygame.font.SysFont(
    "arial",
    62,
    bold=True
)

FONT_MEDIUM = pygame.font.SysFont(
    "arial",
    32,
    bold=True
)

FONT_SMALL = pygame.font.SysFont(
    "arial",
    22,
    bold=True
)

FONT_LEVEL = pygame.font.SysFont(
    "arial",
    40,
    bold=True
)

# ============================================================
# GAME VARIABLES
# ============================================================

GROUND_Y = 570

player_x = 180
player_width = 70
player_height = 150

player_y = GROUND_Y - player_height

velocity_y = 0
gravity = 0.8
jump_strength = -18

on_ground = True

score = 0
best_score = 0

level = 1

game_speed = 7

started = False
game_over = False

frame_count = 0

spawn_timer = 0

dragons = []
particles = []

# ============================================================
# LEVEL UP VARIABLES
# ============================================================

level_up_timer = 0

old_level = 1

# ============================================================
# PARALLAX VARIABLES
# ============================================================

mountain_offset = 0
far_mountain_offset = 0
castle_offset = 0
forest_offset = 0
battlefield_offset = 0

# ============================================================
# STARS
# ============================================================

stars = []

for i in range(160):

    stars.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(20, 420),
        "size": random.randint(1, 3),
        "brightness": random.randint(120, 255)
    })

# ============================================================
# CLOUDS
# ============================================================

clouds = []

for i in range(8):

    clouds.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(80, 300),
        "size": random.randint(50, 100)
    })

# ============================================================
# DRAGON
# ============================================================

def create_dragon():

    width = random.randint(70, 95)
    height = random.randint(50, 75)

    dragon = {
        "x": WIDTH + random.randint(80, 250),
        "y": GROUND_Y - height,
        "w": width,
        "h": height,
        "wing_phase": random.uniform(
            0,
            math.pi * 2
        ),
        "passed": False
    }

    dragons.append(dragon)

# ============================================================
# PARTICLES
# ============================================================

def create_fire_particle(x, y):

    particles.append({
        "x": x,
        "y": y,
        "vx": random.uniform(-5, -1),
        "vy": random.uniform(-1.5, 1.5),
        "life": random.randint(15, 30),
        "type": "fire"
    })


def create_dust_particle(x, y):

    particles.append({
        "x": x,
        "y": y,
        "vx": random.uniform(-2, 2),
        "vy": random.uniform(-2, 0),
        "life": random.randint(15, 25),
        "type": "dust"
    })


def create_hit_particle(x, y):

    particles.append({
        "x": x,
        "y": y,
        "vx": random.uniform(-5, 5),
        "vy": random.uniform(-5, 2),
        "life": random.randint(15, 30),
        "type": "hit"
    })

# ============================================================
# LEVEL CALCULATION
# ============================================================

def calculate_level():

    return (score // 10) + 1


def update_level():

    global level
    global level_up_timer
    global old_level

    new_level = calculate_level()

    if new_level > level:

        old_level = level

        level = new_level

        level_up_timer = 150

        # Small celebration particles
        for i in range(30):

            particles.append({
                "x": WIDTH // 2 + random.randint(-100, 100),
                "y": 230 + random.randint(-30, 30),
                "vx": random.uniform(-3, 3),
                "vy": random.uniform(-5, 1),
                "life": random.randint(30, 60),
                "type": "level"
            })

# ============================================================
# BACKGROUND
# ============================================================


# ============================================================
# DYNAMIC BACKGROUND STRUCTURES
# ============================================================

def draw_dynamic_mountains():
    """Draw mountains that move slowly and keep each mountain shape stable."""
    # Much slower parallax movement so the mountains feel far away.
    far_speed = 0.025
    near_speed = 0.055

    far_offset = -(frame_count * game_speed * far_speed) % 1100
    near_offset = -(frame_count * game_speed * near_speed) % 260

    # ------------------------------------------------------------
    # FAR MOUNTAINS
    # ------------------------------------------------------------
    far_width = 220
    far_start = int((-far_offset // far_width) - 2)

    points = []
    for i in range(far_start, far_start + 9):
        rng = random.Random(i * 1009 + level * 97)
        x = i * far_width + far_offset
        width = rng.randint(190, 270)
        height = rng.randint(75, 155)
        peak_x = x + width * rng.uniform(0.35, 0.65)
        points.append((int(x), 510))
        points.append((int(peak_x), 510 - height))
        points.append((int(x + width), 510))

    points.extend([(WIDTH, HEIGHT), (0, HEIGHT)])
    pygame.draw.polygon(screen, (16, 25, 42), points)

    # ------------------------------------------------------------
    # NEAR MOUNTAINS
    # ------------------------------------------------------------
    near_width = 260
    near_start = int((-near_offset // near_width) - 2)

    points = []
    for i in range(near_start, near_start + 8):
        rng = random.Random(i * 2027 + level * 211)
        x = i * near_width + near_offset
        width = rng.randint(220, 310)
        height = rng.randint(90, 175)
        peak_x = x + width * rng.uniform(0.30, 0.70)
        points.append((int(x), 530))
        points.append((int(peak_x), 530 - height))
        points.append((int(x + width), 530))

    points.extend([(WIDTH, HEIGHT), (0, HEIGHT)])
    pygame.draw.polygon(screen, (25, 38, 50), points)

    # Small fixed highlights so the mountains do not visually morph.
    for i in range(near_start, near_start + 8):
        rng = random.Random(i * 2027 + level * 211)
        x = i * near_width + near_offset
        width = rng.randint(220, 310)
        height = rng.randint(90, 175)
        peak_x = x + width * rng.uniform(0.30, 0.70)
        if rng.random() < 0.5:
            pygame.draw.line(
                screen,
                (65, 75, 82),
                (int(peak_x), int(530 - height)),
                (int(peak_x - width * 0.10), int(530 - height + height * 0.28)),
                2
            )

def draw_egyptian_buildings():
    """Ancient-Egyptian style buildings with changing size/shape/structure."""
    scroll = (frame_count * game_speed * 0.35) % 1500

    for i in range(-2, 12):
        base_x = i * 155 - scroll
        rng = random.Random(i * 1009 + level * 7919)

        width = rng.randint(90, 190)
        height = rng.randint(110, 235)
        x = int(base_x)
        bottom = GROUND_Y

        stone = rng.choice([
            (58, 52, 48),
            (68, 60, 52),
            (76, 66, 55),
            (50, 50, 55)
        ])

        # Main structure changes between tower, temple and stepped building.
        style = rng.randint(0, 3)

        if style == 0:
            # Tall temple tower
            pygame.draw.rect(screen, stone, (x, bottom - height, width, height))
            roof_h = rng.randint(25, 55)
            pygame.draw.polygon(
                screen,
                (38, 35, 34),
                [(x - 12, bottom - height),
                 (x + width // 2, bottom - height - roof_h),
                 (x + width + 12, bottom - height)]
            )

        elif style == 1:
            # Wide temple with sloped sides
            pygame.draw.polygon(
                screen,
                stone,
                [(x + 15, bottom),
                 (x + 25, bottom - height + 35),
                 (x + width - 25, bottom - height + 35),
                 (x + width - 10, bottom)]
            )
            pygame.draw.polygon(
                screen,
                (42, 38, 35),
                [(x + 5, bottom - height + 35),
                 (x + width // 2, bottom - height),
                 (x + width - 5, bottom - height + 35)]
            )

        elif style == 2:
            # Stepped structure
            steps = rng.randint(3, 5)
            step_h = max(18, height // steps)
            for s in range(steps):
                inset = s * 9
                pygame.draw.rect(
                    screen,
                    stone,
                    (
                        x + inset,
                        bottom - (s + 1) * step_h,
                        max(25, width - inset * 2),
                        step_h
                    )
                )

        else:
            # Palace-like building with uneven towers
            pygame.draw.rect(screen, stone, (x, bottom - height + 35, width, height - 35))
            tower_w = max(22, width // 5)
            tower_h = rng.randint(60, 125)
            pygame.draw.rect(screen, stone, (x - 5, bottom - tower_h, tower_w, tower_h))
            pygame.draw.rect(
                screen,
                stone,
                (x + width - tower_w + 5, bottom - tower_h, tower_w, tower_h)
            )

        # Columns
        column_count = rng.randint(2, 5)
        for c in range(column_count):
            cx = x + 18 + int((width - 36) * (c + 0.5) / column_count)
            column_h = rng.randint(45, min(105, max(50, height - 20)))
            pygame.draw.rect(
                screen,
                (105, 88, 67),
                (cx - 5, bottom - column_h, 10, column_h)
            )

        # Door and varied windows
        door_w = rng.randint(16, 30)
        door_h = rng.randint(35, 65)
        pygame.draw.rect(
            screen,
            (25, 23, 24),
            (x + width // 2 - door_w // 2, bottom - door_h, door_w, door_h)
        )

        for w in range(rng.randint(1, 4)):
            wx = x + 15 + rng.randint(0, max(1, width - 30))
            wy = bottom - rng.randint(max(50, height // 2), max(55, height - 25))
            pygame.draw.rect(screen, (190, 145, 55), (wx, wy, 9, 15))


def draw_battlefield_structures():
    """Ruined towers and walls with varied dimensions and shapes."""
    scroll = (frame_count * game_speed * 0.5) % 900

    for i in range(-2, 10):
        rng = random.Random(i * 1237 + level * 3571)
        x = int(i * 155 - scroll)
        w = rng.randint(45, 125)
        h = rng.randint(100, 230)
        style = rng.randint(0, 2)

        if style == 0:
            pygame.draw.rect(
                screen, (55, 48, 48),
                (x, GROUND_Y - h, w, h)
            )
            # Broken top
            pygame.draw.polygon(
                screen, (30, 25, 28),
                [(x - 8, GROUND_Y - h),
                 (x + w * 0.35, GROUND_Y - h - rng.randint(20, 50)),
                 (x + w * 0.62, GROUND_Y - h + 10),
                 (x + w + 8, GROUND_Y - h)]
            )

        elif style == 1:
            wall_h = rng.randint(70, 145)
            pygame.draw.rect(
                screen, (65, 55, 55),
                (x, GROUND_Y - wall_h, w + 70, wall_h)
            )
            # Missing section
            gap_x = x + rng.randint(15, max(16, w))
            pygame.draw.rect(
                screen, (25, 22, 25),
                (gap_x, GROUND_Y - wall_h, rng.randint(18, 45), wall_h // 2)
            )

        else:
            # Slanted ruined tower
            pygame.draw.polygon(
                screen, (48, 42, 44),
                [(x + 12, GROUND_Y),
                 (x + 25, GROUND_Y - h),
                 (x + w, GROUND_Y - h + 20),
                 (x + w - 15, GROUND_Y)]
            )



def draw_background():

    global far_mountain_offset
    global mountain_offset
    global castle_offset
    global forest_offset
    global battlefield_offset

    # ========================================================
    # DIFFERENT SKY FOR EACH LEVEL
    # ========================================================

    if level == 1:

        top_color = (5, 8, 25)
        bottom_color = (28, 40, 70)

    elif level == 2:

        top_color = (7, 10, 30)
        bottom_color = (35, 45, 65)

    elif level == 3:

        top_color = (5, 10, 18)
        bottom_color = (15, 35, 35)

    elif level == 4:

        top_color = (18, 7, 20)
        bottom_color = (50, 20, 25)

    else:

        top_color = (3, 3, 15)
        bottom_color = (18, 10, 35)

    # ========================================================
    # GRADIENT
    # ========================================================

    for y in range(HEIGHT):

        ratio = y / HEIGHT

        r = int(
            top_color[0]
            +
            (bottom_color[0] - top_color[0])
            * ratio
        )

        g = int(
            top_color[1]
            +
            (bottom_color[1] - top_color[1])
            * ratio
        )

        b = int(
            top_color[2]
            +
            (bottom_color[2] - top_color[2])
            * ratio
        )

        pygame.draw.line(
            screen,
            (r, g, b),
            (0, y),
            (WIDTH, y)
        )

    # ========================================================
    # STARS
    # ========================================================

    for star in stars:

        brightness = star["brightness"]

        pygame.draw.circle(
            screen,
            (
                brightness,
                brightness,
                brightness
            ),
            (
                star["x"],
                star["y"]
            ),
            star["size"]
        )

    # ========================================================
    # MOVING CLOUDS
    # ========================================================

    for cloud in clouds:

        cloud["x"] -= 0.25

        if cloud["x"] < -150:

            cloud["x"] = WIDTH + random.randint(
                50,
                200
            )

        size = cloud["size"]

        cloud_surface = pygame.Surface(
            (size * 2, size),
            pygame.SRCALPHA
        )

        pygame.draw.ellipse(
            cloud_surface,
            (120, 130, 150, 35),
            (0, 25, size, 35)
        )

        pygame.draw.ellipse(
            cloud_surface,
            (140, 145, 165, 30),
            (
                size * 0.5,
                10,
                size,
                40
            )
        )

        screen.blit(
            cloud_surface,
            (
                cloud["x"],
                cloud["y"]
            )
        )

    # ========================================================
    # MOON
    # ========================================================

    moon_x = 940
    moon_y = 130

    for radius in range(
        150,
        65,
        -10
    ):

        glow = pygame.Surface(
            (
                radius * 2,
                radius * 2
            ),
            pygame.SRCALPHA
        )

        alpha = int(
            5 +
            (150 - radius) * 0.4
        )

        pygame.draw.circle(
            glow,
            (
                255,
                245,
                210,
                alpha
            ),
            (
                radius,
                radius
            ),
            radius
        )

        screen.blit(
            glow,
            (
                moon_x - radius,
                moon_y - radius
            )
        )

    pygame.draw.circle(
        screen,
        (250, 245, 215),
        (
            moon_x,
            moon_y
        ),
        62
    )

    # Moon craters

    pygame.draw.circle(
        screen,
        (220, 215, 185),
        (915, 110),
        9
    )

    pygame.draw.circle(
        screen,
        (225, 220, 190),
        (955, 145),
        7
    )

    pygame.draw.circle(
        screen,
        (215, 210, 180),
        (950, 105),
        5
    )

    # ========================================================
    # DYNAMIC MOUNTAINS
    # ========================================================

    draw_dynamic_mountains()

    # ========================================================
    # LEVEL 1 - CHANGING ANCIENT EGYPTIAN BUILDINGS
    # ========================================================

    if level == 1:

        draw_egyptian_buildings()

    # ========================================================
    # LEVEL 2 - EXTRA MOVING MOUNTAIN DETAILS
    # ========================================================

    elif level == 2:

        # Add a second layer of irregular mountain peaks.
        scroll = (frame_count * game_speed * 0.28) % 1100

        for i in range(-2, 11):
            rng = random.Random(i * 271 + level * 911)
            x = int(i * 145 - scroll)
            width = rng.randint(90, 190)
            height = rng.randint(55, 130)

            pygame.draw.polygon(
                screen,
                (35, 45, 55),
                [
                    (x, 520),
                    (x + width // 2, 520 - height),
                    (x + width, 520)
                ]
            )

            if rng.random() < 0.6:
                pygame.draw.line(
                    screen,
                    (90, 95, 100),
                    (x + width // 2, 520 - height),
                    (x + width // 2 + rng.randint(10, 35), 520 - height // 2),
                    3
                )

    # ========================================================
    # LEVEL 3 - DARK FOREST
    # ========================================================

    elif level == 3:

        forest_offset -= game_speed * 0.6

        if forest_offset <= -180:

            forest_offset += 180

        for offset in [
            forest_offset,
            forest_offset + 180,
            forest_offset + 360,
            forest_offset + 540,
            forest_offset + 720,
            forest_offset + 900,
            forest_offset + 1080
        ]:

            tree_x = int(offset)

            # trunk
            pygame.draw.rect(
                screen,
                (30, 22, 20),
                (
                    tree_x,
                    350,
                    35,
                    220
                )
            )

            # leaves
            pygame.draw.circle(
                screen,
                (18, 45, 35),
                (
                    tree_x + 18,
                    340
                ),
                70
            )

            pygame.draw.circle(
                screen,
                (15, 38, 30),
                (
                    tree_x - 20,
                    380
                ),
                55
            )

            pygame.draw.circle(
                screen,
                (20, 50, 38),
                (
                    tree_x + 55,
                    380
                ),
                55
            )

    # ========================================================
    # LEVEL 4 - CHANGING BATTLEFIELD STRUCTURES
    # ========================================================

    elif level == 4:

        draw_battlefield_structures()

    # ========================================================
    # LEVEL 5+ - DARKER, CHANGING BATTLEFIELD
    # ========================================================

    else:

        draw_battlefield_structures()

# ============================================================
# GROUND
# ============================================================

def draw_ground():

    pygame.draw.rect(
        screen,
        GROUND,
        (
            0,
            GROUND_Y,
            WIDTH,
            HEIGHT - GROUND_Y
        )
    )

    pygame.draw.rect(
        screen,
        GRASS,
        (
            0,
            GROUND_Y,
            WIDTH,
            12
        )
    )

    offset = int(
        (
            frame_count *
            game_speed
        )
        % 100
    )

    for x in range(
        -100,
        WIDTH + 100,
        100
    ):

        pygame.draw.line(
            screen,
            (55, 60, 62),
            (
                x - offset,
                GROUND_Y + 45
            ),
            (
                x + 45 - offset,
                GROUND_Y + 45
            ),
            2
        )

# ============================================================
# NARUTO-STYLE CHARACTER
# ============================================================

def draw_naruto(x, y):

    run_phase = math.sin(
        frame_count * 0.28
    )

    arm_swing = run_phase * 18
    leg_swing = run_phase * 20

    # Shadow
    shadow = pygame.Surface(
        (110, 35),
        pygame.SRCALPHA
    )

    pygame.draw.ellipse(
        shadow,
        (0, 0, 0, 110),
        (5, 8, 90, 18)
    )

    screen.blit(
        shadow,
        (
            x - 15,
            GROUND_Y - 10
        )
    )

    # ========================================================
    # LEGS
    # ========================================================

    back_leg = leg_swing * 0.25
    front_leg = -leg_swing * 0.25

    pygame.draw.polygon(
        screen,
        CLOTHES_DARK,
        [
            (x + 26, y + 104),
            (x + 42, y + 104),
            (x + 27 + back_leg, y + 133),
            (x + 10 + back_leg, y + 143),
            (x + 14, y + 117)
        ]
    )

    pygame.draw.ellipse(
        screen,
        CLOTHES,
        (
            x + 4 + back_leg,
            y + 137,
            35,
            15
        )
    )

    pygame.draw.polygon(
        screen,
        CLOTHES,
        [
            (x + 37, y + 103),
            (x + 54, y + 103),
            (x + 55 + front_leg, y + 130),
            (x + 45 + front_leg, y + 143),
            (x + 28, y + 118)
        ]
    )

    pygame.draw.ellipse(
        screen,
        CLOTHES,
        (
            x + 35 + front_leg,
            y + 137,
            38,
            16
        )
    )

    # ========================================================
    # TORSO
    # ========================================================

    pygame.draw.polygon(
        screen,
        CLOTHES_DARK,
        [
            (x + 18, y + 62),
            (x + 51, y + 62),
            (x + 58, y + 108),
            (x + 17, y + 108)
        ]
    )

    pygame.draw.polygon(
        screen,
        CLOTHES,
        [
            (x + 24, y + 65),
            (x + 46, y + 65),
            (x + 50, y + 103),
            (x + 23, y + 103)
        ]
    )

    # Navy upper section
    pygame.draw.polygon(
        screen,
        CLOTHES,
        [
            (x + 27, y + 62),
            (x + 45, y + 62),
            (x + 47, y + 78),
            (x + 25, y + 78)
        ]
    )

    # Zipper
    pygame.draw.line(
        screen,
        (45, 45, 50),
        (
            x + 36,
            y + 76
        ),
        (
            x + 36,
            y + 103
        ),
        2
    )

    # Belt
    pygame.draw.rect(
        screen,
        CLOTHES,
        (
            x + 17,
            y + 100,
            42,
            9
        )
    )

    # ========================================================
    # ARMS
    # ========================================================

    back_arm = -arm_swing * 0.35
    front_arm = arm_swing * 0.35

    pygame.draw.polygon(
        screen,
        CLOTHES_DARK,
        [
            (x + 18, y + 65),
            (x + 9, y + 70),
            (x + 9 + back_arm, y + 103),
            (x + 19 + back_arm, y + 100),
            (x + 27, y + 80)
        ]
    )

    pygame.draw.circle(
        screen,
        SKIN,
        (
            int(x + 14 + back_arm),
            y + 108
        ),
        8
    )

    pygame.draw.polygon(
        screen,
        CLOTHES,
        [
            (x + 47, y + 66),
            (x + 58, y + 72),
            (x + 58 + front_arm, y + 100),
            (x + 48 + front_arm, y + 103),
            (x + 39, y + 80)
        ]
    )

    pygame.draw.polygon(
        screen,
        CLOTHES,
        [
            (x + 52 + front_arm, y + 97),
            (x + 61 + front_arm, y + 98),
            (x + 64 + front_arm, y + 114),
            (x + 55 + front_arm, y + 117)
        ]
    )

    pygame.draw.circle(
        screen,
        SKIN,
        (
            int(x + 60 + front_arm),
            y + 119
        ),
        8
    )

    # ========================================================
    # NECK
    # ========================================================

    pygame.draw.rect(
        screen,
        SKIN_DARK,
        (
            x + 28,
            y + 45,
            16,
            22
        )
    )

    # ========================================================
    # FACE
    # ========================================================

    pygame.draw.ellipse(
        screen,
        SKIN,
        (
            x + 16,
            y + 8,
            40,
            48
        )
    )

    pygame.draw.ellipse(
        screen,
        SKIN_LIGHT,
        (
            x + 22,
            y + 14,
            28,
            30
        )
    )

    pygame.draw.ellipse(
        screen,
        SKIN,
        (
            x + 50,
            y + 25,
            10,
            15
        )
    )

    # ========================================================
    # HAIR
    # ========================================================

    pygame.draw.ellipse(
        screen,
        HAIR,
        (
            x + 12,
            y + 1,
            47,
            32
        )
    )

    spikes = [

        [
            (x + 17, y + 18),
            (x + 5, y + 7),
            (x + 20, y + 10)
        ],

        [
            (x + 25, y + 13),
            (x + 18, y - 5),
            (x + 32, y + 7)
        ],

        [
            (x + 34, y + 10),
            (x + 35, y - 8),
            (x + 44, y + 8)
        ],

        [
            (x + 43, y + 11),
            (x + 52, y - 4),
            (x + 51, y + 18)
        ],

        [
            (x + 51, y + 18),
            (x + 64, y + 8),
            (x + 57, y + 29)
        ]
    ]

    for spike in spikes:

        pygame.draw.polygon(
            screen,
            HAIR,
            spike
        )

    # Hair highlights
    pygame.draw.line(
        screen,
        HAIR_LIGHT,
        (
            x + 23,
            y + 6
        ),
        (
            x + 19,
            y + 18
        ),
        2
    )

    pygame.draw.line(
        screen,
        HAIR_LIGHT,
        (
            x + 37,
            y + 4
        ),
        (
            x + 34,
            y + 17
        ),
        2
    )

    pygame.draw.line(
        screen,
        HAIR_LIGHT,
        (
            x + 50,
            y + 7
        ),
        (
            x + 47,
            y + 19
        ),
        2
    )

    # ========================================================
    # FOREHEAD PROTECTOR
    # ========================================================

    pygame.draw.rect(
        screen,
        NAVY,
        (
            x + 14,
            y + 21,
            44,
            9
        )
    )

    pygame.draw.rect(
        screen,
        METAL,
        (
            x + 27,
            y + 20,
            20,
            12
        ),
        border_radius=2
    )

    pygame.draw.line(
        screen,
        METAL_LIGHT,
        (
            x + 29,
            y + 22
        ),
        (
            x + 44,
            y + 22
        ),
        2
    )

    # Leaf-like symbol
    pygame.draw.arc(
        screen,
        NAVY,
        (
            x + 31,
            y + 22,
            10,
            7
        ),
        0,
        math.pi,
        2
    )

    pygame.draw.line(
        screen,
        CLOTHES,
        (
            x + 36,
            y + 25
        ),
        (
            x + 39,
            y + 28
        ),
        2
    )

    # ========================================================
    # EYES
    # ========================================================

    pygame.draw.ellipse(
        screen,
        WHITE,
        (
            x + 25,
            y + 34,
            10,
            6
        )
    )

    pygame.draw.circle(
        screen,
        BLUE_EYE,
        (
            x + 31,
            y + 37
        ),
        3
    )

    pygame.draw.ellipse(
        screen,
        WHITE,
        (
            x + 40,
            y + 34,
            10,
            6
        )
    )

    pygame.draw.circle(
        screen,
        BLUE_EYE,
        (
            x + 46,
            y + 37
        ),
        3
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            x + 31,
            y + 37
        ),
        1
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            x + 46,
            y + 37
        ),
        1
    )

    # Nose
    pygame.draw.line(
        screen,
        SKIN_DARK,
        (
            x + 38,
            y + 38
        ),
        (
            x + 36,
            y + 43
        ),
        1
    )

    # Mouth
    pygame.draw.line(
        screen,
        SKIN_DARK,
        (
            x + 33,
            y + 47
        ),
        (
            x + 44,
            y + 47
        ),
        2
    )

    # ========================================================
    # CHEEK MARKS
    # ========================================================

    for side in [-1, 1]:

        cheek_x = (
            x + 30
            if side == -1
            else x + 44
        )

        pygame.draw.line(
            screen,
            SKIN_DARK,
            (
                cheek_x,
                y + 43
            ),
            (
                cheek_x + side * 7,
                y + 45
            ),
            2
        )

        pygame.draw.line(
            screen,
            SKIN_DARK,
            (
                cheek_x,
                y + 47
            ),
            (
                cheek_x + side * 7,
                y + 49
            ),
            2
        )

    # ========================================================
    # SCARF
    # ========================================================

    scarf_wave = math.sin(
        frame_count * 0.2
    ) * 6

    pygame.draw.polygon(
        screen,
        RED,
        [
            (x + 16, y + 56),
            (x + 46, y + 56),
            (x + 50, y + 67),
            (x + 24, y + 67)
        ]
    )

    pygame.draw.polygon(
        screen,
        CLOTHES_LIGHT,
        [
            (x + 18, y + 58),
            (x - 18, y + 51 + scarf_wave),
            (x - 5, y + 63 + scarf_wave),
            (x + 24, y + 66)
        ]
    )

# ============================================================
# DRAGON
# ============================================================

def draw_dragon(dragon):

    x = dragon["x"]
    y = dragon["y"]

    w = dragon["w"]
    h = dragon["h"]

    wing_wave = math.sin(
        frame_count * 0.15 +
        dragon["wing_phase"]
    ) * 6

    # Tail
    pygame.draw.polygon(
        screen,
        DRAGON_DARK,
        [
            (x + w * 0.62, y + h * 0.65),
            (x + w, y + h * 0.82),
            (x + w * 0.72, y + h * 0.78),
            (x + w * 0.55, y + h * 0.7)
        ]
    )

    # Tail spike
    pygame.draw.polygon(
        screen,
        DRAGON_RED,
        [
            (x + w - 5, y + h * 0.82),
            (x + w + 12, y + h * 0.78),
            (x + w - 2, y + h * 0.9)
        ]
    )

    # Body
    pygame.draw.ellipse(
        screen,
        DRAGON_RED,
        (
            x + w * 0.25,
            y + h * 0.35,
            w * 0.55,
            h * 0.45
        )
    )

    # Belly
    pygame.draw.ellipse(
        screen,
        DRAGON_LIGHT,
        (
            x + w * 0.28,
            y + h * 0.48,
            w * 0.35,
            h * 0.22
        )
    )

    # Wing
    pygame.draw.polygon(
        screen,
        DRAGON_DARK,
        [
            (x + w * 0.48, y + h * 0.45),
            (x + w * 0.52, y - 20 + wing_wave),
            (x + w * 0.75, y + 8 + wing_wave),
            (x + w * 0.82, y + h * 0.55)
        ]
    )

    # Wing bones
    pygame.draw.line(
        screen,
        DRAGON_LIGHT,
        (
            x + w * 0.52,
            y + h * 0.48
        ),
        (
            x + w * 0.52,
            y + 5 + wing_wave
        ),
        2
    )

    pygame.draw.line(
        screen,
        DRAGON_LIGHT,
        (
            x + w * 0.53,
            y + h * 0.5
        ),
        (
            x + w * 0.72,
            y + 12 + wing_wave
        ),
        2
    )

    pygame.draw.line(
        screen,
        DRAGON_LIGHT,
        (
            x + w * 0.55,
            y + h * 0.5
        ),
        (
            x + w * 0.78,
            y + h * 0.4
        ),
        2
    )

    # Neck
    pygame.draw.polygon(
        screen,
        DRAGON_RED,
        [
            (x + w * 0.3, y + h * 0.55),
            (x + w * 0.08, y + h * 0.4),
            (x + w * 0.2, y + h * 0.25),
            (x + w * 0.4, y + h * 0.5)
        ]
    )

    # Head
    head_x = x + w * 0.08
    head_y = y + h * 0.2

    pygame.draw.ellipse(
        screen,
        DRAGON_RED,
        (
            head_x - 10,
            head_y,
            w * 0.35,
            h * 0.35
        )
    )

    # Snout
    pygame.draw.polygon(
        screen,
        DRAGON_RED,
        [
            (head_x + 2, head_y + 12),
            (head_x - 25, head_y + 22),
            (head_x + 4, head_y + 32)
        ]
    )

    # Horns
    pygame.draw.polygon(
        screen,
        (210, 190, 150),
        [
            (head_x + 5, head_y + 5),
            (head_x - 2, head_y - 15),
            (head_x + 13, head_y + 4)
        ]
    )

    pygame.draw.polygon(
        screen,
        (210, 190, 150),
        [
            (head_x + 17, head_y + 4),
            (head_x + 17, head_y - 17),
            (head_x + 25, head_y + 8)
        ]
    )

    # Eye
    pygame.draw.circle(
        screen,
        (255, 190, 30),
        (
            int(head_x + 5),
            int(head_y + 15)
        ),
        5
    )

    pygame.draw.circle(
        screen,
        BLACK,
        (
            int(head_x + 5),
            int(head_y + 15)
        ),
        2
    )

    # Teeth
    for i in range(3):

        tx = head_x - 9 + i * 7

        pygame.draw.polygon(
            screen,
            WHITE,
            [
                (tx, head_y + 28),
                (tx + 4, head_y + 28),
                (tx + 2, head_y + 36)
            ]
        )

    # Legs
    for leg_x in [
        x + w * 0.38,
        x + w * 0.58
    ]:

        pygame.draw.line(
            screen,
            DRAGON_DARK,
            (
                leg_x,
                y + h * 0.68
            ),
            (
                leg_x - 5,
                y + h * 0.9
            ),
            7
        )

    # Fire
    fire_x = head_x - 28
    fire_y = head_y + 23

    pygame.draw.polygon(
        screen,
        FIRE,
        [
            (fire_x, fire_y),
            (fire_x - 35, fire_y - 8),
            (fire_x - 20, fire_y),
            (fire_x - 42, fire_y + 8),
            (fire_x, fire_y + 10)
        ]
    )

    pygame.draw.polygon(
        screen,
        FIRE_YELLOW,
        [
            (fire_x, fire_y + 2),
            (fire_x - 25, fire_y),
            (fire_x - 8, fire_y + 7)
        ]
    )

    if random.random() < 0.25:

        create_fire_particle(
            fire_x - 20,
            fire_y + random.randint(-5, 5)
        )

# ============================================================
# PARTICLES
# ============================================================

def update_particles():

    for particle in particles[:]:

        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]

        particle["life"] -= 1

        if particle["type"] == "fire":

            pygame.draw.circle(
                screen,
                FIRE,
                (
                    int(particle["x"]),
                    int(particle["y"])
                ),
                4
            )

        elif particle["type"] == "dust":

            pygame.draw.circle(
                screen,
                (150, 150, 145),
                (
                    int(particle["x"]),
                    int(particle["y"])
                ),
                4
            )

        elif particle["type"] == "level":

            pygame.draw.circle(
                screen,
                (255, 210, 60),
                (
                    int(particle["x"]),
                    int(particle["y"])
                ),
                5
            )

        else:

            pygame.draw.circle(
                screen,
                RED_LIGHT,
                (
                    int(particle["x"]),
                    int(particle["y"])
                ),
                4
            )

        if particle["life"] <= 0:

            particles.remove(particle)

# ============================================================
# COLLISION
# ============================================================

def get_player_rect():

    return pygame.Rect(
        player_x + 18,
        player_y + 15,
        38,
        125
    )


def get_dragon_rect(dragon):

    return pygame.Rect(
        dragon["x"] + 5,
        dragon["y"] + 10,
        dragon["w"] - 15,
        dragon["h"] - 10
    )

# ============================================================
# RESET
# ============================================================

def reset_game():

    global player_y
    global velocity_y
    global on_ground
    global score
    global game_speed
    global game_over
    global started
    global dragons
    global particles
    global spawn_timer
    global level
    global level_up_timer

    player_y = GROUND_Y - player_height

    velocity_y = 0

    on_ground = True

    score = 0

    level = 1

    game_speed = 7

    dragons = []

    particles = []

    spawn_timer = 60

    level_up_timer = 0

    game_over = False

    started = True

# ============================================================
# HUD
# ============================================================

def draw_hud():

    # Main HUD
    pygame.draw.rect(
        screen,
        (8, 10, 18),
        (
            20,
            20,
            490,
            115
        ),
        border_radius=15
    )

    pygame.draw.rect(
        screen,
        (75, 80, 100),
        (
            20,
            20,
            490,
            115
        ),
        2,
        border_radius=15
    )

    # Score
    score_text = FONT_SMALL.render(
        f"SCORE  {score}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (
            40,
            35
        )
    )

    # Best
    best_text = FONT_SMALL.render(
        f"BEST  {best_score}",
        True,
        WHITE
    )

    screen.blit(
        best_text,
        (
            40,
            68
        )
    )

    # Level
    level_text = FONT_SMALL.render(
        f"LEVEL  {level}",
        True,
        (255, 210, 70)
    )

    screen.blit(
        level_text,
        (
            190,
            35
        )
    )

    # Speed
    speed_text = FONT_SMALL.render(
        f"SPEED  {game_speed:.1f}",
        True,
        (100, 200, 255)
    )

    screen.blit(
        speed_text,
        (
            190,
            68
        )
    )

    # Level progress bar
    bar_x = 325
    bar_y = 48

    pygame.draw.rect(
        screen,
        (45, 45, 55),
        (
            bar_x,
            bar_y,
            150,
            14
        ),
        border_radius=7
    )

    progress = score % 10

    progress_width = int(
        progress / 10 * 150
    )

    pygame.draw.rect(
        screen,
        (255, 190, 40),
        (
            bar_x,
            bar_y,
            progress_width,
            14
        ),
        border_radius=7
    )

    next_level = FONT_SMALL.render(
        f"{10 - progress} to next",
        True,
        WHITE
    )

    screen.blit(
        next_level,
        (
            325,
            72
        )
    )

# ============================================================
# LEVEL UP MESSAGE
# ============================================================

def draw_level_up():

    if level_up_timer <= 0:
        return

    # Fade effect
    alpha = min(
        255,
        level_up_timer * 3
    )

    level_surface = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    # Flash
    pygame.draw.rect(
        level_surface,
        (
            255,
            210,
            50,
            min(60, alpha // 3)
        ),
        (
            0,
            0,
            WIDTH,
            HEIGHT
        )
    )

    screen.blit(
        level_surface,
        (0, 0)
    )

    text = FONT_BIG.render(
        f"LEVEL {level}!",
        True,
        (255, 220, 70)
    )

    subtitle = FONT_MEDIUM.render(
        "THE JOURNEY CONTINUES",
        True,
        WHITE
    )

    # Slight vertical animation
    move = math.sin(
        level_up_timer * 0.08
    ) * 5

    screen.blit(
        text,
        text.get_rect(
            center=(
                WIDTH // 2,
                230 + int(move)
            )
        )
    )

    screen.blit(
        subtitle,
        subtitle.get_rect(
            center=(
                WIDTH // 2,
                285 + int(move)
            )
        )
    )

# ============================================================
# START SCREEN
# ============================================================

def draw_start_screen():

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 120)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    title = FONT_BIG.render(
        "NARUTO DRAGON RUNNER",
        True,
        WHITE
    )

    screen.blit(
        title,
        title.get_rect(
            center=(
                WIDTH // 2,
                200
            )
        )
    )

    subtitle = FONT_MEDIUM.render(
        "RUN • JUMP • SURVIVE",
        True,
        (255, 190, 50)
    )

    screen.blit(
        subtitle,
        subtitle.get_rect(
            center=(
                WIDTH // 2,
                260
            )
        )
    )

    controls = FONT_SMALL.render(
        "SPACE = JUMP",
        True,
        WHITE
    )

    screen.blit(
        controls,
        controls.get_rect(
            center=(
                WIDTH // 2,
                325
            )
        )
    )

    start = FONT_MEDIUM.render(
        "PRESS SPACE TO START",
        True,
        RED_LIGHT
    )

    screen.blit(
        start,
        start.get_rect(
            center=(
                WIDTH // 2,
                390
            )
        )
    )

# ============================================================
# GAME OVER
# ============================================================

def draw_game_over():

    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 155)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    title = FONT_BIG.render(
        "GAME OVER",
        True,
        RED_LIGHT
    )

    screen.blit(
        title,
        title.get_rect(
            center=(
                WIDTH // 2,
                230
            )
        )
    )

    score_text = FONT_MEDIUM.render(
        f"Score: {score}     Level: {level}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        score_text.get_rect(
            center=(
                WIDTH // 2,
                310
            )
        )
    )

    restart = FONT_SMALL.render(
        "PRESS SPACE TO PLAY AGAIN",
        True,
        (255, 220, 100)
    )

    screen.blit(
        restart,
        restart.get_rect(
            center=(
                WIDTH // 2,
                380
            )
        )
    )

# ============================================================
# MAIN LOOP
# ============================================================

running = True

while running:

    clock.tick(FPS)

    frame_count += 1

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                running = False

            if event.key == pygame.K_SPACE:

                # Start
                if not started:

                    reset_game()

                # Restart
                elif game_over:

                    reset_game()

                # Jump
                elif on_ground:

                    velocity_y = jump_strength

                    on_ground = False

                    for i in range(5):

                        create_dust_particle(
                            player_x + 30,
                            GROUND_Y - 5
                        )

    # ========================================================
    # BACKGROUND
    # ========================================================

    draw_background()

    draw_ground()

    # ========================================================
    # START SCREEN
    # ========================================================

    if not started:

        draw_naruto(
            player_x,
            GROUND_Y - player_height
        )

        draw_start_screen()

        pygame.display.flip()

        continue

    # ========================================================
    # GAME OVER
    # ========================================================

    if game_over:

        for dragon in dragons:

            draw_dragon(dragon)

        draw_naruto(
            player_x,
            player_y
        )

        update_particles()

        draw_hud()

        draw_game_over()

        pygame.display.flip()

        continue

    # ========================================================
    # PLAYER PHYSICS
    # ========================================================

    velocity_y += gravity

    player_y += velocity_y

    if player_y >= GROUND_Y - player_height:

        player_y = GROUND_Y - player_height

        velocity_y = 0

        if not on_ground:

            for i in range(5):

                create_dust_particle(
                    player_x + 30,
                    GROUND_Y - 5
                )

        on_ground = True

    # ========================================================
    # LEVEL
    # ========================================================

    update_level()

    # ========================================================
    # DIFFICULTY
    # ========================================================

    # Level 1 = 7.0
    # Level 2 = 7.5
    # Level 3 = 8.0
    # etc.

    game_speed = min(
        13,
        7 + (level - 1) * 0.5
    )

    # ========================================================
    # DRAGON SPAWNING
    # ========================================================

    spawn_timer -= 1

    if spawn_timer <= 0:

        create_dragon()

        # Higher level = dragons appear more frequently

        minimum_spawn = max(
            75,
            130 - level * 5
        )

        maximum_spawn = max(
            110,
            185 - level * 6
        )

        spawn_timer = random.randint(
            minimum_spawn,
            maximum_spawn
        )

    # ========================================================
    # DRAGONS
    # ========================================================

    player_rect = get_player_rect()

    for dragon in dragons[:]:

        dragon["x"] -= game_speed

        draw_dragon(dragon)

        dragon_rect = get_dragon_rect(
            dragon
        )

        # Collision
        if player_rect.colliderect(
            dragon_rect
        ):

            game_over = True

            if score > best_score:

                best_score = score

            for i in range(25):

                create_hit_particle(
                    player_x + 35,
                    player_y + 70
                )

        # Score
        if (
            not dragon["passed"]
            and
            dragon["x"] + dragon["w"] < player_x
        ):

            dragon["passed"] = True

            score += 1

        # Remove dragon
        if (
            dragon["x"] + dragon["w"]
            < -70
        ):

            dragons.remove(dragon)

    # ========================================================
    # PLAYER
    # ========================================================

    draw_naruto(
        player_x,
        player_y
    )

    # ========================================================
    # PARTICLES
    # ========================================================

    update_particles()

    # ========================================================
    # LEVEL UP EFFECT
    # ========================================================

    if level_up_timer > 0:

        level_up_timer -= 1

        draw_level_up()

    # ========================================================
    # HUD
    # ========================================================

    draw_hud()

    # ========================================================
    # DISPLAY
    # ========================================================

    pygame.display.flip()


pygame.quit()
