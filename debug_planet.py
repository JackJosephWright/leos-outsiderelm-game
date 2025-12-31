# DEBUG SCRIPT - Realistic Planet Surface!
# Run this with: python3 debug_planet.py

import pygame
import random
import math

# Wake up Pygame!
pygame.init()

# Screen size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("DEBUG - Realistic Planet Surface")

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 100)
medium_font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 24)

# Clock
clock = pygame.time.Clock()

# --- TEST PLANET ---
current_planet_name = "Earth"
planet_color = (50, 150, 50)  # Green for Earth
sky_color = (135, 206, 235)  # Sky blue

# Planet themes with sky colors
planet_themes = {
    "Earth": {"ground": (50, 150, 50), "sky": (135, 206, 235), "tree_color": (34, 139, 34)},
    "Mars": {"ground": (200, 80, 50), "sky": (255, 180, 150), "tree_color": (150, 80, 60)},
    "Ice World": {"ground": (150, 200, 255), "sky": (200, 230, 255), "tree_color": (100, 150, 180)},
    "Jungle": {"ground": (30, 100, 30), "sky": (100, 180, 100), "tree_color": (20, 80, 20)},
    "Desert": {"ground": (220, 180, 100), "sky": (255, 230, 180), "tree_color": (139, 90, 43)},
    "Ocean": {"ground": (50, 100, 150), "sky": (100, 150, 200), "tree_color": (30, 80, 100)},
    "Volcano": {"ground": (80, 30, 20), "sky": (255, 100, 50), "tree_color": (60, 40, 30)},
}

# Player position on planet
planet_explore_x = SCREEN_WIDTH // 2
planet_explore_y = SCREEN_HEIGHT // 2

# Inventory
materials = 25
food = 75
coins = 100

# --- GENERATE TERRAIN ---
def generate_terrain():
    global trees, rocks, grass_patches, chests, planet_materials, planet_food, water_pools

    trees = []
    rocks = []
    grass_patches = []
    chests = []
    planet_materials = []
    planet_food = []
    water_pools = []

    # Trees (different sizes)
    for i in range(12):
        tx = random.randint(80, SCREEN_WIDTH - 80)
        ty = random.randint(80, SCREEN_HEIGHT - 150)
        tree_size = random.randint(40, 80)
        tree_type = random.choice(["pine", "oak", "palm"])
        trees.append([tx, ty, tree_size, tree_type])

    # Rocks
    for i in range(8):
        rx = random.randint(50, SCREEN_WIDTH - 50)
        ry = random.randint(50, SCREEN_HEIGHT - 100)
        rock_size = random.randint(15, 35)
        rocks.append([rx, ry, rock_size])

    # Grass patches
    for i in range(30):
        gx = random.randint(20, SCREEN_WIDTH - 20)
        gy = random.randint(20, SCREEN_HEIGHT - 80)
        grass_patches.append([gx, gy])

    # Treasure chests!
    for i in range(4):
        cx = random.randint(100, SCREEN_WIDTH - 100)
        cy = random.randint(100, SCREEN_HEIGHT - 150)
        chest_type = random.choice(["common", "rare", "epic"])
        chests.append([cx, cy, chest_type, False])  # False = not opened

    # Materials
    for i in range(12):
        mx = random.randint(100, SCREEN_WIDTH - 100)
        my = random.randint(100, SCREEN_HEIGHT - 100)
        mtype = random.choice(["crystal", "metal", "rock"])
        planet_materials.append([mx, my, mtype])

    # Food
    for i in range(8):
        fx = random.randint(100, SCREEN_WIDTH - 100)
        fy = random.randint(100, SCREEN_HEIGHT - 100)
        ftype = random.choice(["apple", "meat", "berry", "mushroom"])
        planet_food.append([fx, fy, ftype])

    # Water pools (if not desert/volcano)
    if current_planet_name not in ["Desert", "Volcano"]:
        for i in range(3):
            wx = random.randint(150, SCREEN_WIDTH - 150)
            wy = random.randint(150, SCREEN_HEIGHT - 150)
            water_size = random.randint(40, 80)
            water_pools.append([wx, wy, water_size])

generate_terrain()

