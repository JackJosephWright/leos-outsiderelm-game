# IN OUTSIDERELM - by Commander Leo!
# ===================================

# This line gets Pygame ready (Pygame helps us make games!)
import pygame
# Random helps us put stars in random places!
import random
# Math helps us make wavy stink lines!
import math
# OS helps us find music files!
import os
# JSON helps us save our coins to a file!
import json
import asyncio
import sys

# Detect if we're running on the web (Pygbag/Emscripten)
print(f"Platform detected: {sys.platform}")
IS_WEB = sys.platform == "emscripten"
if IS_WEB:
    print("WEB MODE: Using delta time for smooth movement!")
else:
    print("DESKTOP MODE: Using delta time for smooth movement!")

# Target frame time in milliseconds (for 60 FPS)
TARGET_FRAME_TIME = 1000 / 60  # ~16.67ms per frame

# Wake up Pygame! (like turning on a game console)
pygame.init()

# Create a clock to control game speed (60 frames per second!)
clock = pygame.time.Clock()
FPS = 60  # 60 frames per second - smooth and consistent!

# --- MUSIC! ---
# Initialize the music mixer and play some epic tunes!
pygame.mixer.init()

# Find all the songs in the music folder!
music_folder = "music"
songs = []  # List to hold all our song file paths

# Look for all ogg and wav files in the music folder (ogg works on web!)
if os.path.exists(music_folder):
    for file in os.listdir(music_folder):
        if file.endswith(".ogg") or file.endswith(".wav"):
            songs.append(os.path.join(music_folder, file))
    print("Found " + str(len(songs)) + " songs!")

# Shuffle the songs so they play in random order without repeating!
random.shuffle(songs)
current_song_index = 0  # Which song we're on in the shuffled list

# Function to play the next song (without repeating!)
def play_random_song():
    global current_song_index
    if len(songs) > 0:
        # Get the next song in our shuffled list
        song = songs[current_song_index]
        pygame.mixer.music.load(song)
        pygame.mixer.music.set_volume(0.5)  # 50% volume
        pygame.mixer.music.play()  # Play once (we'll pick a new one when it ends!)
        print("Now playing: " + song)

        # Move to next song, and reshuffle when we've played them all!
        current_song_index = current_song_index + 1
        if current_song_index >= len(songs):
            current_song_index = 0
            random.shuffle(songs)  # Reshuffle for next round!
            print("Reshuffled the playlist!")

# Start playing a random song!
play_random_song()

# --- COINS (SAVED POINTS!) ---
# This is your wallet! Coins save even when you close the game!
save_file = "save_data.json"  # The file where we save your coins!

# Function to load coins from the save file!
def load_coins():
    # Try to open the save file and read the coins
    if os.path.exists(save_file):
        try:
            with open(save_file, "r") as f:
                data = json.load(f)
                return data.get("coins", 0)  # Get coins, or 0 if not found
        except:
            return 0  # If something goes wrong, start with 0
    return 0  # No save file? Start with 0 coins!

# Function to save coins to the save file!
def save_coins(coins_to_save):
    data = {"coins": coins_to_save}
    with open(save_file, "w") as f:
        json.dump(data, f)
    print("Saved " + str(coins_to_save) + " coins!")

# Load our coins when the game starts!
coins = load_coins()
print("You have " + str(coins) + " coins!")

# Set up an event for when the music ends so we can play another!
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

# --- MAKE THE WINDOW ---
# These numbers are how big the window is (wide, tall)
# BIGGER window for exploring space!
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Give our window a name at the top!
pygame.display.set_caption("In Outsiderelm")

# --- THRAWN THE HERO ---
# Thrawn starts at the bottom center of the screen
thrawn_x = SCREEN_WIDTH // 2  # Middle of screen
thrawn_y = SCREEN_HEIGHT - 100  # Near the bottom
thrawn_speed = 5  # How fast Thrawn moves in pixels per frame at 60 FPS

# --- MAKE THE STARS ---
# Lots of stars for a big space feeling!
# We have 3 layers: far stars (slow), medium stars, close stars (fast)
far_stars = []  # Tiny distant stars (move slow)
for i in range(80):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    far_stars.append([x, y])

medium_stars = []  # Medium stars
for i in range(50):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    medium_stars.append([x, y])

close_stars = []  # Big close stars (move fast) - feels like speed!
for i in range(20):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    close_stars.append([x, y])

# Keep the old stars list for compatibility
stars = far_stars

# --- LASERS ---
# This list holds all the lasers Thrawn shoots!
lasers = []  # Empty list - lasers get added when SPACE is pressed
laser_speed = 10  # How fast lasers fly up in pixels per frame at 60 FPS
shoot_cooldown = 0  # Timer to prevent shooting too fast
normal_shoot_rate = 300  # Normal time between shots (in ms)
fast_shoot_rate = 80  # Super fast shooting! (in ms)

# --- BIG LASER (MEGA BEAM!) ---
# The ultimate weapon! A huge beam that destroys everything!
big_laser_active = False  # Is the big laser firing?
big_laser_timer = 0  # How long the beam lasts
big_laser_max_time = 500  # How long the beam stays on screen
big_laser_cooldown = 0  # Time until you can fire again
big_laser_cooldown_time = 2000  # Cooldown between big laser shots

# --- ANGRY ZELDAS ---
# These are the bad guys! Green circles with angry faces!
zeldas = []  # Empty list to hold our angry Zeldas - each is [x, y, x_direction]
zelda_speed = 1.5  # How fast Zeldas fly down in pixels per frame at 60 FPS
zelda_side_speed = 2  # How fast Zeldas move side to side!
zelda_spawn_timer = 0  # Counts up until it's time to spawn a new Zelda
zelda_spawn_rate = 2000  # How often a new Zelda appears (in ms)

# --- ZELDA'S SWORDS ---
# The Zeldas fight back by throwing swords at Thrawn!
swords = []  # Each sword is [x, y] position
sword_speed = 5  # How fast swords fly down in pixels per frame at 60 FPS
sword_timer = 0  # Counts up until Zeldas throw more swords
sword_rate = 1500  # How often Zeldas throw swords (in ms)

# --- EXPLOSIONS ---
# When a laser hits a Zelda, BOOM! We show an explosion!
explosions = []  # Each explosion is [x, y, timer] - timer counts down then it disappears

# --- SCORE AND LIVES ---
score = 0  # Your score! Goes up when you destroy Zeldas!
lives = 3  # You start with 3 lives! Don't let Zeldas hit you!
level = 1  # What level are you on? Gets harder each level!

# --- LEVEL COMPLETE! ---
level_complete = False  # True when boss is defeated!
level_complete_timer = 0  # Timer for showing "LEVEL COMPLETE!"

# --- TEXT FOR SHOWING SCORE ---
# This sets up the font so we can write words on screen!
font = pygame.font.Font(None, 36)  # 36 = size of the text
big_font = pygame.font.Font(None, 100)  # BIG font for GAME OVER!
medium_font = pygame.font.Font(None, 50)  # Medium font for final score

# --- PRE-RENDERED SURFACES FOR PERFORMANCE ---
# Pre-render the star background so we don't draw 150 circles every frame!
star_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT * 2), pygame.SRCALPHA)
star_surface.fill((0, 0, 0, 0))  # Transparent background

# Draw all stars onto the surface ONCE
for star in far_stars:
    pygame.draw.circle(star_surface, (100, 100, 120), (int(star[0]), int(star[1])), 1)
    pygame.draw.circle(star_surface, (100, 100, 120), (int(star[0]), int(star[1]) + SCREEN_HEIGHT), 1)
for star in medium_stars:
    pygame.draw.circle(star_surface, (180, 180, 200), (int(star[0]), int(star[1])), 2)
    pygame.draw.circle(star_surface, (180, 180, 200), (int(star[0]), int(star[1]) + SCREEN_HEIGHT), 2)
for star in close_stars:
    pygame.draw.circle(star_surface, (255, 255, 255), (int(star[0]), int(star[1])), 3)
    pygame.draw.circle(star_surface, (255, 255, 255), (int(star[0]), int(star[1]) + SCREEN_HEIGHT), 3)

# Star scroll position (for parallax effect)
star_scroll_y = 0

# Pre-render the title glow effect ONCE instead of every frame!
title_glow_surface = pygame.Surface((600, 120), pygame.SRCALPHA)
title_text_main = big_font.render("IN OUTSIDERELM", True, (0, 100, 255))
title_text_glow = big_font.render("IN OUTSIDERELM", True, (0, 50, 150))
# Draw glow by rendering offset copies
for offset_x in range(-3, 4):
    for offset_y in range(-3, 4):
        title_glow_surface.blit(title_text_glow, (50 + offset_x, 10 + offset_y))
# Draw main title on top
title_glow_surface.blit(title_text_main, (50, 10))

# Pre-render level complete glow too!
level_complete_surface = pygame.Surface((700, 120), pygame.SRCALPHA)
complete_text_main = big_font.render("LEVEL COMPLETE!", True, (0, 255, 0))
complete_text_glow = big_font.render("LEVEL COMPLETE!", True, (0, 100, 0))
for offset_x in range(-3, 4):
    for offset_y in range(-3, 4):
        level_complete_surface.blit(complete_text_glow, (50 + offset_x, 10 + offset_y))
level_complete_surface.blit(complete_text_main, (50, 10))

# --- TEXT CACHE ---
# Cache rendered text to avoid re-rendering every frame
cached_texts = {}
last_score = -1
last_level = -1
last_lives = -1
last_coins = -1

# --- BOSS SYSTEM ---
# Different bosses appear on different levels!
# Level 1: Star Destroyer, Level 2: Mega Zelda Queen,
# Level 3: Giant Robot, Level 4: Space Dragon, Level 5+: Super Dancing 67!
boss_type = "star_destroyer"  # Which boss is active?
boss_active = False  # Is the boss on screen?
boss_x = SCREEN_WIDTH // 2  # Boss x position (center of screen)
boss_y = -150  # Boss y position (starts above screen)
boss_health = 20  # How many hits to defeat the boss!
boss_max_health = 20  # For the health bar
boss_speed = 3  # How fast boss moves side to side in pixels per frame at 60 FPS
boss_direction = 1  # 1 = moving right, -1 = moving left
boss_shoot_timer = 0  # Timer for boss shooting
boss_shoot_rate = 800  # How often boss shoots
boss_lasers = []  # Boss's laser beams!
boss_spawn_score = 500  # Boss appears when you reach this score!
boss_defeated = False  # Did we beat the boss?
boss_defeated_timer = 0  # For boss explosion animation

# Special boss variables!
robot_fist_x = 0  # For Giant Robot's rocket fist!
robot_fist_y = -100
robot_fist_active = False
dragon_fire_timer = 0  # For Space Dragon's fire breath!
dance_angle = 0  # For Super Dancing 67's dance moves!

# --- GAME STATE ---
# This controls if we're on the title screen, shop, or playing!
# "title" = show the cool opening screen
# "shop" = the AWESOME shop where you buy power-ups!
# "playing" = fly around space, discover planets, and fight Zeldas!
game_state = "title"
title_timer = 0  # Timer for cool animations on title screen!

# --- SPACE EXPLORATION! ---
# The big space world you can explore!
WORLD_WIDTH = 4000   # How big is space? (4000 pixels wide)
WORLD_HEIGHT = 4000  # (4000 pixels tall)

# Camera position (what part of the world we're looking at)
camera_x = 0
camera_y = 0