# Buildings
buildings = []
BASE_COST = 50
TURRET_COST = 30

# --- DRAWING FUNCTIONS ---

def draw_tree(x, y, size, tree_type, tree_color):
    trunk_color = (101, 67, 33)
    leaf_color = tree_color

    if tree_type == "pine":
        # Pine tree - triangle shape
        pygame.draw.rect(window, trunk_color, (x - 8, y, 16, size // 2))
        # Multiple triangle layers
        for i in range(3):
            layer_y = y - i * (size // 4)
            layer_size = size - i * 15
            pygame.draw.polygon(window, leaf_color, [
                (x, layer_y - layer_size),
                (x - layer_size // 2, layer_y),
                (x + layer_size // 2, layer_y)
            ])
            # Darker edge for depth
            darker = (max(0, leaf_color[0] - 30), max(0, leaf_color[1] - 30), max(0, leaf_color[2] - 30))
            pygame.draw.polygon(window, darker, [
                (x, layer_y - layer_size),
                (x - layer_size // 2, layer_y),
                (x + layer_size // 2, layer_y)
            ], 2)

    elif tree_type == "oak":
        # Oak tree - round fluffy top
        pygame.draw.rect(window, trunk_color, (x - 10, y, 20, size // 2))
        # Fluffy circles for leaves
        for ox in range(-2, 3):
            for oy in range(-2, 2):
                circle_x = x + ox * 15
                circle_y = y - size // 2 + oy * 12
                pygame.draw.circle(window, leaf_color, (circle_x, circle_y), 20)
        # Highlight
        lighter = (min(255, leaf_color[0] + 40), min(255, leaf_color[1] + 40), min(255, leaf_color[2] + 40))
        pygame.draw.circle(window, lighter, (x - 10, y - size // 2 - 10), 12)

    else:  # palm
        # Palm tree - curved trunk with fronds
        pygame.draw.arc(window, trunk_color, (x - 30, y - size, 60, size + 20), 0, 3.14, 12)
        # Palm fronds
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            frond_x = x + int(math.cos(rad) * 40)
            frond_y = y - size + int(math.sin(rad) * 20)
            pygame.draw.line(window, leaf_color, (x, y - size + 10), (frond_x, frond_y - 30), 4)
            pygame.draw.ellipse(window, leaf_color, (frond_x - 15, frond_y - 40, 30, 15))

def draw_rock(x, y, size):
    # Realistic rock with shading
    rock_color = (128, 128, 128)
    dark = (80, 80, 80)
    light = (180, 180, 180)

    # Main rock shape (irregular)
    points = []
    for i in range(6):
        angle = i * 60 + random.randint(-10, 10)
        rad = math.radians(angle)
        dist = size + random.randint(-5, 5)
        px = x + int(math.cos(rad) * dist)
        py = y + int(math.sin(rad) * dist * 0.7)
        points.append((px, py))

    pygame.draw.polygon(window, rock_color, points)
    pygame.draw.polygon(window, dark, points, 2)

    # Highlight on top
    pygame.draw.circle(window, light, (x - size // 4, y - size // 4), size // 4)

def draw_chest(x, y, chest_type, opened):
    if chest_type == "common":
        chest_color = (139, 90, 43)  # Brown
        lock_color = (150, 150, 150)
    elif chest_type == "rare":
        chest_color = (70, 130, 180)  # Blue
        lock_color = (192, 192, 192)
    else:  # epic
        chest_color = (148, 0, 211)  # Purple
        lock_color = (255, 215, 0)

    dark = (max(0, chest_color[0] - 40), max(0, chest_color[1] - 40), max(0, chest_color[2] - 40))

    if opened:
        # Open chest
        pygame.draw.rect(window, chest_color, (x - 20, y - 5, 40, 25))  # Base
        pygame.draw.rect(window, dark, (x - 20, y - 5, 40, 25), 2)
        # Open lid
        pygame.draw.rect(window, chest_color, (x - 22, y - 25, 44, 20))
        pygame.draw.rect(window, dark, (x - 22, y - 25, 44, 20), 2)
        # Sparkles inside
        for i in range(3):
            sx = x - 10 + i * 10
            sy = y + 5
            pygame.draw.circle(window, (255, 255, 100), (sx, sy), 3)
    else:
        # Closed chest
        pygame.draw.rect(window, chest_color, (x - 20, y - 15, 40, 30))  # Main body
        pygame.draw.rect(window, dark, (x - 20, y - 15, 40, 30), 2)
        # Lid
        pygame.draw.rect(window, dark, (x - 22, y - 18, 44, 8))
        # Lock
        pygame.draw.circle(window, lock_color, (x, y), 6)
        pygame.draw.rect(window, lock_color, (x - 3, y, 6, 8))
        # Shine
        pygame.draw.circle(window, (255, 255, 255), (x - 12, y - 10), 3)

def draw_water(x, y, size):
    # Realistic water pool
    water_color = (64, 164, 223)
    deep = (30, 100, 180)

    pygame.draw.ellipse(window, deep, (x - size, y - size // 2, size * 2, size))
    pygame.draw.ellipse(window, water_color, (x - size + 5, y - size // 2 + 3, size * 2 - 10, size - 6))

    # Ripples
    for i in range(2):
        ripple_y = y - size // 4 + i * 10
        pygame.draw.arc(window, (150, 200, 255), (x - size // 2, ripple_y, size, 10), 0, 3.14, 1)

def draw_grass(x, y, color):
    dark = (max(0, color[0] - 20), max(0, color[1] - 20), max(0, color[2] - 20))
    # Grass blades
    for i in range(-2, 3):
        blade_x = x + i * 4
        pygame.draw.line(window, dark, (blade_x, y), (blade_x + i, y - 12), 2)
        pygame.draw.line(window, color, (blade_x, y), (blade_x + i * 0.5, y - 10), 1)

def draw_material(x, y, mtype):
    if mtype == "crystal":
        # Crystal - shiny diamond shape
        pygame.draw.polygon(window, (80, 180, 255), [
            (x, y - 20), (x + 12, y), (x, y + 20), (x - 12, y)
        ])
        pygame.draw.polygon(window, (150, 220, 255), [
            (x, y - 20), (x + 6, y - 5), (x, y + 5), (x - 6, y - 5)
        ])
        # Sparkle
        pygame.draw.circle(window, (255, 255, 255), (x - 4, y - 10), 3)
    elif mtype == "metal":
        # Metal ore - shiny gray chunks
        pygame.draw.polygon(window, (140, 140, 160), [
            (x - 12, y + 8), (x - 8, y - 10), (x + 5, y - 12),
            (x + 14, y - 2), (x + 10, y + 10), (x - 5, y + 12)
        ])
        pygame.draw.polygon(window, (180, 180, 200), [
            (x - 5, y), (x, y - 8), (x + 8, y - 5), (x + 5, y + 5)
        ])
    else:  # rock
        # Stone - brown/gray
        pygame.draw.circle(window, (120, 100, 80), (x, y), 14)
        pygame.draw.circle(window, (150, 130, 100), (x - 3, y - 3), 8)

def draw_food(x, y, ftype):
    if ftype == "apple":
        # Apple with leaf
        pygame.draw.circle(window, (200, 30, 30), (x, y), 14)
        pygame.draw.circle(window, (255, 50, 50), (x - 4, y - 4), 6)
        pygame.draw.line(window, (101, 67, 33), (x, y - 14), (x + 2, y - 22), 3)
        pygame.draw.ellipse(window, (50, 150, 50), (x + 2, y - 24, 10, 6))
    elif ftype == "meat":
        # Cooked meat
        pygame.draw.ellipse(window, (160, 82, 45), (x - 18, y - 10, 36, 20))
        pygame.draw.ellipse(window, (200, 120, 80), (x - 14, y - 6, 28, 12))
        # Bone
        pygame.draw.line(window, (240, 230, 210), (x - 20, y), (x + 20, y), 4)
        pygame.draw.circle(window, (240, 230, 210), (x - 20, y), 5)
        pygame.draw.circle(window, (240, 230, 210), (x + 20, y), 5)
    elif ftype == "berry":
        # Berry cluster
        for bx, by in [(-6, 0), (6, 0), (0, -8), (-3, 6), (3, 6)]:
            pygame.draw.circle(window, (100, 30, 150), (x + bx, y + by), 6)
            pygame.draw.circle(window, (150, 50, 200), (x + bx - 2, y + by - 2), 2)
    else:  # mushroom
        # Mushroom
        pygame.draw.rect(window, (230, 220, 200), (x - 5, y - 5, 10, 15))
        pygame.draw.ellipse(window, (200, 50, 50), (x - 15, y - 18, 30, 18))
        pygame.draw.circle(window, (255, 255, 255), (x - 5, y - 14), 3)
        pygame.draw.circle(window, (255, 255, 255), (x + 5, y - 12), 2)

def draw_player(x, y):
    # More realistic astronaut
    # Shadow
    pygame.draw.ellipse(window, (0, 0, 0, 100), (x - 18, y + 15, 36, 12))

    # Legs
    pygame.draw.rect(window, (50, 50, 150), (x - 12, y + 5, 8, 18))
    pygame.draw.rect(window, (50, 50, 150), (x + 4, y + 5, 8, 18))
    # Boots
    pygame.draw.rect(window, (40, 40, 40), (x - 14, y + 20, 12, 6))
    pygame.draw.rect(window, (40, 40, 40), (x + 2, y + 20, 12, 6))

    # Body (spacesuit)
    pygame.draw.ellipse(window, (220, 220, 230), (x - 15, y - 15, 30, 35))
    pygame.draw.ellipse(window, (200, 200, 210), (x - 12, y - 12, 24, 28))

    # Backpack (life support)
    pygame.draw.rect(window, (100, 100, 120), (x + 12, y - 10, 10, 20))

    # Arms
    pygame.draw.rect(window, (220, 220, 230), (x - 22, y - 8, 10, 6))
    pygame.draw.rect(window, (220, 220, 230), (x + 12, y - 8, 10, 6))
    # Gloves
    pygame.draw.circle(window, (150, 150, 160), (x - 24, y - 5), 5)
    pygame.draw.circle(window, (150, 150, 160), (x + 24, y - 5), 5)

    # Helmet
    pygame.draw.circle(window, (220, 220, 230), (x, y - 22), 16)
    # Visor (reflective)
    pygame.draw.circle(window, (100, 180, 255), (x, y - 22), 12)
    pygame.draw.circle(window, (150, 210, 255), (x - 4, y - 26), 5)

    # Helmet reflection
    pygame.draw.arc(window, (255, 255, 255), (x - 10, y - 32, 12, 12), 0.5, 2.5, 2)

# --- MAIN LOOP ---
running = True
message = ""
message_timer = 0

while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # B = Build base
            if event.key == pygame.K_b:
                if materials >= BASE_COST:
                    materials -= BASE_COST
                    buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "base"])
                    message = "Built a BASE!"
                    message_timer = 120
                else:
                    message = "Need " + str(BASE_COST) + " materials!"
                    message_timer = 120

            # T = Build turret
            if event.key == pygame.K_t:
                if materials >= TURRET_COST:
                    materials -= TURRET_COST
                    buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "turret"])
                    message = "Built a TURRET!"
                    message_timer = 120
                else:
                    message = "Need " + str(TURRET_COST) + " materials!"
                    message_timer = 120

            # R = Regenerate terrain
            if event.key == pygame.K_r:
                generate_terrain()
                message = "Regenerated terrain!"
                message_timer = 120

            # C = Clear buildings
            if event.key == pygame.K_c:
                buildings = []
                message = "Cleared buildings!"
                message_timer = 120

            # E = Interact (open chests)
            if event.key == pygame.K_e:
                for chest in chests:
                    dist = ((planet_explore_x - chest[0]) ** 2 + (planet_explore_y - chest[1]) ** 2) ** 0.5
                    if dist < 50 and not chest[3]:
                        chest[3] = True  # Open it
                        if chest[2] == "common":
                            coins += 20
                            materials += 10
                            message = "Common chest: +20 coins, +10 materials!"
                        elif chest[2] == "rare":
                            coins += 50
                            materials += 25
                            message = "Rare chest: +50 coins, +25 materials!"
                        else:
                            coins += 100
                            materials += 50
                            message = "EPIC chest: +100 coins, +50 materials!"
                        message_timer = 180

            # 1-7 = Change planet
            planet_keys = {
                pygame.K_1: "Earth",
                pygame.K_2: "Mars",
                pygame.K_3: "Ice World",
                pygame.K_4: "Jungle",
                pygame.K_5: "Desert",
                pygame.K_6: "Ocean",
                pygame.K_7: "Volcano",
            }
            if event.key in planet_keys:
                current_planet_name = planet_keys[event.key]
                planet_color = planet_themes[current_planet_name]["ground"]
                sky_color = planet_themes[current_planet_name]["sky"]
                generate_terrain()
                message = "Welcome to " + current_planet_name + "!"
                message_timer = 120

    # Movement
    keys = pygame.key.get_pressed()
    move_speed = 5
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        planet_explore_x -= move_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        planet_explore_x += move_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        planet_explore_y -= move_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        planet_explore_y += move_speed

    # Keep on screen
    planet_explore_x = max(30, min(SCREEN_WIDTH - 30, planet_explore_x))
    planet_explore_y = max(30, min(SCREEN_HEIGHT - 50, planet_explore_y))

    # Collect materials
    for mat in planet_materials[:]:
        dist = ((planet_explore_x - mat[0]) ** 2 + (planet_explore_y - mat[1]) ** 2) ** 0.5
        if dist < 35:
            planet_materials.remove(mat)
            if mat[2] == "crystal":
                materials += 5
                message = "+5 Crystal!"
            elif mat[2] == "metal":
                materials += 3
                message = "+3 Metal!"
            else:
                materials += 1
                message = "+1 Stone!"
            message_timer = 60

    # Collect food
    for fd in planet_food[:]:
        dist = ((planet_explore_x - fd[0]) ** 2 + (planet_explore_y - fd[1]) ** 2) ** 0.5
        if dist < 35:
            planet_food.remove(fd)
            if fd[2] == "apple":
                food = min(100, food + 15)
                message = "+15 Food (Apple)"
            elif fd[2] == "meat":
                food = min(100, food + 25)
                message = "+25 Food (Meat)"
            elif fd[2] == "mushroom":
                food = min(100, food + 20)
                message = "+20 Food (Mushroom)"
            else:
                food = min(100, food + 10)
                message = "+10 Food (Berries)"
            message_timer = 60

    # --- DRAW ---
    theme = planet_themes[current_planet_name]
    tree_color = theme["tree_color"]

    # Sky gradient
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(sky_color[0] * (1 - ratio * 0.3))
        g = int(sky_color[1] * (1 - ratio * 0.3))
        b = int(sky_color[2] * (1 - ratio * 0.3))
        pygame.draw.line(window, (r, g, b), (0, y), (SCREEN_WIDTH, y))

    # Ground
    ground_color = theme["ground"]
    dark_ground = (max(0, ground_color[0] - 30), max(0, ground_color[1] - 30), max(0, ground_color[2] - 30))
    pygame.draw.rect(window, ground_color, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))

    # Ground texture
    for i in range(0, SCREEN_WIDTH, 30):
        pygame.draw.line(window, dark_ground, (i, SCREEN_HEIGHT - 100), (i + 15, SCREEN_HEIGHT), 1)

    # Water pools (behind everything)
    for pool in water_pools:
        draw_water(pool[0], pool[1], pool[2])

    # Grass patches
    for grass in grass_patches:
        draw_grass(grass[0], grass[1], tree_color)

    # Rocks
    for rock in rocks:
        draw_rock(rock[0], rock[1], rock[2])

    # Trees (sorted by Y for depth)
    for tree in sorted(trees, key=lambda t: t[1]):
        draw_tree(tree[0], tree[1], tree[2], tree[3], tree_color)

    # Buildings
    for building in buildings:
        if building[0] == current_planet_name:
            bx, by = int(building[1]), int(building[2])
            if building[3] == "base":
                # More realistic base
                pygame.draw.rect(window, (80, 80, 120), (bx - 35, by - 25, 70, 50))
                pygame.draw.rect(window, (100, 100, 150), (bx - 30, by - 20, 60, 40))
                pygame.draw.rect(window, (60, 60, 100), (bx - 35, by - 30, 70, 10))
                # Windows
                pygame.draw.rect(window, (200, 230, 255), (bx - 20, by - 15, 15, 15))
                pygame.draw.rect(window, (200, 230, 255), (bx + 5, by - 15, 15, 15))
                # Door
                pygame.draw.rect(window, (60, 60, 80), (bx - 8, by, 16, 20))
            else:  # turret
                # More realistic turret
                pygame.draw.rect(window, (100, 100, 100), (bx - 15, by - 10, 30, 30))
                pygame.draw.rect(window, (80, 80, 80), (bx - 8, by - 35, 16, 30))
                pygame.draw.circle(window, (120, 120, 120), (bx, by - 35), 10)
                pygame.draw.rect(window, (60, 60, 60), (bx - 3, by - 50, 6, 20))

    # Chests
    for chest in chests:
        draw_chest(chest[0], chest[1], chest[2], chest[3])

    # Materials
    for mat in planet_materials:
        draw_material(mat[0], mat[1], mat[2])

    # Food
    for fd in planet_food:
        draw_food(fd[0], fd[1], fd[2])

    # Player (astronaut)
    draw_player(int(planet_explore_x), int(planet_explore_y))

    # Chest prompt
    for chest in chests:
        dist = ((planet_explore_x - chest[0]) ** 2 + (planet_explore_y - chest[1]) ** 2) ** 0.5
        if dist < 50 and not chest[3]:
            prompt = small_font.render("Press E to open", True, (255, 255, 100))
            window.blit(prompt, (chest[0] - 40, chest[1] - 50))

    # --- UI ---
    # Dark panel behind UI
    pygame.draw.rect(window, (0, 0, 0), (10, 10, 280, 170), 0)
    pygame.draw.rect(window, (100, 100, 100), (10, 10, 280, 170), 2)

    # Planet name
    title = medium_font.render(current_planet_name, True, (255, 255, 255))
    window.blit(title, (20, 15))

    # Stats
    mat_text = font.render("Materials: " + str(materials), True, (200, 200, 100))
    window.blit(mat_text, (20, 60))

    coin_text = font.render("Coins: " + str(coins), True, (255, 215, 0))
    window.blit(coin_text, (20, 90))

    # Food bar
    food_label = font.render("Food:", True, (255, 255, 255))
    window.blit(food_label, (20, 120))
    pygame.draw.rect(window, (50, 50, 50), (100, 122, 150, 20))
    food_width = int((food / 100) * 146)
    food_color_bar = (50, 200, 50) if food > 30 else (200, 50, 50)
    pygame.draw.rect(window, food_color_bar, (102, 124, food_width, 16))

    # Message
    if message_timer > 0:
        message_timer -= 1
        msg_text = medium_font.render(message, True, (255, 255, 100))
        msg_rect = msg_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        pygame.draw.rect(window, (0, 0, 0), (msg_rect.x - 10, msg_rect.y - 5, msg_rect.width + 20, msg_rect.height + 10))
        window.blit(msg_text, msg_rect)

    # Controls panel
    pygame.draw.rect(window, (0, 0, 0), (10, SCREEN_HEIGHT - 110, 600, 100))
    pygame.draw.rect(window, (100, 100, 100), (10, SCREEN_HEIGHT - 110, 600, 100), 2)
    controls1 = small_font.render("WASD/Arrows = Move   |   E = Open chest   |   B = Build base   |   T = Build turret", True, (200, 200, 200))
    window.blit(controls1, (20, SCREEN_HEIGHT - 100))
    controls2 = small_font.render("R = Regenerate terrain   |   C = Clear buildings   |   1-7 = Change planet", True, (200, 200, 200))
    window.blit(controls2, (20, SCREEN_HEIGHT - 75))
    controls3 = small_font.render("Planets: 1=Earth, 2=Mars, 3=Ice, 4=Jungle, 5=Desert, 6=Ocean, 7=Volcano", True, (150, 150, 150))
    window.blit(controls3, (20, SCREEN_HEIGHT - 50))

    # DEBUG label
    debug_text = font.render("DEBUG MODE", True, (255, 100, 100))
    window.blit(debug_text, (SCREEN_WIDTH - 150, 20))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("Debug script ended!")