# Player position in the WORLD (not screen!)
player_world_x = WORLD_WIDTH // 2  # Start in the middle of space
player_world_y = WORLD_HEIGHT // 2
player_walk_speed = 4  # Walking speed
player_run_speed = 8   # Running speed (hold SHIFT)

# --- PLANETS! ---
# Planets to discover in space! Each planet is:
# [x, y, name, color, size, discovered, has_zeldas, has_food, has_materials]
planets = [
    [500, 500, "Earth", (50, 150, 50), 80, True, True, True, True],       # Starting planet (discovered)
    [1500, 800, "Mars", (200, 80, 50), 60, False, True, False, True],     # Red planet
    [2500, 400, "Ice World", (150, 200, 255), 70, False, True, True, False],  # Cold planet
    [3000, 2000, "Jungle", (30, 180, 30), 90, False, True, True, True],   # Green planet
    [800, 2500, "Desert", (220, 180, 100), 65, False, True, False, True], # Sandy planet
    [2000, 3200, "Ocean", (50, 100, 200), 85, False, False, True, False], # Water planet
    [3500, 1200, "Volcano", (180, 50, 30), 55, False, True, False, True], # Fire planet
    [1200, 1800, "Moon Base", (180, 180, 180), 40, False, False, False, True],  # Small moon
]

# Current planet (which planet are we battling on?)
current_planet = None
current_planet_name = "Space"

# --- INVENTORY! ---
# What you've collected!
food = 100  # Start with some food (decreases over time!)
materials = 0  # For building bases

# --- SHUTTLE! ---
# Your shuttle to travel to planets!
near_planet = None  # Which planet are we near? (None if not near any)
shuttle_cooldown = 0  # Can't spam the shuttle button

# --- THE SHOP! ---
# These are the things you can buy!
shop_selection = 0  # Which item you're looking at (0, 1, 2, etc.)

# Power-up prices (how many coins each one costs!)
SHIELD_PRICE = 300           # Protects you from 1 hit!
FAST_SHOOTING_PRICE = 250    # Shoot lasers super fast!
BIG_LASER_PRICE = 500        # MEGA destruction beam!
WINGMAN_PRICE = 400          # A buddy ship that fights with you!

# What power-ups does the player have for this game?
has_shield = False           # Do you have a shield?
shield_hits = 0              # How many hits can your shield take?
has_fast_shooting = False    # Did you buy fast shooting?
has_big_laser = False        # Did you buy the BIG LASER?
wingmen = []                 # Your fleet of wingman ships! Each is [x, y]
wingmen_count = 0            # How many wingmen you bought

# --- CHESTS! ---
# Treasure chests spawn during gameplay with awesome loot!
chests = []  # Each chest is [x, y, chest_type] - chest_type determines the loot!
chest_spawn_timer = 0  # Timer for spawning chests
chest_spawn_rate = 8000  # Spawn a chest every 8 seconds (in ms)

# Possible chest loot types:
CHEST_TYPES = [
    "spread_shot",      # Shoot 3 lasers at once!
    "homing_missiles",  # Missiles that track enemies!
    "piercing_laser",   # Laser goes through multiple enemies!
    "double_points",    # 2x score for a while!
    "extra_shield",     # Free shield!
    "coin_bonus",       # Bonus coins!
]

# --- NEW WEAPONS FROM CHESTS! ---
# These are temporary power-ups you find in chests (lost on death!)
has_spread_shot = False      # Shoot 3 lasers in a spread pattern!
has_homing_missiles = False  # Missiles track the nearest enemy!
has_piercing_laser = False   # Lasers go through enemies!
has_double_points = False    # Double score!
double_points_timer = 0      # How long double points lasts

# Homing missile tracking
homing_missiles = []  # Each missile is [x, y, target_zelda]

# Shop items list (for drawing the shop)
shop_items = [
    {"name": "SHIELD", "price": SHIELD_PRICE, "desc": "Bubble protects you!", "color": (100, 200, 255)},
    {"name": "FAST SHOOTING", "price": FAST_SHOOTING_PRICE, "desc": "Pew pew pew pew!", "color": (255, 100, 100)},
    {"name": "BIG LASER", "price": BIG_LASER_PRICE, "desc": "MEGA BEAM!", "color": (255, 255, 0)},
    {"name": "WINGMAN", "price": WINGMAN_PRICE, "desc": "Buddy ship fights with you!", "color": (0, 255, 100)},
    {"name": "START GAME!", "price": 0, "desc": "Let's GO!", "color": (255, 255, 255)},
]

# --- GAME OVER STUFF ---
game_over = False  # When True, show the game over screen!
game_over_timer = 0  # Counts up during game over for animations
game_over_explosions = []  # Extra explosions for the big finale!

# --- GAME LOOP ---
# The game keeps running until we close it
running = True

async def main():
    global running, game_state, title_timer, shop_selection, coins
    global has_shield, shield_hits, has_fast_shooting, has_big_laser
    global wingmen, wingmen_count, thrawn_x, thrawn_y, lasers, shoot_cooldown
    global big_laser_active, big_laser_timer, big_laser_cooldown
    global zeldas, zelda_spawn_timer, swords, sword_timer
    global boss_active, boss_x, boss_y, boss_health, boss_direction, boss_shoot_timer
    global boss_lasers, boss_defeated, boss_defeated_timer, boss_type, boss_spawn_score, boss_max_health
    global robot_fist_active, robot_fist_x, robot_fist_y, dragon_fire_timer, dance_angle
    global explosions, score, lives, level, level_complete, level_complete_timer
    global game_over, game_over_timer, game_over_explosions
    global far_stars, medium_stars, close_stars
    global zelda_speed, zelda_spawn_rate, sword_rate
    global star_scroll_y, cached_texts, last_score, last_level, last_lives, last_coins
    global chests, chest_spawn_timer, has_spread_shot, has_homing_missiles
    global has_piercing_laser, has_double_points, double_points_timer, homing_missiles
    global camera_x, camera_y, player_world_x, player_world_y
    global planets, current_planet, current_planet_name, near_planet
    global food, materials, shuttle_cooldown

    # Track time for delta calculations
    last_time = pygame.time.get_ticks()

    while running:
        await asyncio.sleep(0)  # Let the browser breathe! (MUST be at start of loop for web!)

        # Calculate delta time (how long since last frame)
        current_time = pygame.time.get_ticks()
        delta_ms = current_time - last_time
        last_time = current_time

        # Convert to a multiplier (1.0 = perfect 60 FPS, 2.0 = 30 FPS, etc.)
        # Cap delta to prevent huge jumps if game freezes
        delta_ms = min(delta_ms, 100)  # Cap at 100ms (10 FPS minimum)
        dt = delta_ms / TARGET_FRAME_TIME  # dt = 1.0 at 60 FPS

        # Check if player closes the window (clicks the X)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- PLAY NEXT SONG WHEN CURRENT ONE ENDS ---
            if event.type == SONG_END:
                play_random_song()  # Pick another random song!

            # --- PRESS ENTER TO PLAY! ---
            # When on title screen, press ENTER to start the game!
            if event.type == pygame.KEYDOWN and game_state == "title":
                if event.key == pygame.K_RETURN:  # RETURN is the ENTER key!
                    game_state = "playing"  # Start playing!
                    # Center camera on player
                    camera_x = player_world_x - SCREEN_WIDTH // 2
                    camera_y = player_world_y - SCREEN_HEIGHT // 2

            # --- IN-GAME CONTROLS! ---
            # TAB opens the shop while playing!
            if event.type == pygame.KEYDOWN and game_state == "playing" and not game_over:
                if event.key == pygame.K_TAB:
                    game_state = "shop"
                    shop_selection = 0

            # --- SHOP CONTROLS! ---
            # In the shop, use UP/DOWN to pick items and ENTER to buy!
            if event.type == pygame.KEYDOWN and game_state == "shop":
                # Move UP in the shop menu
                if event.key == pygame.K_UP:
                    shop_selection = shop_selection - 1
                    if shop_selection < 0:
                        shop_selection = len(shop_items) - 1  # Wrap to bottom!

                # Move DOWN in the shop menu
                if event.key == pygame.K_DOWN:
                    shop_selection = shop_selection + 1
                    if shop_selection >= len(shop_items):
                        shop_selection = 0  # Wrap to top!

                # ENTER to buy the selected item!
                if event.key == pygame.K_RETURN:
                    selected_item = shop_items[shop_selection]

                    # Is it the START GAME button?
                    if selected_item["name"] == "START GAME!":
                        game_state = "playing"  # Let's GO!
                        # Create wingmen based on how many you bought!
                        wingmen = []
                        for i in range(wingmen_count):
                            # Position wingmen on alternating sides of Thrawn!
                            if i % 2 == 0:
                                wx = thrawn_x - 50 - (i // 2) * 40  # Left side
                            else:
                                wx = thrawn_x + 50 + (i // 2) * 40  # Right side
                            wingmen.append([wx, thrawn_y])

                    # Try to buy SHIELD!
                    elif selected_item["name"] == "SHIELD":
                        if coins >= SHIELD_PRICE:
                            coins = coins - SHIELD_PRICE
                            has_shield = True
                            shield_hits = shield_hits + 1  # Can buy multiple!
                            save_coins(coins)
                            print("Bought SHIELD! You have " + str(shield_hits) + " shield(s)!")

                    # Try to buy FAST SHOOTING!
                    elif selected_item["name"] == "FAST SHOOTING":
                        if coins >= FAST_SHOOTING_PRICE and not has_fast_shooting:
                            coins = coins - FAST_SHOOTING_PRICE
                            has_fast_shooting = True
                            save_coins(coins)
                            print("Bought FAST SHOOTING!")

                    # Try to buy BIG LASER!
                    elif selected_item["name"] == "BIG LASER":
                        if coins >= BIG_LASER_PRICE and not has_big_laser:
                            coins = coins - BIG_LASER_PRICE
                            has_big_laser = True
                            save_coins(coins)
                            print("Bought BIG LASER!")

                    # Try to buy a WINGMAN!
                    elif selected_item["name"] == "WINGMAN":
                        if coins >= WINGMAN_PRICE:
                            coins = coins - WINGMAN_PRICE
                            wingmen_count = wingmen_count + 1
                            save_coins(coins)
                            print("Bought WINGMAN! You have " + str(wingmen_count) + " wingmen!")

            # --- SHOOTING LASERS ---
            # When SPACE bar is pressed, shoot a laser! (only if game is NOT over)
            # Now uses a cooldown so you can't spam too fast (unless you have fast shooting!)
            if event.type == pygame.KEYDOWN and not game_over and game_state == "playing":  # A key was just pressed
                if event.key == pygame.K_SPACE:  # Was it SPACE?
                    # Check if we can shoot (cooldown is done)
                    if shoot_cooldown <= 0:
                        # SPREAD SHOT - shoot 3 lasers in a fan!
                        if has_spread_shot:
                            lasers.append([thrawn_x - 15, thrawn_y - 30])  # Left laser
                            lasers.append([thrawn_x, thrawn_y - 30])       # Center laser
                            lasers.append([thrawn_x + 15, thrawn_y - 30])  # Right laser
                        else:
                            # Normal single laser
                            new_laser = [thrawn_x, thrawn_y - 30]
                            lasers.append(new_laser)

                        # HOMING MISSILES - shoot tracking missiles!
                        if has_homing_missiles:
                            homing_missiles.append([thrawn_x - 10, thrawn_y - 25])
                            homing_missiles.append([thrawn_x + 10, thrawn_y - 25])

                        # WINGMEN SHOOT TOO! (when Thrawn shoots)
                        for wingman in wingmen:
                            wingman_laser = [wingman[0], wingman[1] - 20]
                            lasers.append(wingman_laser)

                        # Set the cooldown based on power-up!
                        if has_fast_shooting:
                            shoot_cooldown = fast_shoot_rate  # Super fast!
                        else:
                            shoot_cooldown = normal_shoot_rate  # Normal speed

                # --- BIG LASER! ---
                # Press B to fire the MEGA BEAM! (if you have it)
                if event.key == pygame.K_b:
                    if has_big_laser and big_laser_cooldown <= 0 and not big_laser_active:
                        big_laser_active = True
                        big_laser_timer = big_laser_max_time
                        print("MEGA BEAM ACTIVATED!")

        # --- TITLE SCREEN ---
        # If we're on the title screen, update the timer and skip game logic!
        if game_state == "title":
            title_timer = title_timer + delta_ms

        # --- UPDATE SHOOTING COOLDOWN ---
        # Count down the cooldown timer so you can shoot again!
        if shoot_cooldown > 0:
            shoot_cooldown = shoot_cooldown - delta_ms

        # --- UPDATE BIG LASER ---
        # If the big laser is active, count down its timer and destroy enemies!
        if big_laser_active:
            big_laser_timer = big_laser_timer - delta_ms
            if big_laser_timer <= 0:
                big_laser_active = False
                big_laser_cooldown = big_laser_cooldown_time  # Start cooldown!

            # BIG LASER destroys ALL Zeldas in its path!
            # The beam is a wide column from Thrawn going up!
            zeldas_to_destroy = []
            for zelda in zeldas:
                # Is the Zelda in the laser beam? (within 50 pixels of Thrawn's x)
                if abs(zelda[0] - thrawn_x) < 50 and zelda[1] < thrawn_y:
                    zeldas_to_destroy.append(zelda)
                    explosions.append([zelda[0], zelda[1], 300])
                    score = score + 100  # Still get points!

            for zelda in zeldas_to_destroy:
                if zelda in zeldas:
                    zeldas.remove(zelda)

            # Big laser also damages the BOSS!
            if boss_active and not boss_defeated:
                if abs(boss_x - thrawn_x) < 100 and boss_y > 0:
                    # Constant damage while beam is on boss! (damage every ~50ms)
                    if int(big_laser_timer / 50) != int((big_laser_timer + delta_ms) / 50):
                        boss_health = boss_health - 1
                        explosions.append([boss_x + random.randint(-50, 50), boss_y + random.randint(-20, 20), 200])

        # Count down big laser cooldown
        if big_laser_cooldown > 0:
            big_laser_cooldown = big_laser_cooldown - delta_ms

        # --- MOVE THRAWN WITH ARROW KEYS ---
        # Only move if game is NOT over and we're playing!
        if not game_over and game_state == "playing":
            # Check which keys are being pressed right now
            keys = pygame.key.get_pressed()

            # How fast should Thrawn move? SHIFT to go faster!
            current_speed = thrawn_speed * dt  # Multiply by delta time!
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                current_speed = current_speed * 1.5  # BOOST!

            # Move in the WORLD (not just screen!)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_world_x = player_world_x - current_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_world_x = player_world_x + current_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player_world_y = player_world_y - current_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player_world_y = player_world_y + current_speed

            # Keep player in world bounds
            player_world_x = max(50, min(WORLD_WIDTH - 50, player_world_x))
            player_world_y = max(50, min(WORLD_HEIGHT - 50, player_world_y))

            # Camera follows player (smooth)
            target_camera_x = player_world_x - SCREEN_WIDTH // 2
            target_camera_y = player_world_y - SCREEN_HEIGHT // 2
            camera_x = camera_x + (target_camera_x - camera_x) * 0.1 * dt
            camera_y = camera_y + (target_camera_y - camera_y) * 0.1 * dt

            # Keep camera in bounds
            camera_x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, camera_x))
            camera_y = max(0, min(WORLD_HEIGHT - SCREEN_HEIGHT, camera_y))

            # Update thrawn_x/y to match world position on screen (for drawing and collisions)
            thrawn_x = player_world_x - camera_x
            thrawn_y = player_world_y - camera_y

            # Check for nearby planets and discover them!
            for planet in planets:
                px, py = planet[0], planet[1]
                dist = ((player_world_x - px) ** 2 + (player_world_y - py) ** 2) ** 0.5
                planet_size = planet[4]

                # Discover planet if close enough!
                if dist < planet_size + 100:
                    if not planet[5]:  # Not discovered yet?
                        planet[5] = True  # DISCOVERED!
                        print("DISCOVERED: " + planet[2] + "!")

        # --- UPDATE WINGMEN ---
        # Wingmen fly in formation around Thrawn!
        if game_state == "playing" and not game_over:
            for i in range(len(wingmen)):
                wingman = wingmen[i]
                # Calculate target position (formation around Thrawn)
                if i % 2 == 0:
                    target_x = thrawn_x - 50 - (i // 2) * 40  # Left side
                else:
                    target_x = thrawn_x + 50 + (i // 2) * 40  # Right side
                target_y = thrawn_y + 20  # Slightly behind Thrawn

                # Smoothly move toward target position (use dt for smooth movement)
                wingman[0] = wingman[0] + (target_x - wingman[0]) * 0.1 * dt
                wingman[1] = wingman[1] + (target_y - wingman[1]) * 0.1 * dt

        # --- MOVE THE LASERS ---
        # Each laser flies UP the screen!
        for laser in lasers:
            laser[1] = laser[1] - laser_speed * dt  # Move up (subtract from y)

        # Remove lasers that flew off the top of the screen
        # (We don't need them anymore - they're in outer space now!)
        lasers_to_keep = []  # New list for lasers still on screen
        for laser in lasers:
            if laser[1] > 0:  # If laser is still visible
                lasers_to_keep.append(laser)  # Keep it!
        lasers = lasers_to_keep  # Replace old list with new list

        # --- SPAWN ANGRY ZELDAS ---
        # The timer counts up, and when it's big enough, a new Zelda appears!
        # (Don't spawn new ones if game is over or on title screen!)
        if not game_over and game_state == "playing":
            zelda_spawn_timer = zelda_spawn_timer + delta_ms
        if zelda_spawn_timer >= zelda_spawn_rate and not game_over and game_state == "playing":
            # Time to spawn a new angry Zelda!
            new_zelda_x = random.randint(30, SCREEN_WIDTH - 30)  # Random spot (not too close to edges)
            new_zelda_y = -30  # Start above the screen (so it flies in!)
            # Random direction: -1 = moving left, 1 = moving right
            new_zelda_dir = random.choice([-1, 1])
            zeldas.append([new_zelda_x, new_zelda_y, new_zelda_dir])
            zelda_spawn_timer = 0  # Reset the timer!

        # --- MOVE THE ANGRY ZELDAS ---
        # Each Zelda flies DOWN and SIDEWAYS in a zigzag pattern!
        for zelda in zeldas:
            zelda[1] = zelda[1] + zelda_speed * dt  # Move down (add to y)
            zelda[0] = zelda[0] + (zelda_side_speed * zelda[2]) * dt  # Move sideways!

            # Bounce off the walls! If Zelda hits edge, reverse direction!
            if zelda[0] <= 30:  # Hit left wall?
                zelda[2] = 1    # Now move right!
            if zelda[0] >= SCREEN_WIDTH - 30:  # Hit right wall?
                zelda[2] = -1   # Now move left!

        # Remove Zeldas that flew off the bottom of the screen
        zeldas_to_keep = []
        for zelda in zeldas:
            if zelda[1] < SCREEN_HEIGHT + 50:  # If Zelda is still on screen
                zeldas_to_keep.append(zelda)
        zeldas = zeldas_to_keep

        # --- ZELDAS THROW SWORDS! ---
        # Every so often, each Zelda on screen throws a sword at Thrawn!
        # (Don't throw if game is over or on title screen!)
        if not game_over and game_state == "playing":
            sword_timer = sword_timer + delta_ms
        if sword_timer >= sword_rate and not game_over and game_state == "playing":
            # Time for Zeldas to throw swords!
            for zelda in zeldas:
                # Only shoot if Zelda is on screen (not above it)
                if zelda[1] > 0:
                    # Create a sword at the Zelda's position!
                    new_sword = [zelda[0], zelda[1] + 30]  # Below the Zelda
                    swords.append(new_sword)
            sword_timer = 0  # Reset the timer!

        # --- MOVE THE SWORDS ---
        # Each sword flies DOWN toward Thrawn!
        for sword in swords:
            sword[1] = sword[1] + sword_speed * dt  # Move down (add to y)

        # Remove swords that flew off the bottom of the screen
        swords_to_keep = []
        for sword in swords:
            if sword[1] < SCREEN_HEIGHT + 50:
                swords_to_keep.append(sword)
        swords = swords_to_keep

        # --- TREASURE CHESTS! ---
        # Spawn chests periodically during gameplay!
        if not game_over and game_state == "playing":
            chest_spawn_timer = chest_spawn_timer + delta_ms
        if chest_spawn_timer >= chest_spawn_rate and not game_over and game_state == "playing":
            # Time to spawn a treasure chest!
            chest_x = random.randint(50, SCREEN_WIDTH - 50)
            chest_y = -40  # Start above screen
            chest_type = random.choice(CHEST_TYPES)  # Random loot!
            chests.append([chest_x, chest_y, chest_type])
            chest_spawn_timer = 0
            print("A treasure chest appeared!")

        # Move chests down the screen
        for chest in chests:
            chest[1] = chest[1] + 2 * dt  # Float down slowly

        # Remove chests that went off screen
        chests_to_keep = []
        for chest in chests:
            if chest[1] < SCREEN_HEIGHT + 50:
                chests_to_keep.append(chest)
        chests = chests_to_keep

        # --- COLLECT CHESTS! ---
        # Check if Thrawn touches a chest!
        chests_to_remove = []
        for chest in chests:
            distance_x = abs(chest[0] - thrawn_x)
            distance_y = abs(chest[1] - thrawn_y)
            if distance_x < 40 and distance_y < 40:
                chests_to_remove.append(chest)
                # Apply the power-up based on chest type!
                loot = chest[2]
                if loot == "spread_shot":
                    has_spread_shot = True
                    print("GOT SPREAD SHOT! Shoot 3 lasers at once!")
                elif loot == "homing_missiles":
                    has_homing_missiles = True
                    print("GOT HOMING MISSILES! They track enemies!")
                elif loot == "piercing_laser":
                    has_piercing_laser = True
                    print("GOT PIERCING LASER! Goes through enemies!")
                elif loot == "double_points":
                    has_double_points = True
                    double_points_timer = 10000  # 10 seconds of double points!
                    print("GOT DOUBLE POINTS! 2x score for 10 seconds!")
                elif loot == "extra_shield":
                    shield_hits = shield_hits + 1
                    has_shield = True
                    print("GOT EXTRA SHIELD! Now have " + str(shield_hits) + " shields!")
                elif loot == "coin_bonus":
                    bonus = random.randint(50, 150)
                    coins = coins + bonus
                    save_coins(coins)
                    print("GOT " + str(bonus) + " BONUS COINS!")
                # Create a sparkle explosion!
                explosions.append([chest[0], chest[1], 400])

        for chest in chests_to_remove:
            if chest in chests:
                chests.remove(chest)

        # Update double points timer
        if has_double_points:
            double_points_timer = double_points_timer - delta_ms
            if double_points_timer <= 0:
                has_double_points = False
                print("Double points ended!")

        # --- MOVE HOMING MISSILES! ---
        # Homing missiles track the nearest Zelda!
        for missile in homing_missiles:
            # Find nearest Zelda
            nearest_dist = 99999
            target_x = missile[0]
            target_y = missile[1] - 100  # Default: go up
            for zelda in zeldas:
                dist = abs(zelda[0] - missile[0]) + abs(zelda[1] - missile[1])
                if dist < nearest_dist:
                    nearest_dist = dist
                    target_x = zelda[0]
                    target_y = zelda[1]
            # Move toward target
            dx = target_x - missile[0]
            dy = target_y - missile[1]
            dist = max(1, (dx*dx + dy*dy) ** 0.5)
            missile[0] = missile[0] + (dx / dist) * 8 * dt
            missile[1] = missile[1] + (dy / dist) * 8 * dt

        # Remove missiles that went off screen
        missiles_to_keep = []
        for missile in homing_missiles:
            if 0 < missile[0] < SCREEN_WIDTH and -50 < missile[1] < SCREEN_HEIGHT + 50:
                missiles_to_keep.append(missile)
        homing_missiles = missiles_to_keep

        # --- STAR DESTROYER BOSS! ---
        # Spawn the boss when player reaches enough points!
        if score >= boss_spawn_score and not boss_active and not boss_defeated and not game_over and game_state == "playing":
            boss_active = True
            boss_x = SCREEN_WIDTH // 2
            boss_y = -150  # Start above screen
            boss_health = boss_max_health

        # Move the boss if it's active
        if boss_active and not game_over:
            # Fly down onto the screen first
            if boss_y < 80:
                boss_y = boss_y + 2 * dt
            else:
                # --- STAR DESTROYER MOVEMENT ---
                if boss_type == "star_destroyer":
                    # Move side to side once in position
                    boss_x = boss_x + (boss_speed * boss_direction * dt)
                    # Bounce off walls
                    if boss_x <= 150:
                        boss_direction = 1
                    if boss_x >= SCREEN_WIDTH - 150:
                        boss_direction = -1

                # --- MEGA ZELDA QUEEN MOVEMENT ---
                elif boss_type == "zelda_queen":
                    # Bounces around crazily!
                    boss_x = boss_x + (boss_speed * 1.5 * boss_direction * dt)
                    if boss_x <= 100:
                        boss_direction = 1
                    if boss_x >= SCREEN_WIDTH - 100:
                        boss_direction = -1

                # --- GIANT ROBOT MOVEMENT ---
                elif boss_type == "giant_robot":
                    # Slow but menacing!
                    boss_x = boss_x + (boss_speed * 0.5 * boss_direction * dt)
                    if boss_x <= 150:
                        boss_direction = 1
                    if boss_x >= SCREEN_WIDTH - 150:
                        boss_direction = -1
                    # Rocket fist attack!
                    if not robot_fist_active and random.randint(0, 1000) < 3:
                        robot_fist_active = True
                        robot_fist_x = boss_x
                        robot_fist_y = boss_y + 50
                    if robot_fist_active:
                        robot_fist_y = robot_fist_y + 6 * dt  # Fist flies down!
                        if robot_fist_y > SCREEN_HEIGHT + 50:
                            robot_fist_active = False
                            robot_fist_y = -100

                # --- SPACE DRAGON MOVEMENT ---
                elif boss_type == "space_dragon":
                    # Swoops in circles!
                    dragon_fire_timer = dragon_fire_timer + 0.03 * dt
                    boss_x = SCREEN_WIDTH // 2 + math.sin(dragon_fire_timer) * 350
                    boss_y = 100 + math.cos(dragon_fire_timer * 0.5) * 50

                # --- SUPER DANCING 67 MOVEMENT ---
                elif boss_type == "dancing_67":
                    # Dances around the screen!
                    dance_angle = dance_angle + 0.05 * dt
                    boss_x = SCREEN_WIDTH // 2 + math.sin(dance_angle * 2) * 300
                    boss_y = 120 + math.sin(dance_angle * 3) * 40

            # Boss shoots attacks at Thrawn!
            boss_shoot_timer = boss_shoot_timer + delta_ms
            if boss_shoot_timer >= boss_shoot_rate and boss_y > 50:
                if boss_type == "star_destroyer":
                    # Shoot 3 lasers in a spread pattern!
                    boss_lasers.append([boss_x - 60, boss_y + 50, -0.2])
                    boss_lasers.append([boss_x, boss_y + 60, 0])
                    boss_lasers.append([boss_x + 60, boss_y + 50, 0.2])
                elif boss_type == "zelda_queen":
                    # Throws MEGA swords!
                    for i in range(5):  # 5 swords at once!
                        swords.append([boss_x - 80 + i * 40, boss_y + 60])
                elif boss_type == "giant_robot":
                    # Laser eyes!
                    boss_lasers.append([boss_x - 30, boss_y + 20, -0.1])
                    boss_lasers.append([boss_x + 30, boss_y + 20, 0.1])
                elif boss_type == "space_dragon":
                    # Fire breath! Many small fireballs!
                    for i in range(7):
                        angle = -0.3 + i * 0.1
                        boss_lasers.append([boss_x, boss_y + 40, angle])
                elif boss_type == "dancing_67":
                    # Disco lasers in all directions!
                    for i in range(8):
                        angle = -0.4 + i * 0.1
                        boss_lasers.append([boss_x, boss_y + 30, angle])
                boss_shoot_timer = 0

        # Move boss lasers
        for laser in boss_lasers:
            laser[1] = laser[1] + 7 * dt  # Move down
            laser[0] = laser[0] + laser[2] * 15 * dt  # Move sideways based on angle

        # Remove boss lasers that went off screen
        boss_lasers_to_keep = []
        for laser in boss_lasers:
            if laser[1] < SCREEN_HEIGHT + 50:
                boss_lasers_to_keep.append(laser)
        boss_lasers = boss_lasers_to_keep

        # --- BOSS DEFEATED ANIMATION ---
        if boss_defeated:
            boss_defeated_timer = boss_defeated_timer + delta_ms

        # --- LEVEL COMPLETE! ---
        # After beating the boss, show message then go to next level!
        if level_complete:
            level_complete_timer = level_complete_timer + delta_ms

            # After 3 seconds (3000ms), return to space to explore more planets!
            if level_complete_timer > 3000:
                # PLANET CLEARED! Back to space exploration!
                level = level + 1  # You've beaten more planets!
                level_complete = False
                level_complete_timer = 0
                boss_defeated = False
                boss_defeated_timer = 0

                # Go back to exploring space!
                game_state = "playing"
                # Center camera on player
                camera_x = player_world_x - SCREEN_WIDTH // 2
                camera_y = player_world_y - SCREEN_HEIGHT // 2

                # Reset Thrawn to starting position for next battle
                thrawn_x = SCREEN_WIDTH // 2
                thrawn_y = SCREEN_HEIGHT - 100

                # Clear any remaining stuff
                lasers = []
                zeldas = []
                swords = []
                boss_lasers = []
                explosions = []

                # Reset battle stuff for next planet
                boss_spawn_score = 500  # Boss comes after getting points
                boss_active = False
                score = 0  # Reset score for next planet battle
                lives = 3  # Fresh lives for next planet!

                # Reset difficulty for next planet
                zelda_speed = 1.5
                zelda_spawn_rate = 2000
                sword_rate = 1500
                boss_max_health = 20 + (level * 5)  # Harder on each planet!
                boss_type = "star_destroyer"  # Reset boss type


        # --- BOOM! COLLISION DETECTION ---
        # Check if any laser hits any Zelda!
        lasers_to_remove = []  # Lasers that hit something
        zeldas_to_remove = []  # Zeldas that got hit

        for laser in lasers:
            for zelda in zeldas:
                # How far apart are the laser and Zelda?
                # If they're close enough, it's a HIT!
                distance_x = abs(laser[0] - zelda[0])  # How far apart left-right
                distance_y = abs(laser[1] - zelda[1])  # How far apart up-down

                # If laser is within 30 pixels of Zelda's center = BOOM!
                if distance_x < 30 and distance_y < 30:
                    # PIERCING LASER goes through enemies! (don't remove laser)
                    if not has_piercing_laser:
                        lasers_to_remove.append(laser)
                    zeldas_to_remove.append(zelda)
                    # Create an explosion at the Zelda's position!
                    explosions.append([zelda[0], zelda[1], 500])  # 500 = how long explosion lasts
                    # Add points! DOUBLE if power-up active!
                    points = 100
                    if has_double_points:
                        points = 200
                    score = score + points

        # --- HOMING MISSILES HIT ZELDAS! ---
        missiles_to_remove = []
        for missile in homing_missiles:
            for zelda in zeldas:
                distance_x = abs(missile[0] - zelda[0])
                distance_y = abs(missile[1] - zelda[1])
                if distance_x < 30 and distance_y < 30:
                    missiles_to_remove.append(missile)
                    if zelda not in zeldas_to_remove:
                        zeldas_to_remove.append(zelda)
                    explosions.append([zelda[0], zelda[1], 500])
                    points = 100
                    if has_double_points:
                        points = 200
                    score = score + points

        # Remove missiles that hit
        for missile in missiles_to_remove:
            if missile in homing_missiles:
                homing_missiles.remove(missile)

        # Remove the lasers and Zeldas that collided
        for laser in lasers_to_remove:
            if laser in lasers:
                lasers.remove(laser)
        for zelda in zeldas_to_remove:
            if zelda in zeldas:
                zeldas.remove(zelda)

        # --- LASERS HIT THE BOSS? ---
        # Check if player's lasers hit the Star Destroyer!
        if boss_active and not boss_defeated:
            for laser in lasers:
                # Boss is big! Check if laser hits anywhere on the ship
                distance_x = abs(laser[0] - boss_x)
                distance_y = abs(laser[1] - boss_y)

                # Boss hitbox is bigger than Zeldas!
                if distance_x < 100 and distance_y < 50:
                    # Piercing laser goes through boss too!
                    if not has_piercing_laser:
                        if laser in lasers:
                            lasers.remove(laser)
                    boss_health = boss_health - 1
                    # Small explosion on the boss!
                    explosions.append([laser[0], laser[1], 300])

            # Homing missiles also hit the boss!
            for missile in homing_missiles:
                distance_x = abs(missile[0] - boss_x)
                distance_y = abs(missile[1] - boss_y)
                if distance_x < 100 and distance_y < 50:
                    if missile in homing_missiles:
                        homing_missiles.remove(missile)
                    boss_health = boss_health - 2  # Missiles do 2 damage!
                    explosions.append([missile[0], missile[1], 400])

            # Did we defeat the boss?
            if boss_health <= 0:
                boss_active = False
                boss_defeated = True
                boss_defeated_timer = 0
                # LEVEL COMPLETE! Beat the boss!
                level_complete = True
                level_complete_timer = 0
                # HUGE score bonus for defeating the boss! (double if power-up!)
                boss_bonus = 1000
                if has_double_points:
                    boss_bonus = 2000
                score = score + boss_bonus
                # Create massive explosion!
                for i in range(15):
                    ex = boss_x + random.randint(-100, 100)
                    ey = boss_y + random.randint(-50, 50)
                    explosions.append([ex, ey, 600 + random.randint(0, 300)])
                # Clear all enemies - level is done!
                zeldas = []
                swords = []
                boss_lasers = []

        # --- BOSS LASERS HIT THRAWN? ---
        # Check if boss's green lasers hit the player!
        boss_lasers_to_remove = []
        for laser in boss_lasers:
            distance_x = abs(laser[0] - thrawn_x)
            distance_y = abs(laser[1] - thrawn_y)

            if distance_x < 25 and distance_y < 30:
                boss_lasers_to_remove.append(laser)
                # SHIELD CHECK! Does the shield block it?
                if shield_hits > 0:
                    shield_hits = shield_hits - 1  # Shield takes the hit!
                    print("Shield blocked! " + str(shield_hits) + " shields left!")
                else:
                    lives = lives - 1  # No shield? Lose a life!
                explosions.append([thrawn_x, thrawn_y, 300])

        for laser in boss_lasers_to_remove:
            if laser in boss_lasers:
                boss_lasers.remove(laser)

        # --- ROBOT FIST HITS THRAWN? ---
        # Check if the Giant Robot's rocket fist hit the player!
        if robot_fist_active and boss_type == "giant_robot":
            distance_x = abs(robot_fist_x - thrawn_x)
            distance_y = abs(robot_fist_y - thrawn_y)
            if distance_x < 30 and distance_y < 40:
                robot_fist_active = False
                robot_fist_y = -100
                if shield_hits > 0:
                    shield_hits = shield_hits - 1
                    print("Shield blocked the ROCKET FIST!")
                else:
                    lives = lives - 1
                explosions.append([thrawn_x, thrawn_y, 400])

        # --- UPDATE EXPLOSIONS ---
        # Count down the explosion timers, remove old ones
        explosions_to_keep = []
        for explosion in explosions:
            explosion[2] = explosion[2] - delta_ms  # Count down the timer
            if explosion[2] > 0:  # If timer hasn't run out
                explosions_to_keep.append(explosion)
        explosions = explosions_to_keep

        # --- ZELDA HITS THRAWN? OUCH! ---
        # Check if any Zelda crashed into Thrawn!
        for zelda in zeldas:
            distance_x = abs(zelda[0] - thrawn_x)
            distance_y = abs(zelda[1] - thrawn_y)

            # If Zelda is close to Thrawn = OUCH!
            if distance_x < 40 and distance_y < 40:
                zeldas.remove(zelda)  # Remove the Zelda
                # SHIELD CHECK! Does the shield block it?
                if shield_hits > 0:
                    shield_hits = shield_hits - 1  # Shield takes the hit!
                    print("Shield blocked! " + str(shield_hits) + " shields left!")
                else:
                    lives = lives - 1  # No shield? Lose a life!
                # Make an explosion where Thrawn got hit!
                explosions.append([thrawn_x, thrawn_y, 300])

        # --- SWORD HITS THRAWN? OUCH! ---
        # Check if any sword stabbed Thrawn!
        swords_to_remove = []
        for sword in swords:
            distance_x = abs(sword[0] - thrawn_x)
            distance_y = abs(sword[1] - thrawn_y)

            # If sword is close to Thrawn = STABBED!
            if distance_x < 25 and distance_y < 30:
                swords_to_remove.append(sword)  # Remove the sword
                # SHIELD CHECK! Does the shield block it?
                if shield_hits > 0:
                    shield_hits = shield_hits - 1  # Shield takes the hit!
                    print("Shield blocked! " + str(shield_hits) + " shields left!")
                else:
                    lives = lives - 1  # No shield? Lose a life!
                # Make an explosion where Thrawn got hit!
                explosions.append([thrawn_x, thrawn_y, 300])

        # Remove swords that hit Thrawn
        for sword in swords_to_remove:
            if sword in swords:
                swords.remove(sword)

        # --- GAME OVER? ---
        # If you run out of lives, check if you have wingmen to save you!
        if lives <= 0 and not game_over:
            # DO YOU HAVE A WINGMAN? They become the new Thrawn!
            if len(wingmen) > 0:
                # A wingman sacrifices themselves to save you!
                savior = wingmen.pop(0)  # Get the first wingman
                thrawn_x = savior[0]  # Thrawn teleports to wingman position
                thrawn_y = savior[1]
                lives = 1  # You're back with 1 life!
                print("WINGMAN SAVED YOU! " + str(len(wingmen)) + " wingmen left!")
                # Make a cool effect where you got saved!
                explosions.append([thrawn_x, thrawn_y, 400])
            else:
                # No wingmen left... it's really game over!
                game_over = True
                game_over_timer = 0
                # ADD YOUR SCORE TO YOUR COINS! You keep what you earned!
                coins = coins + score
                save_coins(coins)  # Save to file so you don't lose them!
                print("You earned " + str(score) + " coins! Total: " + str(coins))
                # ROGUELIKE: Lose chest power-ups on death! (but keep coins!)
                has_spread_shot = False
                has_homing_missiles = False
                has_piercing_laser = False
                has_double_points = False
                double_points_timer = 0
                homing_missiles = []
                chests = []
                chest_spawn_timer = 0
                print("Lost all chest power-ups!")
                # Create a HUGE explosion where Thrawn was!
                # Multiple explosions spreading out from the ship!
                for i in range(8):
                    # Random positions around Thrawn for multiple explosions
                    ex = thrawn_x + random.randint(-50, 50)
                    ey = thrawn_y + random.randint(-50, 50)
                    delay = i * 100  # Stagger the explosions!
                    game_over_explosions.append([ex, ey, 800 + delay, delay])  # x, y, timer, delay

        # Update game over animation
        if game_over:
            game_over_timer = game_over_timer + delta_ms
            # After showing explosions for a while, allow going back to lobby
            if game_over_timer > 5000:
                # Press any key to go back to exploring!
                keys = pygame.key.get_pressed()
                if any(keys):
                    # RESET BATTLE and go back to space exploration!
                    game_state = "playing"
                    # Center camera on player
                    camera_x = player_world_x - SCREEN_WIDTH // 2
                    camera_y = player_world_y - SCREEN_HEIGHT // 2
                    game_over = False
                    game_over_timer = 0
                    game_over_explosions = []

                    # Reset player stats
                    score = 0
                    lives = 3
                    level = 1

                    # Reset Thrawn position
                    thrawn_x = SCREEN_WIDTH // 2
                    thrawn_y = SCREEN_HEIGHT - 100

                    # Clear all enemies and projectiles
                    lasers = []
                    zeldas = []
                    swords = []
                    boss_lasers = []
                    explosions = []

                    # Reset boss stuff
                    boss_active = False
                    boss_x = SCREEN_WIDTH // 2
                    boss_y = -150
                    boss_health = 20
                    boss_max_health = 20
                    boss_spawn_score = 500
                    boss_defeated = False
                    boss_defeated_timer = 0
                    boss_type = "star_destroyer"  # Start with Star Destroyer!
                    robot_fist_active = False
                    robot_fist_y = -100
                    dragon_fire_timer = 0
                    dance_angle = 0

                    # Reset difficulty back to normal
                    zelda_speed = 1.5  # Base speed at 60 FPS
                    zelda_spawn_rate = 2000
                    sword_rate = 1500

                    # Reset level complete
                    level_complete = False
                    level_complete_timer = 0

                    # Reset ALL power-ups for next game!
                    has_shield = False
                    shield_hits = 0
                    has_fast_shooting = False
                    has_big_laser = False
                    wingmen = []
                    wingmen_count = 0
                    big_laser_active = False
                    big_laser_timer = 0
                    big_laser_cooldown = 0
                    shoot_cooldown = 0

                    # Reset chest power-ups too!
                    has_spread_shot = False
                    has_homing_missiles = False
                    has_piercing_laser = False
                    has_double_points = False
                    double_points_timer = 0
                    homing_missiles = []
                    chests = []
                    chest_spawn_timer = 0

        # Fill the window with BLACK (like space!)
        window.fill((0, 0, 0))

        # --- DRAW THE STARS (OPTIMIZED!) ---
        # Instead of drawing 150 circles, we blit one pre-rendered surface!
        # Scroll the star surface down for parallax effect
        star_scroll_y = star_scroll_y + 2 * dt
        if star_scroll_y >= SCREEN_HEIGHT:
            star_scroll_y = star_scroll_y - SCREEN_HEIGHT

        # Blit the pre-rendered star surface (wrapping vertically)
        window.blit(star_surface, (0, int(star_scroll_y) - SCREEN_HEIGHT))

        # --- DRAW PLANETS IN THE BACKGROUND (while playing!) ---
        if game_state == "playing":
            # Draw planets in the big world!
            for planet in planets:
                # Convert world position to screen position using camera
                screen_x = int(planet[0] - camera_x)
                screen_y = int(planet[1] - camera_y)

                # Only draw if on screen
                if -100 < screen_x < SCREEN_WIDTH + 100 and -100 < screen_y < SCREEN_HEIGHT + 100:
                    size = planet[4]
                    color = planet[3]
                    discovered = planet[5]

                    if discovered:
                        # Draw the planet!
                        pygame.draw.circle(window, color, (screen_x, screen_y), size)
                        # Atmosphere glow
                        pygame.draw.circle(window, (color[0]//2, color[1]//2, color[2]//2), (screen_x, screen_y), size + 10, 3)
                        # Planet name
                        name_text = font.render(planet[2], True, (255, 255, 255))
                        name_rect = name_text.get_rect(center=(screen_x, screen_y - size - 20))
                        window.blit(name_text, name_rect)
                    else:
                        # Unknown planet - show as "?"
                        pygame.draw.circle(window, (50, 50, 50), (screen_x, screen_y), size)
                        question = font.render("?", True, (100, 100, 100))
                        q_rect = question.get_rect(center=(screen_x, screen_y))
                        window.blit(question, q_rect)

            # Draw mini-map in corner so you can see where you are!
            minimap_size = 120
            minimap_x = SCREEN_WIDTH - minimap_size - 10
            minimap_y = 10
            pygame.draw.rect(window, (20, 20, 40), (minimap_x, minimap_y, minimap_size, minimap_size))
            pygame.draw.rect(window, (100, 100, 100), (minimap_x, minimap_y, minimap_size, minimap_size), 2)

            # Draw planets on minimap
            for planet in planets:
                if planet[5]:  # Only show discovered planets
                    mm_x = minimap_x + int((planet[0] / WORLD_WIDTH) * minimap_size)
                    mm_y = minimap_y + int((planet[1] / WORLD_HEIGHT) * minimap_size)
                    pygame.draw.circle(window, planet[3], (mm_x, mm_y), 3)

            # Draw player on minimap
            mm_px = minimap_x + int((player_world_x / WORLD_WIDTH) * minimap_size)
            mm_py = minimap_y + int((player_world_y / WORLD_HEIGHT) * minimap_size)
            pygame.draw.circle(window, (0, 255, 255), (mm_px, mm_py), 3)

        # --- DRAW THE TITLE SCREEN ---
        # Show the epic opening screen before the game starts!
        if game_state == "title":
            # --- STAR DESTROYER in the background! ---
            # It floats at the top, looking menacing!
            title_boss_x = SCREEN_WIDTH // 2
            title_boss_y = 120 + math.sin(title_timer / 1000) * 10  # Gentle floating!

            # Main body - big gray triangle (like a Star Destroyer!)
            pygame.draw.polygon(window, (80, 80, 90), [
                (title_boss_x, title_boss_y - 40),
                (title_boss_x - 120, title_boss_y + 40),
                (title_boss_x + 120, title_boss_y + 40)
            ])
            # Bridge tower
            pygame.draw.polygon(window, (60, 60, 70), [
                (title_boss_x - 20, title_boss_y + 10),
                (title_boss_x + 20, title_boss_y + 10),
                (title_boss_x + 15, title_boss_y - 10),
                (title_boss_x - 15, title_boss_y - 10)
            ])
            # Bridge windows (glowing)
            pygame.draw.rect(window, (255, 255, 100), (title_boss_x - 10, title_boss_y - 5, 20, 5))
            # Engine glow
            pygame.draw.circle(window, (100, 150, 255), (title_boss_x - 60, title_boss_y + 40), 12)
            pygame.draw.circle(window, (100, 150, 255), (title_boss_x, title_boss_y + 40), 15)
            pygame.draw.circle(window, (100, 150, 255), (title_boss_x + 60, title_boss_y + 40), 12)

            # --- ANGRY ZELDAS on the sides! ---
            # Left Zelda - bobbing up and down!
            zelda1_x = 200
            zelda1_y = 350 + math.sin(title_timer / 600) * 20

            # Hair!
            hair_color = (180, 130, 50)
            pygame.draw.line(window, hair_color, (zelda1_x - 20, zelda1_y), (zelda1_x - 25, zelda1_y + 60), 4)
            pygame.draw.line(window, hair_color, (zelda1_x, zelda1_y + 10), (zelda1_x, zelda1_y + 75), 4)
            pygame.draw.line(window, hair_color, (zelda1_x + 20, zelda1_y), (zelda1_x + 25, zelda1_y + 60), 4)
            # Green head
            pygame.draw.circle(window, (0, 200, 0), (int(zelda1_x), int(zelda1_y)), 25)
            # Crown!
            pygame.draw.polygon(window, (255, 215, 0), [
                (zelda1_x - 20, zelda1_y - 20), (zelda1_x - 15, zelda1_y - 35),
                (zelda1_x - 7, zelda1_y - 25), (zelda1_x, zelda1_y - 40),
                (zelda1_x + 7, zelda1_y - 25), (zelda1_x + 15, zelda1_y - 35),
                (zelda1_x + 20, zelda1_y - 20)
            ])
            pygame.draw.circle(window, (255, 0, 0), (int(zelda1_x), int(zelda1_y - 30)), 4)
            # Angry face!
            pygame.draw.line(window, (0, 0, 0), (zelda1_x - 15, zelda1_y - 10), (zelda1_x - 5, zelda1_y - 5), 3)
            pygame.draw.line(window, (0, 0, 0), (zelda1_x + 15, zelda1_y - 10), (zelda1_x + 5, zelda1_y - 5), 3)
            pygame.draw.circle(window, (0, 0, 0), (int(zelda1_x - 10), int(zelda1_y)), 4)
            pygame.draw.circle(window, (0, 0, 0), (int(zelda1_x + 10), int(zelda1_y)), 4)
            pygame.draw.arc(window, (0, 0, 0), (zelda1_x - 10, zelda1_y + 5, 20, 10), 3.14, 6.28, 3)

            # Right Zelda - bobbing opposite!
            zelda2_x = SCREEN_WIDTH - 200
            zelda2_y = 350 + math.cos(title_timer / 600) * 20

            # Hair!
            pygame.draw.line(window, hair_color, (zelda2_x - 20, zelda2_y), (zelda2_x - 25, zelda2_y + 60), 4)
            pygame.draw.line(window, hair_color, (zelda2_x, zelda2_y + 10), (zelda2_x, zelda2_y + 75), 4)
            pygame.draw.line(window, hair_color, (zelda2_x + 20, zelda2_y), (zelda2_x + 25, zelda2_y + 60), 4)
            # Green head
            pygame.draw.circle(window, (0, 200, 0), (int(zelda2_x), int(zelda2_y)), 25)
            # Crown!
            pygame.draw.polygon(window, (255, 215, 0), [
                (zelda2_x - 20, zelda2_y - 20), (zelda2_x - 15, zelda2_y - 35),
                (zelda2_x - 7, zelda2_y - 25), (zelda2_x, zelda2_y - 40),
                (zelda2_x + 7, zelda2_y - 25), (zelda2_x + 15, zelda2_y - 35),
                (zelda2_x + 20, zelda2_y - 20)
            ])
            pygame.draw.circle(window, (255, 0, 0), (int(zelda2_x), int(zelda2_y - 30)), 4)
            # Angry face!
            pygame.draw.line(window, (0, 0, 0), (zelda2_x - 15, zelda2_y - 10), (zelda2_x - 5, zelda2_y - 5), 3)
            pygame.draw.line(window, (0, 0, 0), (zelda2_x + 15, zelda2_y - 10), (zelda2_x + 5, zelda2_y - 5), 3)
            pygame.draw.circle(window, (0, 0, 0), (int(zelda2_x - 10), int(zelda2_y)), 4)
            pygame.draw.circle(window, (0, 0, 0), (int(zelda2_x + 10), int(zelda2_y)), 4)
            pygame.draw.arc(window, (0, 0, 0), (zelda2_x - 10, zelda2_y + 5, 20, 10), 3.14, 6.28, 3)

            # --- THE GAME TITLE! ---
            # "IN OUTSIDERELM" with a pre-rendered glowing effect!
            # Just blit the pre-rendered glow surface (MUCH faster!)
            title_rect = title_glow_surface.get_rect(center=(SCREEN_WIDTH // 2, 280))
            window.blit(title_glow_surface, title_rect)

            # --- CONTROLS INFO ---
            controls1 = font.render("WASD/ARROWS = Move   SHIFT = Run", True, (200, 200, 200))
            controls1_rect = controls1.get_rect(center=(SCREEN_WIDTH // 2, 520))
            window.blit(controls1, controls1_rect)

            controls2 = font.render("Explore space, discover planets, battle Zeldas!", True, (255, 100, 100))
            controls2_rect = controls2.get_rect(center=(SCREEN_WIDTH // 2, 560))
            window.blit(controls2, controls2_rect)

            # --- PRESS ENTER TO START! ---
            # This text blinks by changing visibility based on timer!
            if (int(title_timer) // 500) % 2 == 0:  # Blink every 500ms!
                start_text = medium_font.render("PRESS ENTER TO PLAY!", True, (255, 255, 0))
                start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 650))
                window.blit(start_text, start_rect)

            # Show how many coins you have!
            coins_text = font.render("COINS: " + str(coins), True, (255, 215, 0))
            coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, 700))
            window.blit(coins_text, coins_rect)

        # --- DRAW THE SHOP SCREEN! ---
        # The awesome shop where you buy power-ups!
        if game_state == "shop":
            # Cool shop title!
            shop_title = big_font.render("SHOP", True, (255, 215, 0))
            shop_title_rect = shop_title.get_rect(center=(SCREEN_WIDTH // 2, 60))
            window.blit(shop_title, shop_title_rect)

            # Show your coins in the corner!
            coins_display = medium_font.render("COINS: " + str(coins), True, (255, 215, 0))
            window.blit(coins_display, (20, 20))

            # Draw each shop item! (centered on the bigger screen)
            shop_left = (SCREEN_WIDTH - 800) // 2  # Center the shop box
            for i in range(len(shop_items)):
                item = shop_items[i]
                y_pos = 150 + i * 90  # More space between items

                # Is this item selected? Make it glow!
                if i == shop_selection:
                    # Draw a glowing box around the selected item!
                    pygame.draw.rect(window, item["color"], (shop_left, y_pos - 10, 800, 70), 3)
                    text_color = item["color"]
                else:
                    text_color = (150, 150, 150)  # Gray for unselected

                # Item name
                name_text = font.render(item["name"], True, text_color)
                window.blit(name_text, (shop_left + 20, y_pos))

                # Item description
                desc_text = font.render(item["desc"], True, (100, 100, 100))
                window.blit(desc_text, (shop_left + 20, y_pos + 30))

                # Item price (except for START GAME)
                if item["price"] > 0:
                    price_text = font.render(str(item["price"]) + " coins", True, (255, 215, 0))
                    window.blit(price_text, (shop_left + 600, y_pos))

                    # Show if you already own it!
                    if item["name"] == "FAST SHOOTING" and has_fast_shooting:
                        owned_text = font.render("OWNED!", True, (0, 255, 0))
                        window.blit(owned_text, (shop_left + 600, y_pos + 30))
                    elif item["name"] == "BIG LASER" and has_big_laser:
                        owned_text = font.render("OWNED!", True, (0, 255, 0))
                        window.blit(owned_text, (shop_left + 600, y_pos + 30))
                    elif item["name"] == "SHIELD" and shield_hits > 0:
                        owned_text = font.render("x" + str(shield_hits), True, (0, 255, 0))
                        window.blit(owned_text, (shop_left + 600, y_pos + 30))
                    elif item["name"] == "WINGMAN" and wingmen_count > 0:
                        owned_text = font.render("x" + str(wingmen_count), True, (0, 255, 0))
                        window.blit(owned_text, (shop_left + 600, y_pos + 30))

            # Instructions at the bottom!
            instr1 = font.render("UP/DOWN = Select    ENTER = Buy", True, (200, 200, 200))
            instr1_rect = instr1.get_rect(center=(SCREEN_WIDTH // 2, 720))
            window.blit(instr1, instr1_rect)

        # --- DRAW THE EXPLOSIONS ---
        # Big colorful BOOM when Zeldas get hit!
        for explosion in explosions:
            ex = int(explosion[0])  # Explosion x position
            ey = int(explosion[1])  # Explosion y position
            timer = explosion[2]    # How much time left

            # Make the explosion shrink as time runs out (cool effect!)
            size = int(timer / 10) + 10  # Starts big, gets smaller

            # Draw colorful explosion circles!
            pygame.draw.circle(window, (255, 100, 0), (ex, ey), size)       # Orange outer
            pygame.draw.circle(window, (255, 255, 0), (ex, ey), size - 10)  # Yellow middle
            pygame.draw.circle(window, (255, 255, 255), (ex, ey), size - 20) # White center

        # --- DRAW THE LASERS ---
        # Draw each laser as a RED rectangle (like a laser beam!)
        for laser in lasers:
            # pygame.draw.rect needs: window, color, (x, y, width, height)
            # laser[0] is x position, laser[1] is y position
            # PIERCING LASER is BLUE and longer!
            if has_piercing_laser:
                pygame.draw.rect(window, (0, 200, 255), (laser[0] - 3, laser[1], 6, 25))
            else:
                pygame.draw.rect(window, (255, 0, 0), (laser[0] - 2, laser[1], 4, 15))

        # --- DRAW HOMING MISSILES! ---
        # Orange missiles that track enemies!
        for missile in homing_missiles:
            mx = int(missile[0])
            my = int(missile[1])
            # Missile body (orange)
            pygame.draw.ellipse(window, (255, 150, 0), (mx - 4, my - 8, 8, 16))
            # Missile tip (red)
            pygame.draw.polygon(window, (255, 50, 0), [
                (mx, my - 12), (mx - 4, my - 6), (mx + 4, my - 6)
            ])
            # Flame trail
            pygame.draw.polygon(window, (255, 255, 0), [
                (mx - 3, my + 8), (mx, my + 15), (mx + 3, my + 8)
            ])

        # --- DRAW TREASURE CHESTS! ---
        # Golden chests floating down with goodies inside!
        for chest in chests:
            cx = int(chest[0])
            cy = int(chest[1])
            # Chest body (brown wood)
            pygame.draw.rect(window, (139, 90, 43), (cx - 20, cy - 12, 40, 24))
            # Chest lid (darker wood)
            pygame.draw.rect(window, (100, 60, 30), (cx - 22, cy - 18, 44, 10))
            # Gold trim
            pygame.draw.rect(window, (255, 215, 0), (cx - 22, cy - 8, 44, 4))
            # Gold lock
            pygame.draw.circle(window, (255, 215, 0), (cx, cy), 6)
            pygame.draw.circle(window, (200, 150, 0), (cx, cy), 3)
            # Sparkle effect!
            sparkle = int(title_timer / 200) % 4
            if sparkle == 0:
                pygame.draw.circle(window, (255, 255, 255), (cx - 15, cy - 15), 3)
            elif sparkle == 1:
                pygame.draw.circle(window, (255, 255, 255), (cx + 15, cy - 10), 3)
            elif sparkle == 2:
                pygame.draw.circle(window, (255, 255, 255), (cx + 10, cy + 5), 3)

        # --- DRAW THE BIG LASER (MEGA BEAM!) ---
        # A massive beam of destruction from Thrawn to the top of the screen!
        if big_laser_active and not game_over:
            # The beam flickers and pulses for a cool effect!
            flicker = random.randint(-5, 5)
            beam_width = 40 + flicker

            # Draw multiple layers for a glowing effect!
            # Outer red glow
            pygame.draw.rect(window, (255, 50, 50), (int(thrawn_x) - beam_width - 10, 0, (beam_width + 10) * 2, int(thrawn_y) - 30))
            # Middle orange layer
            pygame.draw.rect(window, (255, 150, 0), (int(thrawn_x) - beam_width, 0, beam_width * 2, int(thrawn_y) - 30))
            # Inner yellow layer
            pygame.draw.rect(window, (255, 255, 0), (int(thrawn_x) - beam_width + 10, 0, (beam_width - 10) * 2, int(thrawn_y) - 30))
            # White hot center!
            pygame.draw.rect(window, (255, 255, 255), (int(thrawn_x) - 15, 0, 30, int(thrawn_y) - 30))

        # --- DRAW THE SWORDS ---
        # Draw each sword as a silver blade with a golden handle!
        for sword in swords:
            sx = int(sword[0])  # Sword x position
            sy = int(sword[1])  # Sword y position

            # Silver blade (pointy triangle pointing down!)
            pygame.draw.polygon(window, (192, 192, 192), [
                (sx, sy + 20),       # Point at bottom (tip of sword!)
                (sx - 4, sy - 5),    # Top left of blade
                (sx + 4, sy - 5)     # Top right of blade
            ])

            # Golden handle/hilt (crossguard)
            pygame.draw.rect(window, (255, 215, 0), (sx - 8, sy - 8, 16, 4))  # Crossguard

            # Brown grip
            pygame.draw.rect(window, (139, 69, 19), (sx - 2, sy - 15, 4, 8))  # Handle

        # --- DRAW BOSS LASERS ---
        # Green laser beams from the Star Destroyer!
        for laser in boss_lasers:
            lx = int(laser[0])
            ly = int(laser[1])
            # Green glowing laser!
            pygame.draw.rect(window, (0, 255, 0), (lx - 3, ly, 6, 20))
            pygame.draw.rect(window, (150, 255, 150), (lx - 1, ly + 2, 2, 16))  # Bright center

        # --- DRAW THE BOSS ---
        if boss_active or boss_defeated_timer > 0:
            bx = int(boss_x)
            by = int(boss_y)

            # === STAR DESTROYER ===
            if boss_type == "star_destroyer":
                # Main body - big gray triangle!
                pygame.draw.polygon(window, (80, 80, 90), [
                    (bx, by - 40), (bx - 120, by + 40), (bx + 120, by + 40)
                ])
                # Bridge tower
                pygame.draw.polygon(window, (60, 60, 70), [
                    (bx - 20, by + 10), (bx + 20, by + 10), (bx + 15, by - 10), (bx - 15, by - 10)
                ])
                pygame.draw.rect(window, (255, 255, 100), (bx - 10, by - 5, 20, 5))
                # Engines
                pygame.draw.circle(window, (100, 150, 255), (bx - 60, by + 40), 12)
                pygame.draw.circle(window, (100, 150, 255), (bx, by + 40), 15)
                pygame.draw.circle(window, (100, 150, 255), (bx + 60, by + 40), 12)
                boss_name = "STAR DESTROYER"

            # === MEGA ZELDA QUEEN ===
            elif boss_type == "zelda_queen":
                # HUGE green head!
                pygame.draw.circle(window, (0, 180, 0), (bx, by), 60)
                # SUPER long hair!
                for i in range(-3, 4):
                    pygame.draw.line(window, (255, 200, 50), (bx + i * 20, by), (bx + i * 25, by + 120), 6)
                # MEGA CROWN!
                pygame.draw.polygon(window, (255, 215, 0), [
                    (bx - 50, by - 50), (bx - 35, by - 90), (bx - 20, by - 60),
                    (bx, by - 100), (bx + 20, by - 60), (bx + 35, by - 90), (bx + 50, by - 50)
                ])
                # Big jewels!
                pygame.draw.circle(window, (255, 0, 0), (bx, by - 75), 10)
                pygame.draw.circle(window, (0, 0, 255), (bx - 30, by - 65), 6)
                pygame.draw.circle(window, (0, 0, 255), (bx + 30, by - 65), 6)
                # ANGRY eyes!
                pygame.draw.line(window, (0, 0, 0), (bx - 35, by - 20), (bx - 15, by - 10), 5)
                pygame.draw.line(window, (0, 0, 0), (bx + 35, by - 20), (bx + 15, by - 10), 5)
                pygame.draw.circle(window, (255, 0, 0), (bx - 25, by), 12)  # Evil red eyes!
                pygame.draw.circle(window, (255, 0, 0), (bx + 25, by), 12)
                # Angry mouth!
                pygame.draw.arc(window, (0, 0, 0), (bx - 30, by + 15, 60, 30), 3.14, 6.28, 5)
                boss_name = "MEGA ZELDA QUEEN"

            # === GIANT ROBOT ===
            elif boss_type == "giant_robot":
                # Robot body (gray metal box!)
                pygame.draw.rect(window, (100, 100, 120), (bx - 60, by - 40, 120, 80))
                # Robot head
                pygame.draw.rect(window, (80, 80, 100), (bx - 30, by - 70, 60, 35))
                # LASER EYES!
                eye_glow = random.randint(200, 255)
                pygame.draw.circle(window, (eye_glow, 0, 0), (bx - 15, by - 55), 10)
                pygame.draw.circle(window, (eye_glow, 0, 0), (bx + 15, by - 55), 10)
                # Arms
                pygame.draw.rect(window, (70, 70, 90), (bx - 80, by - 20, 25, 60))
                pygame.draw.rect(window, (70, 70, 90), (bx + 55, by - 20, 25, 60))
                # Antenna
                pygame.draw.line(window, (150, 150, 150), (bx, by - 70), (bx, by - 90), 3)
                pygame.draw.circle(window, (255, 0, 0), (bx, by - 90), 5)
                boss_name = "GIANT ROBOT"
                # Draw rocket fist if active!
                if robot_fist_active:
                    fx = int(robot_fist_x)
                    fy = int(robot_fist_y)
                    pygame.draw.rect(window, (150, 150, 170), (fx - 15, fy, 30, 40))
                    pygame.draw.circle(window, (255, 150, 0), (fx - 10, fy + 40), 8)
                    pygame.draw.circle(window, (255, 150, 0), (fx + 10, fy + 40), 8)

            # === SPACE DRAGON ===
            elif boss_type == "space_dragon":
                # Dragon body (purple!)
                pygame.draw.ellipse(window, (150, 50, 200), (bx - 70, by - 30, 140, 60))
                # Dragon head
                pygame.draw.circle(window, (170, 60, 220), (bx + 60, by - 10), 35)
                # Dragon eyes (yellow!)
                pygame.draw.circle(window, (255, 255, 0), (bx + 70, by - 20), 10)
                pygame.draw.circle(window, (0, 0, 0), (bx + 72, by - 20), 5)
                # Dragon wings!
                pygame.draw.polygon(window, (200, 80, 255), [
                    (bx - 30, by - 20), (bx - 100, by - 80), (bx - 60, by + 10)
                ])
                pygame.draw.polygon(window, (200, 80, 255), [
                    (bx + 10, by - 20), (bx + 60, by - 80), (bx + 30, by + 10)
                ])
                # Dragon horns!
                pygame.draw.polygon(window, (100, 30, 130), [
                    (bx + 50, by - 40), (bx + 40, by - 70), (bx + 60, by - 35)
                ])
                pygame.draw.polygon(window, (100, 30, 130), [
                    (bx + 80, by - 40), (bx + 90, by - 70), (bx + 70, by - 35)
                ])
                # Fire mouth!
                if boss_shoot_timer > boss_shoot_rate - 100:
                    pygame.draw.polygon(window, (255, 100, 0), [
                        (bx + 85, by), (bx + 130, by + 30), (bx + 85, by + 20)
                    ])
                boss_name = "SPACE DRAGON"

            # === SUPER DANCING 67 ===
            elif boss_type == "dancing_67":
                # Dancing robot body! Changes color!
                dance_color_r = int(127 + 127 * math.sin(dance_angle * 5))
                dance_color_g = int(127 + 127 * math.sin(dance_angle * 5 + 2))
                dance_color_b = int(127 + 127 * math.sin(dance_angle * 5 + 4))
                # Body
                pygame.draw.rect(window, (dance_color_r, dance_color_g, dance_color_b), (bx - 40, by - 30, 80, 60))
                # Head with disco ball effect!
                pygame.draw.circle(window, (200, 200, 200), (bx, by - 50), 25)
                # Disco sparkles!
                for i in range(8):
                    sparkle_angle = dance_angle * 3 + i * 0.8
                    sx = bx + math.cos(sparkle_angle) * 20
                    sy = by - 50 + math.sin(sparkle_angle) * 20
                    pygame.draw.circle(window, (255, 255, 255), (int(sx), int(sy)), 3)
                # Dancing arms!
                arm_wave = math.sin(dance_angle * 10) * 30
                pygame.draw.line(window, (dance_color_r, dance_color_g, dance_color_b),
                               (bx - 40, by), (bx - 70, by - 20 + arm_wave), 8)
                pygame.draw.line(window, (dance_color_r, dance_color_g, dance_color_b),
                               (bx + 40, by), (bx + 70, by - 20 - arm_wave), 8)
                # Dancing legs!
                leg_wave = math.sin(dance_angle * 10 + 1.5) * 20
                pygame.draw.line(window, (dance_color_r, dance_color_g, dance_color_b),
                               (bx - 20, by + 30), (bx - 30 + leg_wave, by + 70), 8)
                pygame.draw.line(window, (dance_color_r, dance_color_g, dance_color_b),
                               (bx + 20, by + 30), (bx + 30 - leg_wave, by + 70), 8)
                # "67" on its chest!
                text_67 = font.render("67", True, (255, 255, 255))
                text_rect = text_67.get_rect(center=(bx, by))
                window.blit(text_67, text_rect)
                boss_name = "SUPER DANCING 67"

            # --- BOSS HEALTH BAR (for all bosses!) ---
            if boss_active:
                bar_width = 150
                bar_height = 10
                bar_x = bx - bar_width // 2
                bar_y = by - 100 if boss_type != "star_destroyer" else by - 60

                pygame.draw.rect(window, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
                health_width = int((boss_health / boss_max_health) * bar_width)
                pygame.draw.rect(window, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))
                pygame.draw.rect(window, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

                boss_label = font.render(boss_name, True, (255, 255, 255))
                label_rect = boss_label.get_rect(center=(bx, bar_y - 15))
                window.blit(boss_label, label_rect)

        # --- DRAW THE ANGRY ZELDAS ---
        # Each Zelda is a green circle with an angry face, long hair, and a crown!
        for zelda in zeldas:
            zx = zelda[0]  # Zelda's x position (easier to type!)
            zy = zelda[1]  # Zelda's y position

            # SUPER LONG HAIR! (flows down behind the head)
            # Brown/blonde hair lines going way down!
            hair_color = (180, 130, 50)  # Golden brown hair!
            pygame.draw.line(window, hair_color, (zx - 20, zy), (zx - 25, zy + 60), 4)  # Left hair
            pygame.draw.line(window, hair_color, (zx - 10, zy + 5), (zx - 15, zy + 70), 4)  # Left-middle
            pygame.draw.line(window, hair_color, (zx, zy + 10), (zx, zy + 75), 4)  # Middle hair
            pygame.draw.line(window, hair_color, (zx + 10, zy + 5), (zx + 15, zy + 70), 4)  # Right-middle
            pygame.draw.line(window, hair_color, (zx + 20, zy), (zx + 25, zy + 60), 4)  # Right hair

            # Green circle body (the head!)
            pygame.draw.circle(window, (0, 200, 0), (int(zx), int(zy)), 25)
            # (0, 200, 0) = GREEN!

            # GOLDEN CROWN! (on top of the head!)
            crown_color = (255, 215, 0)  # GOLD!
            # Crown is a polygon with pointy tips!
            pygame.draw.polygon(window, crown_color, [
                (zx - 20, zy - 20),  # Bottom left
                (zx - 15, zy - 35),  # Left point
                (zx - 7, zy - 25),   # Left dip
                (zx, zy - 40),       # Middle point (tallest!)
                (zx + 7, zy - 25),   # Right dip
                (zx + 15, zy - 35),  # Right point
                (zx + 20, zy - 20),  # Bottom right
            ])
            # Little red jewel in the crown!
            pygame.draw.circle(window, (255, 0, 0), (int(zx), int(zy - 30)), 4)

            # Angry eyebrows! (two lines that make a V shape)
            pygame.draw.line(window, (0, 0, 0), (zx - 15, zy - 10), (zx - 5, zy - 5), 3)  # Left eyebrow
            pygame.draw.line(window, (0, 0, 0), (zx + 15, zy - 10), (zx + 5, zy - 5), 3)  # Right eyebrow

            # Angry eyes! (black dots under the eyebrows)
            pygame.draw.circle(window, (0, 0, 0), (int(zx - 10), int(zy)), 4)  # Left eye
            pygame.draw.circle(window, (0, 0, 0), (int(zx + 10), int(zy)), 4)  # Right eye

            # Angry frown! (a curved line going down)
            pygame.draw.arc(window, (0, 0, 0), (zx - 10, zy + 5, 20, 10), 3.14, 6.28, 3)
            # This draws the bottom half of a circle = a frown!

        # --- DRAW THRAWN ---
        # Only draw Thrawn if the game is NOT over (he exploded!)
        if not game_over:
            # SHIELD BUBBLE! Draw it behind Thrawn if you have shields!
            if shield_hits > 0:
                # Glowing blue bubble around Thrawn!
                # Outer glow
                pygame.draw.circle(window, (50, 100, 200), (int(thrawn_x), int(thrawn_y)), 45, 3)
                # Inner bubble (semi-transparent look with multiple circles)
                pygame.draw.circle(window, (100, 150, 255), (int(thrawn_x), int(thrawn_y)), 42, 2)
                pygame.draw.circle(window, (150, 200, 255), (int(thrawn_x), int(thrawn_y)), 38, 1)

            # Blue triangle spaceship body (3 points make a triangle!)
            # Point 1: top (nose of ship), Point 2: bottom-left, Point 3: bottom-right
            pygame.draw.polygon(window, (0, 100, 255), [
                (thrawn_x, thrawn_y - 30),      # Top point (nose)
                (thrawn_x - 25, thrawn_y + 20), # Bottom-left
                (thrawn_x + 25, thrawn_y + 20)  # Bottom-right
            ])
            # Red glowing eyes!
            pygame.draw.circle(window, (255, 0, 0), (thrawn_x - 8, thrawn_y), 5)  # Left eye
            pygame.draw.circle(window, (255, 0, 0), (thrawn_x + 8, thrawn_y), 5)  # Right eye

        # --- DRAW THE WINGMEN ---
        # Your fleet of buddy ships that fight alongside Thrawn!
        if game_state == "playing":
            for wingman in wingmen:
                wx = int(wingman[0])
                wy = int(wingman[1])

                # Green triangle ship (smaller than Thrawn!)
                pygame.draw.polygon(window, (0, 200, 100), [
                    (wx, wy - 20),        # Top point (nose)
                    (wx - 15, wy + 12),   # Bottom-left
                    (wx + 15, wy + 12)    # Bottom-right
                ])
                # Little white eyes!
                pygame.draw.circle(window, (255, 255, 255), (wx - 5, wy - 5), 3)
                pygame.draw.circle(window, (255, 255, 255), (wx + 5, wy - 5), 3)

        # --- DRAW LEVEL COMPLETE! ---
        # When you beat the boss, show an awesome message!
        if level_complete:
            # Use pre-rendered glow surface (MUCH faster!)
            complete_rect = level_complete_surface.get_rect(center=(SCREEN_WIDTH // 2, 250))
            window.blit(level_complete_surface, complete_rect)

            # Show what level is next!
            next_text = medium_font.render("Get ready for LEVEL " + str(level + 1) + "!", True, (255, 255, 0))
            next_rect = next_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
            window.blit(next_text, next_rect)

            # Show score
            score_msg = font.render("Score: " + str(score), True, (255, 255, 255))
            score_rect = score_msg.get_rect(center=(SCREEN_WIDTH // 2, 380))
            window.blit(score_msg, score_rect)

        # --- DRAW GAME OVER FART CLOUDS ---
        # When the game is over, show STINKY fart clouds!
        if game_over:
            # Update and draw the fart clouds
            explosions_still_going = []
            for explosion in game_over_explosions:
                ex = int(explosion[0])
                ey = int(explosion[1])
                timer = explosion[2]
                delay = explosion[3]

                # Only start showing after delay
                if game_over_timer > delay:
                    timer = timer - 1
                    explosion[2] = timer

                    if timer > 0:
                        # STINKY fart clouds! They grow and float up!
                        size = int(timer / 6) + 30  # Big puffy clouds!
                        float_up = int((800 - timer) / 10)  # Float upward!

                        # Draw multiple puffy cloud circles (green/brown fart colors!)
                        # Outer dark green stink cloud
                        pygame.draw.circle(window, (80, 120, 40), (ex - 10, ey - float_up), size)
                        pygame.draw.circle(window, (80, 120, 40), (ex + 15, ey - float_up - 5), size - 10)
                        # Middle gross yellow-green
                        pygame.draw.circle(window, (150, 180, 50), (ex, ey - float_up), size - 15)
                        pygame.draw.circle(window, (150, 180, 50), (ex + 10, ey - float_up + 5), size - 20)
                        # Inner lighter green puff
                        pygame.draw.circle(window, (180, 200, 100), (ex - 5, ey - float_up), size - 30)

                        explosions_still_going.append(explosion)
                else:
                    explosions_still_going.append(explosion)

            game_over_explosions = explosions_still_going

            # Draw stink lines! (wavy lines rising up)
            if game_over_timer > 200:
                for i in range(5):
                    stink_x = thrawn_x - 40 + (i * 20)
                    wave = math.sin(game_over_timer / 200 + i) * 10
                    stink_y = thrawn_y - (game_over_timer / 20) - (i * 30)
                    if stink_y > 50:
                        pygame.draw.line(window, (100, 150, 50),
                                       (stink_x + wave, stink_y),
                                       (stink_x - wave, stink_y - 30), 3)

            # Show GAME OVER text after farts start
            if game_over_timer > 500:
                # Draw "GAME OVER" in big green stinky letters!
                game_over_text = big_font.render("GAME OVER", True, (100, 180, 50))
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
                window.blit(game_over_text, text_rect)

                # Funny fart message!
                fart_text = medium_font.render("* PFFFFFTTT *", True, (150, 200, 80))
                fart_rect = fart_text.get_rect(center=(SCREEN_WIDTH // 2, 310))
                window.blit(fart_text, fart_rect)

                # Show final score!
                final_score_text = medium_font.render("Final Score: " + str(score), True, (255, 255, 255))
                score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, 370))
                window.blit(final_score_text, score_rect)

            # Show "Press any key" after a bit
            if game_over_timer > 3000:
                press_key_text = font.render("Press any key to return to space", True, (150, 150, 150))
                key_rect = press_key_text.get_rect(center=(SCREEN_WIDTH // 2, 430))
                window.blit(press_key_text, key_rect)

        # --- DRAW SCORE AND LIVES ---
        # Only show score/lives when playing (not on title screen!)
        if game_state == "playing":
            # Show the score in the top left!
            score_text = font.render("SCORE: " + str(score), True, (255, 255, 255))
            window.blit(score_text, (10, 10))  # Put it at top-left corner

            # Show current level in the middle!
            level_text = font.render("LEVEL " + str(level), True, (0, 255, 255))
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
            window.blit(level_text, level_rect)

            # Show lives in the top right!
            lives_text = font.render("LIVES: " + str(lives), True, (255, 0, 0))
            window.blit(lives_text, (SCREEN_WIDTH - 120, 10))  # Put it at top-right corner

            # --- POWER-UP DISPLAY ---
            # Show what power-ups are active!
            powerup_y = 40  # Start below the score

            # Show shields
            if shield_hits > 0:
                shield_text = font.render("SHIELDS: " + str(shield_hits), True, (100, 200, 255))
                window.blit(shield_text, (10, powerup_y))
                powerup_y = powerup_y + 25

            # Show wingmen count
            if len(wingmen) > 0:
                wingmen_text = font.render("WINGMEN: " + str(len(wingmen)), True, (0, 255, 100))
                window.blit(wingmen_text, (10, powerup_y))
                powerup_y = powerup_y + 25

            # Show big laser status
            if has_big_laser:
                if big_laser_cooldown > 0:
                    laser_text = font.render("MEGA BEAM: Charging...", True, (150, 150, 0))
                else:
                    laser_text = font.render("MEGA BEAM: READY! (B)", True, (255, 255, 0))
                window.blit(laser_text, (10, powerup_y))
                powerup_y = powerup_y + 25

            # --- CHEST POWER-UPS! ---
            # Show temporary power-ups from chests (right side of screen)
            chest_y = 40
            if has_spread_shot:
                spread_text = font.render("SPREAD SHOT!", True, (255, 100, 100))
                window.blit(spread_text, (SCREEN_WIDTH - 180, chest_y))
                chest_y = chest_y + 25
            if has_homing_missiles:
                homing_text = font.render("HOMING MISSILES!", True, (255, 150, 0))
                window.blit(homing_text, (SCREEN_WIDTH - 200, chest_y))
                chest_y = chest_y + 25
            if has_piercing_laser:
                pierce_text = font.render("PIERCING LASER!", True, (0, 200, 255))
                window.blit(pierce_text, (SCREEN_WIDTH - 185, chest_y))
                chest_y = chest_y + 25
            if has_double_points:
                secs_left = int(double_points_timer / 1000)
                double_text = font.render("2X POINTS! " + str(secs_left) + "s", True, (255, 255, 0))
                window.blit(double_text, (SCREEN_WIDTH - 170, chest_y))
                chest_y = chest_y + 25

        # Show everything on screen
        pygame.display.flip()

        # Control game speed - only use clock.tick on desktop
        # On web, the browser handles timing via requestAnimationFrame
        if not IS_WEB:
            clock.tick(FPS)

    # Turn off Pygame when done
    pygame.quit()

asyncio.run(main())
