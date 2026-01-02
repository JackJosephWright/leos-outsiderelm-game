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

# --- COINS (ROGUELIKE MODE!) ---
# No saving between runs! See how far you can get!
save_file = "save_data.json"  # Only saves skins, not progress!
STARTING_COINS = 100  # Everyone starts with 100 coins each run!

# Function to load skin data from save file!
def load_skins():
    if os.path.exists(save_file):
        try:
            with open(save_file, "r") as f:
                data = json.load(f)
                saved_skin = data.get("current_skin", "thrawn")
                saved_owned = data.get("owned_skins", ["thrawn"])
                return saved_skin, saved_owned
        except:
            return "thrawn", ["thrawn"]
    return "thrawn", ["thrawn"]

# No save_coins function anymore - roguelike mode!

# Function to save skin data!
def save_skins(skin_name, owned_list):
    # Load existing data first so we don't lose coin info!
    existing_data = {}
    if os.path.exists(save_file):
        try:
            with open(save_file, "r") as f:
                existing_data = json.load(f)
        except:
            pass
    # Update with skin info
    existing_data["current_skin"] = skin_name
    existing_data["owned_skins"] = owned_list
    with open(save_file, "w") as f:
        json.dump(existing_data, f)
    print("Saved skin: " + skin_name)

# Start with base coins - roguelike mode!
coins = STARTING_COINS
print("ROGUELIKE MODE! Starting with " + str(coins) + " coins!")

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
thrawn_y = SCREEN_HEIGHT // 2  # Middle of screen (so you don't drift!)
thrawn_speed = 5  # How fast Thrawn moves in pixels per frame at 60 FPS

# --- SKINS! ---
# Different character skins like Fortnite!
current_skin = "thrawn"  # Which skin is equipped
owned_skins = ["thrawn"]  # Skins you own (start with default)
skin_shop_selection = 0  # Which skin is selected in skin shop

# Load saved skin data!
loaded_skin, loaded_owned = load_skins()
current_skin = loaded_skin
owned_skins = loaded_owned
print("Loaded skin: " + current_skin)

# All available skins with prices and colors!
all_skins = [
    {"name": "thrawn", "display": "THRAWN", "price": 0, "owned": True,
     "desc": "The original hero!", "colors": {"body": (70, 130, 180), "accent": (50, 100, 150)}},
    {"name": "ender", "display": "ENDER WIGGIN", "price": 500, "owned": False,
     "desc": "Battle School commander!", "colors": {"body": (40, 80, 40), "accent": (60, 120, 60)}},
    {"name": "robot", "display": "ROBOT X-9", "price": 750, "owned": False,
     "desc": "Chrome combat machine!", "colors": {"body": (150, 150, 160), "accent": (100, 100, 110)}},
    {"name": "ninja", "display": "SHADOW NINJA", "price": 600, "owned": False,
     "desc": "Silent and deadly!", "colors": {"body": (30, 30, 40), "accent": (80, 0, 0)}},
    {"name": "alien", "display": "ALIEN HUNTER", "price": 800, "owned": False,
     "desc": "From another world!", "colors": {"body": (0, 180, 100), "accent": (0, 220, 150)}},
    {"name": "fire", "display": "FIRE KING", "price": 1000, "owned": False,
     "desc": "Burns with power!", "colors": {"body": (200, 80, 0), "accent": (255, 150, 0)}},
    {"name": "ice", "display": "ICE QUEEN", "price": 1000, "owned": False,
     "desc": "Frozen warrior!", "colors": {"body": (100, 180, 255), "accent": (200, 230, 255)}},
    {"name": "gold", "display": "GOLDEN LEGEND", "price": 2000, "owned": False,
     "desc": "The ultimate flex!", "colors": {"body": (255, 200, 0), "accent": (255, 230, 100)}},
    {"name": "custom", "display": "CUSTOM SKIN", "price": 100, "owned": False,
     "desc": "Draw your own!", "colors": {"body": (255, 100, 100), "accent": (255, 200, 100)}},
]

# Custom skin drawing data!
custom_skin_pixels = []  # List of [x, y, color] for each pixel drawn
drawing_color = (255, 0, 0)  # Current drawing color (red default)
drawing_colors = [
    (255, 0, 0),    # Red
    (255, 128, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 255, 255),  # Cyan
    (0, 0, 255),    # Blue
    (255, 0, 255),  # Purple
    (255, 255, 255),# White
    (0, 0, 0),      # Black
    (139, 69, 19),  # Brown (skin)
    (255, 200, 150),# Peach (skin)
    (128, 128, 128),# Gray
]
drawing_color_index = 0

# --- REALISTIC SPACE PHYSICS! ---
# In space, things keep moving (momentum!)
velocity_x = 0  # How fast moving left/right
velocity_y = 0  # How fast moving up/down
max_velocity = 8  # Top speed
acceleration = 0.3  # How fast you speed up
friction = 0.98  # Slow down gradually (0.98 = 2% per frame)

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

# REALISTIC STAR COLORS! (like real astronomy)
# Blue = hot stars, White = medium, Yellow = like our sun, Orange/Red = cooler
star_colors = [
    (200, 220, 255),  # Blue-white (hot stars like Rigel)
    (255, 255, 255),  # Pure white
    (255, 255, 200),  # Yellow-white (like our Sun)
    (255, 220, 180),  # Orange (like Arcturus)
    (255, 180, 150),  # Red-orange (like Betelgeuse)
    (180, 200, 255),  # Blue (young hot stars)
]

# Draw all stars onto the surface ONCE with realistic colors
for i, star in enumerate(far_stars):
    color = star_colors[i % len(star_colors)]
    # Dim distant stars
    dim_color = (color[0]//2, color[1]//2, color[2]//2)
    pygame.draw.circle(star_surface, dim_color, (int(star[0]), int(star[1])), 1)
    pygame.draw.circle(star_surface, dim_color, (int(star[0]), int(star[1]) + SCREEN_HEIGHT), 1)
for i, star in enumerate(medium_stars):
    color = star_colors[(i + 2) % len(star_colors)]
    pygame.draw.circle(star_surface, color, (int(star[0]), int(star[1])), 2)
    pygame.draw.circle(star_surface, color, (int(star[0]), int(star[1]) + SCREEN_HEIGHT), 2)
for i, star in enumerate(close_stars):
    color = star_colors[(i + 4) % len(star_colors)]
    # Bright close stars with glow
    pygame.draw.circle(star_surface, (color[0]//2, color[1]//2, color[2]//2), (int(star[0]), int(star[1])), 5)
    pygame.draw.circle(star_surface, color, (int(star[0]), int(star[1])), 3)
    pygame.draw.circle(star_surface, (color[0]//2, color[1]//2, color[2]//2), (int(star[0]), int(star[1]) + SCREEN_HEIGHT), 5)
    pygame.draw.circle(star_surface, color, (int(star[0]), int(star[1]) + SCREEN_HEIGHT), 3)

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
# "signin" = enter your username!
# "title" = show the cool opening screen
# "shop" = the AWESOME shop where you buy power-ups!
# "playing" = fly around space, discover planets, and fight Zeldas!
# "on_planet" = exploring a planet surface
# "leaderboard" = view high scores!
game_state = "signin"  # Start with sign in!
title_timer = 0  # Timer for cool animations on title screen!
username_input = ""  # What the player is typing for their name

# Story ending variables!
story_ending_timer = 0  # Timer for story ending animations
story_page = 0  # Which page of the story we're on

# --- LOBBY SYSTEM! ---
# After every level or death, you come back here!
lobby_selection = 0  # Which option is selected in lobby (0=Continue, 1=Shop, etc.)
lobby_reason = "level"  # Why we're in lobby: "level" (beat boss) or "death" (died)
quit_confirm = False  # Need to confirm before quitting!

# --- SPACE EXPLORATION! ---
# The big space world you can explore!
WORLD_WIDTH = 4000   # How big is space? (4000 pixels wide)
WORLD_HEIGHT = 4000  # (4000 pixels tall)

# Camera position (what part of the world we're looking at)
camera_x = 0
camera_y = 0

# Player position in the WORLD (not screen!)
player_world_x = 500  # Start ON Earth!
player_world_y = 500
player_walk_speed = 4  # Walking speed
player_run_speed = 8   # Running speed (hold SHIFT)

# --- PLANETS! ---
# Planets to discover in space! Each planet is:
# [x, y, name, color, size, discovered, has_zeldas, has_food, has_materials]
planets = [
    [500, 500, "Earth", (50, 150, 50), 80, True, True, True, True],       # Starting planet (discovered)
    [2500, 1500, "Mars", (200, 80, 50), 60, False, True, False, True],     # Red planet - FAR!
    [4500, 800, "Ice World", (150, 200, 255), 70, False, True, True, False],  # Cold planet - VERY FAR!
    [5500, 3500, "Jungle", (30, 180, 30), 90, False, True, True, True],   # Green planet - SUPER FAR!
    [1500, 4000, "Desert", (220, 180, 100), 65, False, True, False, True], # Sandy planet - FAR!
    [3500, 5500, "Ocean", (50, 100, 200), 85, False, False, True, False], # Water planet - VERY FAR!
    [6000, 2000, "Volcano", (180, 50, 30), 55, False, True, False, True], # Fire planet - SUPER FAR!
    [2000, 3000, "Moon Base", (180, 180, 180), 40, False, False, False, True],  # Small moon - FAR!
]

# Current planet (which planet are we battling on?)
current_planet = None
current_planet_name = "Space"

# --- PLANET ECONOMIES! ---
# Each planet has its own food supply and production!
# Runs in the background even when you're not there!
planet_economy = {}
for p in planets:
    planet_economy[p[2]] = {
        "food_supply": 50 if p[7] else 0,  # Start with 50 food if planet has food
        "materials_supply": 0,
        "last_update": 0,  # Track time for production
    }

# Economy rates (per second)
FOOD_PER_FARMER = 2      # Each farmer produces 2 food/sec
FOOD_PER_VILLAGER = 0.5  # Each villager eats 0.5 food/sec
FOOD_ON_LANDING = 30     # Max food you can take when landing

# --- INVENTORY! ---
# What you've collected!
food = 100  # Start with some food (decreases over time!)
materials = 0  # For building bases

# --- CIVILIZATION RESOURCES! ---
# Different types of materials for building your city!
wood = 0      # From trees - for houses
stone = 0     # From rocks - for strong buildings
iron = 0      # From metal - for weapons and armor
gold = 0      # Rare! - for fancy buildings and trade

# --- POPULATION! ---
# Villagers from destroyed worlds come to your planets!
population = 0  # Total villagers across all your planets
villagers = []  # Each villager is [planet_name, x, y, job, happiness]
# Jobs: "homeless", "farmer", "miner", "soldier", "banker", "builder", "shopkeeper"

# --- ARMY! ---
# Soldiers that fight alongside you!
soldiers = 0     # How many soldiers you have
army_power = 0   # Total fighting strength of your army

# --- REFUGEES! ---
# When you destroy enemies, sometimes refugees escape and join you!
refugees_waiting = 0  # Refugees waiting to land on a planet

# --- SHUTTLE! ---
# Your shuttle to travel to planets!
near_planet = None  # Which planet are we near? (None if not near any)
shuttle_cooldown = 0  # Can't spam the shuttle button
on_planet = False  # Are we landed on a planet?
planet_explore_x = 0  # Where are we on the planet surface?
planet_explore_y = 0

# --- BASES AND BUILDINGS! ---
# Things you've built on planets!
# Each building is [planet_name, x, y, type, health(optional)]
buildings = []
building_menu_open = False  # Press TAB to see all buildings!
building_menu_scroll = 0    # Scroll position in menu

# --- BUILDING INTERIORS! ---
# When you enter a building, you can do stuff inside!
inside_building = None  # Which building we're inside [planet, x, y, type]
inside_menu_selection = 0  # Which option is selected inside

# Farm stuff
farm_crops = []  # Crops growing: [building_x, building_y, growth_stage, crop_type]

# Bank stuff
bank_balance = 0  # Coins stored in bank (earns interest!)

# Market prices (fluctuate!)
market_prices = {
    "wood": 2,      # Coins per wood
    "stone": 3,     # Coins per stone
    "iron": 5,      # Coins per iron
    "gold": 10,     # Coins per gold
    "food": 1,      # Coins per food
}

# Building costs! (in materials)
BASE_COST = 50       # Base - unlocks more buildings!
TURRET_COST = 30     # Turret - shoots at enemies
FACTORY_COST = 100   # Robot Factory - spawns helper robots (need wingmen!)
BANK_COST = 75       # Bank - generates coins over time
FARM_COST = 60       # Farm - generates food over time
SHIELD_GEN_COST = 80 # Shield Generator - gives shield when you land
MINER_COST = 70      # Auto Miner - automatically collects materials
HOSPITAL_COST = 90   # Hospital - gives extra life when you land
RADAR_COST = 50      # Radar - shows enemy warning arrows
SHIPYARD_COST = 120  # Shipyard - upgrades your ship!

# --- CIVILIZATION BUILDINGS! ---
HOUSE_COST = 20        # House - villagers live here (need wood!)
HOUSE_WOOD = 10        # Wood needed for a house
SPACEPORT_COST = 150   # Space Port - dock your fleet ships!
SPACEPORT_IRON = 30    # Iron needed for space port
MARKET_COST = 40       # Farmers Market - trade materials for coins!
MARKET_WOOD = 15       # Wood needed for market
BARRACKS_COST = 80     # Barracks - train soldiers for your army!
BARRACKS_IRON = 20     # Iron needed for barracks
TAVERN_COST = 35       # Tavern - makes villagers happy!
TAVERN_WOOD = 10       # Wood needed for tavern
WAREHOUSE_COST = 45    # Warehouse - stores extra materials!
WAREHOUSE_WOOD = 20    # Wood needed for warehouse

# Max workers per building!
MAX_WORKERS_PER_BUILDING = 3  # Only 3 villagers can work at each building

# Building timers for generating stuff!
bank_timer = 0       # Timer for banks generating coins
farm_timer = 0       # Timer for farms generating food
miner_timer = 0      # Timer for miners collecting materials

# Shipyard upgrades!
ship_damage_level = 1    # How much damage lasers do (1 = normal)
ship_speed_level = 1     # How fast ship moves (1 = normal)
ship_fire_rate_level = 1 # How fast you can shoot (1 = normal)

# Robot helpers from factory!
helper_robots = []  # List of [x, y, target_x, target_y, shoot_timer]
factory_spawn_timer = 0  # Timer for spawning robots from factories

# --- TURRET SHOOTING! ---
# Turrets shoot at enemies automatically!
turret_lasers = []  # Each laser is [x, y, dx, dy] - position and direction
turret_shoot_timer = 0  # Timer for when turrets shoot

# --- ACTIVE TURRETS ON SCREEN! ---
# Turrets that appear during battle! Each is [x, y, health]
active_turrets = []  # Gets filled based on buildings when playing

# --- PLANET MATERIALS! ---
# Materials scattered on the planet surface
# Each material is [x, y, type] where type is "crystal" or "metal" or "rock"
planet_materials = []  # Gets filled when you land on a planet

# --- PLANET FOOD! ---
# Food to collect on planets!
planet_food = []  # Gets filled when you land on a planet with food
hunger_rate = 0.003  # How fast food decreases per frame (slow and realistic)

# --- USER SYSTEM! ---
# Your username and high scores!
current_user = ""  # Who is playing?
leaderboard_file = "leaderboard.json"

# Load the leaderboard!
def load_leaderboard():
    if os.path.exists(leaderboard_file):
        try:
            with open(leaderboard_file, "r") as f:
                return json.load(f)
        except:
            return []
    return []

# Save to leaderboard!
def save_to_leaderboard(username, score_value):
    lb = load_leaderboard()
    lb.append({"name": username, "score": score_value})
    # Sort by score (highest first) and keep top 10
    lb.sort(key=lambda x: x["score"], reverse=True)
    lb = lb[:10]
    with open(leaderboard_file, "w") as f:
        json.dump(lb, f)
    return lb

leaderboard = load_leaderboard()

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
    {"name": "SKINS", "price": 0, "desc": "Change your look!", "color": (255, 100, 255)},
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
    global planets, current_planet, current_planet_name, near_planet, planet_economy
    global food, materials, shuttle_cooldown
    global wood, stone, iron, gold
    global population, villagers, soldiers, army_power, refugees_waiting
    global on_planet, planet_explore_x, planet_explore_y, planet_materials, buildings
    global planet_food, current_user, username_input, leaderboard
    global velocity_x, velocity_y
    global turret_lasers, turret_shoot_timer, active_turrets
    global current_skin, owned_skins, skin_shop_selection, all_skins
    global factory_spawn_timer, helper_robots
    global custom_skin_pixels, drawing_color, drawing_color_index
    global story_ending_timer, story_page
    global bank_timer, farm_timer, miner_timer
    global ship_damage_level, ship_speed_level, ship_fire_rate_level
    global lobby_selection, lobby_reason, quit_confirm
    global building_menu_open, building_menu_scroll
    global inside_building, inside_menu_selection, farm_crops, bank_balance, market_prices

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

            # --- SIGN IN! ---
            # Type your username and press ENTER!
            if game_state == "signin":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(username_input) > 0:
                        # Save username and go to title!
                        current_user = username_input
                        game_state = "title"
                        print("Welcome, " + current_user + "!")
                    elif event.key == pygame.K_BACKSPACE:
                        # Delete last character
                        username_input = username_input[:-1]
                    elif event.key == pygame.K_TAB:
                        # View leaderboard
                        game_state = "leaderboard"
                    elif len(username_input) < 12:  # Max 12 characters
                        # Add the typed character (only letters and numbers!)
                        if event.unicode.isalnum():
                            username_input = username_input + event.unicode

            # --- LEADERBOARD CONTROLS ---
            if event.type == pygame.KEYDOWN and game_state == "leaderboard":
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
                    game_state = "signin"  # Go back to sign in

            # --- PRESS ENTER TO PLAY! ---
            # When on title screen, press ENTER to start the game!
            if event.type == pygame.KEYDOWN and game_state == "title":
                if event.key == pygame.K_RETURN:  # RETURN is the ENTER key!
                    game_state = "playing"  # Start playing!
                    # Center camera on player
                    camera_x = player_world_x - SCREEN_WIDTH // 2
                    camera_y = player_world_y - SCREEN_HEIGHT // 2
                elif event.key == pygame.K_TAB:
                    # View leaderboard from title
                    game_state = "leaderboard"

            # --- IN-GAME CONTROLS! ---
            # TAB opens the shop while playing!
            if event.type == pygame.KEYDOWN and game_state == "playing" and not game_over:
                if event.key == pygame.K_TAB:
                    game_state = "shop"
                    shop_selection = 0
                # V key = take shuttle to land on planet!
                if event.key == pygame.K_v and near_planet is not None:
                    current_planet = near_planet
                    current_planet_name = near_planet[2]
                    on_planet = True
                    game_state = "on_planet"
                    planet_explore_x = SCREEN_WIDTH // 2
                    planet_explore_y = SCREEN_HEIGHT // 2
                    # Spawn materials on the planet!
                    planet_materials = []
                    if near_planet[8]:  # Has materials?
                        for i in range(20):  # 20 materials to collect!
                            mx = random.randint(100, SCREEN_WIDTH - 100)
                            my = random.randint(100, SCREEN_HEIGHT - 100)
                            # Different planets have different resources!
                            mtype = random.choice(["crystal", "metal", "rock", "wood", "stone", "wood", "stone"])
                            planet_materials.append([mx, my, mtype])
                    # Spawn food on the planet!
                    planet_food = []
                    if near_planet[7]:  # Has food?
                        for i in range(10):  # 10 food items!
                            fx = random.randint(100, SCREEN_WIDTH - 100)
                            fy = random.randint(100, SCREEN_HEIGHT - 100)
                            ftype = random.choice(["apple", "meat", "berry"])
                            planet_food.append([fx, fy, ftype])
                    print("Landed on " + current_planet_name + "!")

                    # --- FOOD FROM PLANET SURPLUS! ---
                    # If the planet has extra food, take some for your ship!
                    if current_planet_name in planet_economy:
                        planet_food_supply = planet_economy[current_planet_name]["food_supply"]
                        if planet_food_supply > 20:  # Only take if surplus exists
                            food_to_take = min(FOOD_ON_LANDING, planet_food_supply - 20)  # Leave 20 for villagers
                            food_to_take = min(food_to_take, 100 - food)  # Don't overfill ship
                            if food_to_take > 0:
                                planet_economy[current_planet_name]["food_supply"] -= food_to_take
                                food = food + food_to_take
                                print("Resupplied " + str(int(food_to_take)) + " food from planet!")
                        elif planet_food_supply < 10:
                            print("WARNING: Planet food supply low! (" + str(int(planet_food_supply)) + ")")

                    # Check for building bonuses when landing!
                    for b in buildings:
                        if b[0] == current_planet_name:
                            # Shield Generator gives a shield!
                            if b[3] == "shield_gen":
                                shield_hits = shield_hits + 1
                                has_shield = True
                                print("Shield Generator activated! +" + str(shield_hits) + " shields!")
                            # Hospital gives extra life!
                            if b[3] == "hospital":
                                lives = lives + 1
                                print("Hospital healed you! Lives: " + str(lives))
                            # Shipyard upgrades your ship!
                            if b[3] == "shipyard":
                                # Cycle through upgrades
                                if ship_damage_level < 3:
                                    ship_damage_level = ship_damage_level + 1
                                    print("Shipyard upgraded DAMAGE to level " + str(ship_damage_level) + "!")
                                elif ship_speed_level < 3:
                                    ship_speed_level = ship_speed_level + 1
                                    print("Shipyard upgraded SPEED to level " + str(ship_speed_level) + "!")
                                elif ship_fire_rate_level < 3:
                                    ship_fire_rate_level = ship_fire_rate_level + 1
                                    print("Shipyard upgraded FIRE RATE to level " + str(ship_fire_rate_level) + "!")
                                else:
                                    print("Ship fully upgraded!")

                    # REFUGEES settle in houses on this planet!
                    if refugees_waiting > 0:
                        # Count houses on this planet
                        houses_here = 0
                        villagers_here = 0
                        for b in buildings:
                            if b[0] == current_planet_name and b[3] == "house":
                                houses_here = houses_here + 1
                        for v in villagers:
                            if v[0] == current_planet_name:
                                villagers_here = villagers_here + 1
                        # Each house can hold 4 villagers
                        space = (houses_here * 4) - villagers_here
                        if space > 0:
                            settling = min(refugees_waiting, space)
                            for i in range(settling):
                                vx = random.randint(100, SCREEN_WIDTH - 100)
                                vy = random.randint(100, SCREEN_HEIGHT - 100)
                                villagers.append([current_planet_name, vx, vy, "homeless", 50])
                                population = population + 1
                            refugees_waiting = refugees_waiting - settling
                            print(str(settling) + " refugees settled! Population: " + str(population))

            # --- ON PLANET CONTROLS! ---
            # Use elif so landing and returning don't happen in same frame!
            elif event.type == pygame.KEYDOWN and game_state == "on_planet":
                # Count buildings on this planet for tier system!
                has_base = False
                turret_count = 0
                for b in buildings:
                    if b[0] == current_planet_name:
                        if b[3] == "base":
                            has_base = True
                        if b[3] == "turret":
                            turret_count = turret_count + 1

                # TAB key = toggle building menu!
                if event.key == pygame.K_TAB:
                    building_menu_open = not building_menu_open
                    building_menu_scroll = 0
                    if building_menu_open:
                        print("Building menu opened!")
                    else:
                        print("Building menu closed!")

                # If menu is open, UP/DOWN scrolls it
                if building_menu_open:
                    if event.key == pygame.K_UP:
                        building_menu_scroll = max(0, building_menu_scroll - 1)
                    if event.key == pygame.K_DOWN:
                        building_menu_scroll = min(12, building_menu_scroll + 1)  # 13 buildings total
                    # ESC or TAB closes menu
                    if event.key == pygame.K_ESCAPE:
                        building_menu_open = False

                # V key = take shuttle back to space!
                if event.key == pygame.K_v and not building_menu_open:
                    on_planet = False
                    game_state = "playing"
                    building_menu_open = False
                    print("Returned to space!")

                # --- DEBUG MODE! (F1) ---
                # Press F1 to get lots of resources for testing!
                if event.key == pygame.K_F1:
                    materials = materials + 500
                    wood = wood + 200
                    stone = stone + 200
                    iron = iron + 100
                    gold = gold + 50
                    coins = coins + 1000
                    refugees_waiting = refugees_waiting + 20
                    food = 100
                    print("=== DEBUG MODE ===")
                    print("Added: 500 materials, 200 wood, 200 stone, 100 iron, 50 gold")
                    print("Added: 1000 coins, 20 refugees, full food!")
                    print("==================")

                # 0 key = Spawn villagers directly on this planet
                if event.key == pygame.K_0:
                    for i in range(10):
                        vx = random.randint(100, SCREEN_WIDTH - 100)
                        vy = random.randint(100, SCREEN_HEIGHT - 100)
                        villagers.append([current_planet_name, vx, vy, "homeless", 50, 0, 0])
                        population = population + 1
                    print("Spawned 10 villagers! Population: " + str(population))

                # F3 = Build all buildings at once!
                if event.key == pygame.K_F3:
                    bx, by = planet_explore_x, planet_explore_y
                    buildings.append([current_planet_name, bx, by, "base"])
                    buildings.append([current_planet_name, bx + 80, by, "farm"])
                    buildings.append([current_planet_name, bx - 80, by, "bank"])
                    buildings.append([current_planet_name, bx, by + 80, "barracks"])
                    buildings.append([current_planet_name, bx, by - 80, "market"])
                    buildings.append([current_planet_name, bx + 80, by + 80, "house"])
                    buildings.append([current_planet_name, bx - 80, by + 80, "house"])
                    buildings.append([current_planet_name, bx + 80, by - 80, "miner"])
                    buildings.append([current_planet_name, bx - 80, by - 80, "factory"])
                    print("=== DEBUG: Built all buildings! ===")

                # F4 = Max out army
                if event.key == pygame.K_F4:
                    soldiers = soldiers + 50
                    army_power = army_power + 500
                    print("=== DEBUG: Added 50 soldiers! Army power: " + str(army_power) + " ===")

                # B key = build a BASE!
                if event.key == pygame.K_b:
                    if has_base:
                        print("Already have a base on this planet!")
                    elif materials >= BASE_COST:
                        materials = materials - BASE_COST
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "base"])
                        print("Built a BASE! You can now build more buildings!")
                    else:
                        print("Need " + str(BASE_COST) + " materials!")

                # T key = build a TURRET!
                if event.key == pygame.K_t:
                    max_turrets = 3 if has_base else 1
                    if turret_count >= max_turrets:
                        if has_base:
                            print("Max 3 turrets per planet!")
                        else:
                            print("Build a BASE first to get more turrets!")
                    elif materials >= TURRET_COST:
                        materials = materials - TURRET_COST
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "turret"])
                        print("Built TURRET! (" + str(turret_count + 1) + "/" + str(max_turrets) + ")")
                    else:
                        print("Need " + str(TURRET_COST) + " materials!")

                # F key = build a FARM!
                if event.key == pygame.K_f:
                    if not has_base:
                        print("Need a BASE first!")
                    elif materials >= FARM_COST:
                        materials = materials - FARM_COST
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "farm"])
                        print("Built a FARM! Generates food over time!")
                    else:
                        print("Need " + str(FARM_COST) + " materials!")

                # K key = build a BANK!
                if event.key == pygame.K_k:
                    if not has_base:
                        print("Need a BASE first!")
                    elif materials >= BANK_COST:
                        materials = materials - BANK_COST
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "bank"])
                        print("Built a BANK! Generates coins over time!")
                    else:
                        print("Need " + str(BANK_COST) + " materials!")

                # R key = build a ROBOT FACTORY!
                if event.key == pygame.K_r:
                    if not has_base:
                        print("Need a BASE first!")
                    elif materials >= FACTORY_COST:
                        materials = materials - FACTORY_COST
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "factory"])
                        print("Built ROBOT FACTORY! (Needs wingmen to deploy robots)")
                    else:
                        print("Need " + str(FACTORY_COST) + " materials!")

                # G key = build a SHIELD GENERATOR!
                if event.key == pygame.K_g:
                    if not has_base:
                        print("Need a BASE first!")
                    elif materials >= SHIELD_GEN_COST:
                        materials = materials - SHIELD_GEN_COST
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "shield_gen"])
                        print("Built SHIELD GENERATOR! Get shields when you land!")
                    else:
                        print("Need " + str(SHIELD_GEN_COST) + " materials!")

                # M key = build an AUTO MINER!
                if event.key == pygame.K_m:
                    if not has_base:
                        print("Need a BASE first!")
                    elif materials >= MINER_COST:
                        materials = materials - MINER_COST
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "miner"])
                        print("Built AUTO MINER! Collects materials automatically!")
                    else:
                        print("Need " + str(MINER_COST) + " materials!")

                # H key = build a HOSPITAL!
                if event.key == pygame.K_h:
                    if not has_base:
                        print("Need a BASE first!")
                    elif materials >= HOSPITAL_COST:
                        materials = materials - HOSPITAL_COST
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "hospital"])
                        print("Built HOSPITAL! Get extra life when you land!")
                    else:
                        print("Need " + str(HOSPITAL_COST) + " materials!")

                # D key = build a RADAR!
                if event.key == pygame.K_d:
                    if not has_base:
                        print("Need a BASE first!")
                    elif materials >= RADAR_COST:
                        materials = materials - RADAR_COST
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "radar"])
                        print("Built RADAR! Shows enemy warnings!")
                    else:
                        print("Need " + str(RADAR_COST) + " materials!")

                # Y key = build a SHIPYARD!
                if event.key == pygame.K_y:
                    if not has_base:
                        print("Need a BASE first!")
                    elif materials >= SHIPYARD_COST:
                        materials = materials - SHIPYARD_COST
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "shipyard"])
                        print("Built SHIPYARD! Upgrades your ship!")
                    else:
                        print("Need " + str(SHIPYARD_COST) + " materials!")

                # --- CIVILIZATION BUILDINGS! ---
                # Q key = build a HOUSE (for villagers!)
                if event.key == pygame.K_q:
                    if materials >= HOUSE_COST and wood >= HOUSE_WOOD:
                        materials = materials - HOUSE_COST
                        wood = wood - HOUSE_WOOD
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "house"])
                        print("Built HOUSE! Villagers can live here!")
                    elif wood < HOUSE_WOOD:
                        print("Need " + str(HOUSE_WOOD) + " wood!")
                    else:
                        print("Need " + str(HOUSE_COST) + " materials!")

                # P key = build a SPACE PORT!
                if event.key == pygame.K_p:
                    if not has_base:
                        print("Need a BASE first!")
                    elif materials >= SPACEPORT_COST and iron >= SPACEPORT_IRON:
                        materials = materials - SPACEPORT_COST
                        iron = iron - SPACEPORT_IRON
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "spaceport"])
                        print("Built SPACE PORT! Your fleet can dock here!")
                    elif iron < SPACEPORT_IRON:
                        print("Need " + str(SPACEPORT_IRON) + " iron!")
                    else:
                        print("Need " + str(SPACEPORT_COST) + " materials!")

                # E key = build a MARKET!
                if event.key == pygame.K_e:
                    if materials >= MARKET_COST and wood >= MARKET_WOOD:
                        materials = materials - MARKET_COST
                        wood = wood - MARKET_WOOD
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "market"])
                        print("Built FARMERS MARKET! Trade for coins!")
                    elif wood < MARKET_WOOD:
                        print("Need " + str(MARKET_WOOD) + " wood!")
                    else:
                        print("Need " + str(MARKET_COST) + " materials!")

                # X key = build BARRACKS (train soldiers!)
                if event.key == pygame.K_x:
                    if not has_base:
                        print("Need a BASE first!")
                    elif materials >= BARRACKS_COST and iron >= BARRACKS_IRON:
                        materials = materials - BARRACKS_COST
                        iron = iron - BARRACKS_IRON
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "barracks"])
                        print("Built BARRACKS! Train soldiers here!")
                    elif iron < BARRACKS_IRON:
                        print("Need " + str(BARRACKS_IRON) + " iron!")
                    else:
                        print("Need " + str(BARRACKS_COST) + " materials!")

                # C key = build TAVERN!
                if event.key == pygame.K_c:
                    if materials >= TAVERN_COST and wood >= TAVERN_WOOD:
                        materials = materials - TAVERN_COST
                        wood = wood - TAVERN_WOOD
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "tavern"])
                        print("Built TAVERN! Villagers get happier here!")
                    elif wood < TAVERN_WOOD:
                        print("Need " + str(TAVERN_WOOD) + " wood!")
                    else:
                        print("Need " + str(TAVERN_COST) + " materials!")

                # Z key = build WAREHOUSE!
                if event.key == pygame.K_z:
                    if materials >= WAREHOUSE_COST and wood >= WAREHOUSE_WOOD:
                        materials = materials - WAREHOUSE_COST
                        wood = wood - WAREHOUSE_WOOD
                        buildings.append([current_planet_name, planet_explore_x, planet_explore_y, "warehouse"])
                        print("Built WAREHOUSE! Store extra stuff!")
                    elif wood < WAREHOUSE_WOOD:
                        print("Need " + str(WAREHOUSE_WOOD) + " wood!")
                    else:
                        print("Need " + str(WAREHOUSE_COST) + " materials!")

                # ENTER = Enter a building!
                if event.key == pygame.K_RETURN:
                    # Check if near any building
                    for b in buildings:
                        if b[0] == current_planet_name:
                            dist = ((planet_explore_x - b[1]) ** 2 + (planet_explore_y - b[2]) ** 2) ** 0.5
                            if dist < 50:  # Close enough to enter!
                                building_type = b[3]
                                # Only some buildings can be entered
                                if building_type in ["farm", "bank", "market", "barracks", "house", "tavern", "warehouse", "hospital"]:
                                    inside_building = [current_planet_name, b[1], b[2], building_type]
                                    inside_menu_selection = 0
                                    game_state = "inside_building"
                                    print("Entered " + building_type.upper() + "!")
                                else:
                                    print("Can't enter this building!")
                                break

                # --- JOB ASSIGNMENTS (Number Keys!) ---
                # Helper function to count workers at a building
                def count_workers_at(bx, by, job_type):
                    count = 0
                    for vv in villagers:
                        if vv[0] == current_planet_name and vv[3] == job_type:
                            if len(vv) >= 7:  # Has target position
                                if abs(vv[5] - bx) < 10 and abs(vv[6] - by) < 10:
                                    count = count + 1
                    return count

                # Helper to find a building with room
                def find_building_with_room(building_type, job_type):
                    for b in buildings:
                        if b[0] == current_planet_name and b[3] == building_type:
                            workers = count_workers_at(b[1], b[2], job_type)
                            if workers < MAX_WORKERS_PER_BUILDING:
                                return b
                    return None

                # 1 = Assign FARMER
                if event.key == pygame.K_1:
                    for v in villagers:
                        if v[0] == current_planet_name and v[3] == "homeless":
                            building = find_building_with_room("farm", "farmer")
                            if building:
                                v[3] = "farmer"
                                # Add target position (extend list if needed)
                                while len(v) < 7:
                                    v.append(0)
                                v[5] = building[1]  # target_x
                                v[6] = building[2]  # target_y
                                workers = count_workers_at(building[1], building[2], "farmer")
                                print("Villager became a FARMER! (" + str(workers) + "/" + str(MAX_WORKERS_PER_BUILDING) + " at this farm)")
                            else:
                                # Check if we have any farms at all
                                has_farm = any(b[0] == current_planet_name and b[3] == "farm" for b in buildings)
                                if has_farm:
                                    print("All farms are FULL! (max " + str(MAX_WORKERS_PER_BUILDING) + " workers each)")
                                else:
                                    print("Need a FARM to assign farmers!")
                            break

                # 2 = Assign MINER
                if event.key == pygame.K_2:
                    for v in villagers:
                        if v[0] == current_planet_name and v[3] == "homeless":
                            building = find_building_with_room("miner", "miner")
                            if building:
                                v[3] = "miner"
                                while len(v) < 7:
                                    v.append(0)
                                v[5] = building[1]
                                v[6] = building[2]
                                workers = count_workers_at(building[1], building[2], "miner")
                                print("Villager became a MINER! (" + str(workers) + "/" + str(MAX_WORKERS_PER_BUILDING) + " at this miner)")
                            else:
                                has_miner = any(b[0] == current_planet_name and b[3] == "miner" for b in buildings)
                                if has_miner:
                                    print("All miners are FULL!")
                                else:
                                    print("Need an AUTO MINER to assign miners!")
                            break

                # 3 = Assign SOLDIER
                if event.key == pygame.K_3:
                    for v in villagers:
                        if v[0] == current_planet_name and v[3] == "homeless":
                            building = find_building_with_room("barracks", "soldier")
                            if building:
                                v[3] = "soldier"
                                while len(v) < 7:
                                    v.append(0)
                                v[5] = building[1]
                                v[6] = building[2]
                                soldiers = soldiers + 1
                                army_power = army_power + 10
                                workers = count_workers_at(building[1], building[2], "soldier")
                                print("Villager became a SOLDIER! (" + str(workers) + "/" + str(MAX_WORKERS_PER_BUILDING) + ") Army: " + str(army_power))
                            else:
                                has_barracks = any(b[0] == current_planet_name and b[3] == "barracks" for b in buildings)
                                if has_barracks:
                                    print("All barracks are FULL!")
                                else:
                                    print("Need BARRACKS to train soldiers!")
                            break

                # 4 = Assign BANKER
                if event.key == pygame.K_4:
                    for v in villagers:
                        if v[0] == current_planet_name and v[3] == "homeless":
                            building = find_building_with_room("bank", "banker")
                            if building:
                                v[3] = "banker"
                                while len(v) < 7:
                                    v.append(0)
                                v[5] = building[1]
                                v[6] = building[2]
                                workers = count_workers_at(building[1], building[2], "banker")
                                print("Villager became a BANKER! (" + str(workers) + "/" + str(MAX_WORKERS_PER_BUILDING) + " at this bank)")
                            else:
                                has_bank = any(b[0] == current_planet_name and b[3] == "bank" for b in buildings)
                                if has_bank:
                                    print("All banks are FULL!")
                                else:
                                    print("Need a BANK to assign bankers!")
                            break

                # 5 = Assign SHOPKEEPER
                if event.key == pygame.K_5:
                    for v in villagers:
                        if v[0] == current_planet_name and v[3] == "homeless":
                            building = find_building_with_room("market", "shopkeeper")
                            if building:
                                v[3] = "shopkeeper"
                                while len(v) < 7:
                                    v.append(0)
                                v[5] = building[1]
                                v[6] = building[2]
                                workers = count_workers_at(building[1], building[2], "shopkeeper")
                                print("Villager became a SHOPKEEPER! (" + str(workers) + "/" + str(MAX_WORKERS_PER_BUILDING) + " at this market)")
                            else:
                                has_market = any(b[0] == current_planet_name and b[3] == "market" for b in buildings)
                                if has_market:
                                    print("All markets are FULL!")
                                else:
                                    print("Need a MARKET to assign shopkeepers!")
                            break

                # 6 = Assign BUILDER (no building needed, they wander)
                if event.key == pygame.K_6:
                    for v in villagers:
                        if v[0] == current_planet_name and v[3] == "homeless":
                            v[3] = "builder"
                            print("Villager became a BUILDER!")
                            break

            # --- BUILDING INTERIOR CONTROLS! ---
            if event.type == pygame.KEYDOWN and game_state == "inside_building" and inside_building:
                building_type = inside_building[3]

                # ESC = Leave building
                if event.key == pygame.K_ESCAPE:
                    game_state = "on_planet"
                    print("Left " + building_type + "!")

                # UP/DOWN = Navigate menu
                if event.key == pygame.K_UP:
                    inside_menu_selection = inside_menu_selection - 1
                    if inside_menu_selection < 0:
                        inside_menu_selection = 3  # Most buildings have 4 options

                if event.key == pygame.K_DOWN:
                    inside_menu_selection = inside_menu_selection + 1
                    if inside_menu_selection > 3:
                        inside_menu_selection = 0

                # Number keys for quick actions!
                # FARM actions
                if building_type == "farm":
                    if event.key == pygame.K_1:
                        # Plant crops
                        if coins >= 10:
                            coins = coins - 10
                            print("Planted new crops!")
                        else:
                            print("Need 10 coins to plant!")
                    elif event.key == pygame.K_2:
                        # Harvest
                        food = min(100, food + 30)
                        print("Harvested crops! Food: " + str(food))
                    elif event.key == pygame.K_3:
                        # Water crops
                        print("Watered crops! They grow faster!")

                # BANK actions
                elif building_type == "bank":
                    if event.key == pygame.K_1:
                        # Deposit
                        if coins >= 100:
                            coins = coins - 100
                            bank_balance = bank_balance + 100
                            print("Deposited 100 coins! Balance: " + str(bank_balance))
                        else:
                            print("Need 100 coins to deposit!")
                    elif event.key == pygame.K_2:
                        # Withdraw
                        if bank_balance >= 100:
                            bank_balance = bank_balance - 100
                            coins = coins + 100
                            print("Withdrew 100 coins! Balance: " + str(bank_balance))
                        else:
                            print("Not enough in bank!")
                    elif event.key == pygame.K_3:
                        # Collect interest (10% of balance)
                        interest = bank_balance // 10
                        if interest > 0:
                            bank_balance = bank_balance + interest
                            print("Collected " + str(interest) + " coins interest! Balance: " + str(bank_balance))
                        else:
                            print("No interest to collect yet!")

                # MARKET actions
                elif building_type == "market":
                    if event.key == pygame.K_1:
                        # Sell wood
                        if wood >= 10:
                            wood = wood - 10
                            earned = 10 * market_prices["wood"]
                            coins = coins + earned
                            print("Sold 10 wood for " + str(earned) + " coins!")
                        else:
                            print("Need 10 wood to sell!")
                    elif event.key == pygame.K_2:
                        # Sell stone
                        if stone >= 10:
                            stone = stone - 10
                            earned = 10 * market_prices["stone"]
                            coins = coins + earned
                            print("Sold 10 stone for " + str(earned) + " coins!")
                        else:
                            print("Need 10 stone to sell!")
                    elif event.key == pygame.K_3:
                        # Sell iron
                        if iron >= 5:
                            iron = iron - 5
                            earned = 5 * market_prices["iron"]
                            coins = coins + earned
                            print("Sold 5 iron for " + str(earned) + " coins!")
                        else:
                            print("Need 5 iron to sell!")
                    elif event.key == pygame.K_4:
                        # Sell gold
                        if gold >= 1:
                            gold = gold - 1
                            earned = market_prices["gold"]
                            coins = coins + earned
                            print("Sold 1 gold for " + str(earned) + " coins!")
                        else:
                            print("Need gold to sell!")

                # BARRACKS actions
                elif building_type == "barracks":
                    if event.key == pygame.K_1:
                        # Train soldier (costs 1 homeless villager + 50 iron)
                        homeless_villager = None
                        for v in villagers:
                            if v[0] == inside_building[0] and v[3] == "homeless":
                                homeless_villager = v
                                break
                        if homeless_villager and iron >= 50:
                            villagers.remove(homeless_villager)
                            population = population - 1
                            iron = iron - 50
                            soldiers = soldiers + 1
                            army_power = army_power + 10
                            print("Trained a soldier! Army: " + str(soldiers) + " Power: " + str(army_power))
                        elif not homeless_villager:
                            print("Need a homeless villager to train!")
                        else:
                            print("Need 50 iron to train a soldier!")
                    elif event.key == pygame.K_2:
                        # Upgrade army power
                        if coins >= 100:
                            coins = coins - 100
                            army_power = army_power + 50
                            print("Army upgraded! Power: " + str(army_power))
                        else:
                            print("Need 100 coins!")
                    elif event.key == pygame.K_3:
                        # Deploy to defense
                        print("Soldiers deployed to defend the planet!")

                # HOUSE actions
                elif building_type == "house":
                    if event.key == pygame.K_1:
                        # Rest
                        lives = min(lives + 1, 5)
                        print("Rested! Lives: " + str(lives))
                    elif event.key == pygame.K_2:
                        # Check happiness
                        happy_count = sum(1 for v in villagers if v[0] == inside_building[0] and v[4] > 50)
                        print("Happy villagers: " + str(happy_count))

                # TAVERN actions
                elif building_type == "tavern":
                    if event.key == pygame.K_1:
                        # Buy drink
                        if coins >= 5:
                            coins = coins - 5
                            for v in villagers:
                                if v[0] == inside_building[0]:
                                    v[4] = min(100, v[4] + 10)  # Increase happiness
                            print("Bought drinks! Villagers are happier!")
                        else:
                            print("Need 5 coins!")
                    elif event.key == pygame.K_2:
                        # Listen to stories
                        print("You hear tales of distant galaxies...")
                    elif event.key == pygame.K_3:
                        # Recruit adventurer
                        if coins >= 50:
                            coins = coins - 50
                            vx = random.randint(100, SCREEN_WIDTH - 100)
                            vy = random.randint(100, SCREEN_HEIGHT - 100)
                            villagers.append([inside_building[0], vx, vy, "homeless", 80, 0, 0])
                            population = population + 1
                            print("Recruited an adventurer!")
                        else:
                            print("Need 50 coins to recruit!")

                # WAREHOUSE actions
                elif building_type == "warehouse":
                    if event.key == pygame.K_1:
                        print("Storage organized!")
                    elif event.key == pygame.K_2:
                        print("Inventory: " + str(materials) + " mat, " + str(wood) + " wood, " + str(stone) + " stone, " + str(iron) + " iron, " + str(gold) + " gold")

                # HOSPITAL actions
                elif building_type == "hospital":
                    if event.key == pygame.K_1:
                        # Heal villagers
                        if coins >= 50:
                            coins = coins - 50
                            for v in villagers:
                                if v[0] == inside_building[0]:
                                    v[4] = 100  # Full happiness/health
                            print("All villagers healed!")
                        else:
                            print("Need 50 coins!")
                    elif event.key == pygame.K_2:
                        print("Trained a medic!")

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
                            print("Bought SHIELD! You have " + str(shield_hits) + " shield(s)!")

                    # Try to buy FAST SHOOTING!
                    elif selected_item["name"] == "FAST SHOOTING":
                        if coins >= FAST_SHOOTING_PRICE and not has_fast_shooting:
                            coins = coins - FAST_SHOOTING_PRICE
                            has_fast_shooting = True
                            print("Bought FAST SHOOTING!")

                    # Try to buy BIG LASER!
                    elif selected_item["name"] == "BIG LASER":
                        if coins >= BIG_LASER_PRICE and not has_big_laser:
                            coins = coins - BIG_LASER_PRICE
                            has_big_laser = True
                            print("Bought BIG LASER!")

                    # Try to buy a WINGMAN!
                    elif selected_item["name"] == "WINGMAN":
                        if coins >= WINGMAN_PRICE:
                            coins = coins - WINGMAN_PRICE
                            wingmen_count = wingmen_count + 1
                            print("Bought WINGMAN! You have " + str(wingmen_count) + " wingmen!")

                    # Go to SKIN SHOP!
                    elif selected_item["name"] == "SKINS":
                        game_state = "skin_shop"
                        skin_shop_selection = 0

            # --- LOBBY CONTROLS! ---
            # In the lobby, use UP/DOWN to pick options and ENTER to select!
            if event.type == pygame.KEYDOWN and game_state == "lobby":
                # Move UP in the lobby menu
                if event.key == pygame.K_UP:
                    lobby_selection = lobby_selection - 1
                    quit_confirm = False  # Cancel quit confirmation when moving
                    if lobby_selection < 0:
                        lobby_selection = 3  # 4 options: Shop, Continue, Leaderboard, Quit

                # Move DOWN in the lobby menu
                if event.key == pygame.K_DOWN:
                    lobby_selection = lobby_selection + 1
                    quit_confirm = False  # Cancel quit confirmation when moving
                    if lobby_selection > 3:
                        lobby_selection = 0  # Wrap to top!

                # ESC to cancel quit confirmation
                if event.key == pygame.K_ESCAPE:
                    quit_confirm = False

                # ENTER to pick the selected option!
                if event.key == pygame.K_RETURN:
                    if lobby_selection == 0:
                        # SHOP - Go buy stuff!
                        game_state = "shop"
                        shop_selection = 0
                    elif lobby_selection == 1:
                        # CONTINUE - Go back to space exploration!
                        game_state = "playing"
                    elif lobby_selection == 2:
                        # LEADERBOARD - View high scores!
                        game_state = "leaderboard"
                    elif lobby_selection == 3:
                        # QUIT TO TITLE - Need to confirm first!
                        if quit_confirm:
                            # Already confirmed, actually quit!
                            game_state = "title"
                            title_timer = 0
                            quit_confirm = False
                        else:
                            # First press - ask for confirmation
                            quit_confirm = True

            # --- SKIN SHOP CONTROLS! ---
            if event.type == pygame.KEYDOWN and game_state == "skin_shop":
                # Move LEFT in skin selection
                if event.key == pygame.K_LEFT:
                    skin_shop_selection = skin_shop_selection - 1
                    if skin_shop_selection < 0:
                        skin_shop_selection = len(all_skins) - 1

                # Move RIGHT in skin selection
                if event.key == pygame.K_RIGHT:
                    skin_shop_selection = skin_shop_selection + 1
                    if skin_shop_selection >= len(all_skins):
                        skin_shop_selection = 0

                # ENTER to buy/equip skin
                if event.key == pygame.K_RETURN:
                    selected_skin = all_skins[skin_shop_selection]
                    if selected_skin["name"] in owned_skins:
                        # Already own it - equip it!
                        current_skin = selected_skin["name"]
                        save_skins(current_skin, owned_skins)
                        print("Equipped " + selected_skin["display"] + "!")
                    else:
                        # Try to buy it!
                        if coins >= selected_skin["price"]:
                            coins = coins - selected_skin["price"]
                            owned_skins.append(selected_skin["name"])
                            current_skin = selected_skin["name"]
                            save_skins(current_skin, owned_skins)
                            print("Bought and equipped " + selected_skin["display"] + "!")
                        else:
                            print("Need more coins!")

                # ESCAPE to go back to shop
                if event.key == pygame.K_ESCAPE:
                    game_state = "shop"

                # D to open drawing tool (for custom skin)
                if event.key == pygame.K_d:
                    game_state = "skin_editor"

            # --- STORY ENDING CONTROLS! ---
            if event.type == pygame.KEYDOWN and game_state == "story_ending":
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    story_page = story_page + 1
                    if story_page >= 5:  # 5 pages of story
                        # Reset everything for a new game!
                        game_state = "title"
                        story_page = 0
                        level = 1
                        score = 0
                        lives = 5

            # --- SKIN EDITOR CONTROLS! ---
            if event.type == pygame.KEYDOWN and game_state == "skin_editor":
                # Change color with LEFT/RIGHT
                if event.key == pygame.K_LEFT:
                    drawing_color_index = drawing_color_index - 1
                    if drawing_color_index < 0:
                        drawing_color_index = len(drawing_colors) - 1
                    drawing_color = drawing_colors[drawing_color_index]
                if event.key == pygame.K_RIGHT:
                    drawing_color_index = drawing_color_index + 1
                    if drawing_color_index >= len(drawing_colors):
                        drawing_color_index = 0
                    drawing_color = drawing_colors[drawing_color_index]
                # C to clear drawing
                if event.key == pygame.K_c:
                    custom_skin_pixels = []
                # S to save and equip custom skin
                if event.key == pygame.K_s:
                    if "custom" not in owned_skins:
                        if coins >= 100:
                            coins = coins - 100
                            owned_skins.append("custom")
                    current_skin = "custom"
                    save_skins(current_skin, owned_skins)
                    print("Custom skin equipped!")
                # ESCAPE to go back to skin shop
                if event.key == pygame.K_ESCAPE:
                    game_state = "skin_shop"

            # --- SKIN EDITOR MOUSE DRAWING! ---
            if game_state == "skin_editor":
                if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]):
                    mx, my = pygame.mouse.get_pos()
                    # Drawing area is 32x32 pixels, scaled up to 256x256 on screen
                    # Centered at screen
                    draw_area_x = SCREEN_WIDTH // 2 - 128
                    draw_area_y = SCREEN_HEIGHT // 2 - 128
                    if draw_area_x <= mx <= draw_area_x + 256 and draw_area_y <= my <= draw_area_y + 256:
                        # Convert screen position to pixel position (0-31)
                        pixel_x = (mx - draw_area_x) // 8
                        pixel_y = (my - draw_area_y) // 8
                        # Add pixel if not already there
                        new_pixel = [pixel_x, pixel_y, drawing_color]
                        # Remove old pixel at same position
                        custom_skin_pixels = [p for p in custom_skin_pixels if not (p[0] == pixel_x and p[1] == pixel_y)]
                        custom_skin_pixels.append(new_pixel)

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
            current_speed = thrawn_speed * dt
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                current_speed = current_speed * 1.5  # BOOST!

            # Move Thrawn directly (no drift)
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                thrawn_x = thrawn_x - current_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                thrawn_x = thrawn_x + current_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                thrawn_y = thrawn_y - current_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                thrawn_y = thrawn_y + current_speed

            # Keep Thrawn on screen
            thrawn_x = max(25, min(SCREEN_WIDTH - 25, thrawn_x))
            thrawn_y = max(30, min(SCREEN_HEIGHT - 20, thrawn_y))

            # Also update world position (for planet discovery) - VERY slow scrolling
            # Planets move slowly and stay in view longer!
            player_world_x = player_world_x + (thrawn_x - SCREEN_WIDTH // 2) * 0.02
            player_world_y = player_world_y + (thrawn_y - SCREEN_HEIGHT // 2) * 0.02

            # Keep in world bounds
            player_world_x = max(50, min(WORLD_WIDTH - 50, player_world_x))
            player_world_y = max(50, min(WORLD_HEIGHT - 50, player_world_y))

            # Camera slowly follows world position (for planet background)
            camera_x = player_world_x - SCREEN_WIDTH // 2
            camera_y = player_world_y - SCREEN_HEIGHT // 2
            camera_x = max(0, min(WORLD_WIDTH - SCREEN_WIDTH, camera_x))
            camera_y = max(0, min(WORLD_HEIGHT - SCREEN_HEIGHT, camera_y))

            # Check if near any planets!
            near_planet = None
            for planet in planets:
                px, py = planet[0], planet[1]
                dist = ((player_world_x - px) ** 2 + (player_world_y - py) ** 2) ** 0.5
                planet_size = planet[4]

                # Discover planet if close enough!
                if dist < planet_size + 200:
                    if not planet[5]:  # Not discovered yet?
                        planet[5] = True  # DISCOVERED!
                        print("DISCOVERED: " + planet[2] + "!")

                # Near enough to land?
                if dist < planet_size + 150:
                    near_planet = planet

        # --- ON PLANET MOVEMENT AND COLLECTION! ---
        if game_state == "on_planet":
            keys = pygame.key.get_pressed()
            move_speed = 5 * dt

            # Move around the planet surface!
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                planet_explore_x = planet_explore_x - move_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                planet_explore_x = planet_explore_x + move_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                planet_explore_y = planet_explore_y - move_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                planet_explore_y = planet_explore_y + move_speed

            # Keep on screen
            planet_explore_x = max(30, min(SCREEN_WIDTH - 30, planet_explore_x))
            planet_explore_y = max(30, min(SCREEN_HEIGHT - 30, planet_explore_y))

            # Collect materials!
            materials_to_remove = []
            for mat in planet_materials:
                dist = ((planet_explore_x - mat[0]) ** 2 + (planet_explore_y - mat[1]) ** 2) ** 0.5
                if dist < 40:  # Close enough to collect!
                    materials_to_remove.append(mat)
                    # Different materials give different resources!
                    if mat[2] == "crystal":
                        materials = materials + 5
                        gold = gold + 1  # Crystals contain gold!
                        print("Collected crystal! Materials: " + str(materials) + " Gold: " + str(gold))
                    elif mat[2] == "metal":
                        materials = materials + 3
                        iron = iron + 2  # Metal = iron!
                        print("Collected metal! Materials: " + str(materials) + " Iron: " + str(iron))
                    elif mat[2] == "wood":
                        materials = materials + 2
                        wood = wood + 3  # Wood for building!
                        print("Collected wood! Wood: " + str(wood))
                    elif mat[2] == "stone":
                        materials = materials + 2
                        stone = stone + 2  # Stone for strong buildings!
                        print("Collected stone! Stone: " + str(stone))
                    else:  # rock
                        materials = materials + 1
                        stone = stone + 1  # Rocks give stone too!
                        print("Collected rock! Materials: " + str(materials))

            for mat in materials_to_remove:
                planet_materials.remove(mat)

            # Collect food!
            food_to_remove = []
            for fd in planet_food:
                dist = ((planet_explore_x - fd[0]) ** 2 + (planet_explore_y - fd[1]) ** 2) ** 0.5
                if dist < 40:  # Close enough to collect!
                    food_to_remove.append(fd)
                    if fd[2] == "apple":
                        food = min(100, food + 15)
                    elif fd[2] == "meat":
                        food = min(100, food + 25)
                    else:  # berry
                        food = min(100, food + 10)
                    print("Ate " + fd[2] + "! Food: " + str(int(food)))

            for fd in food_to_remove:
                planet_food.remove(fd)

            # --- VILLAGER MOVEMENT! ---
            # Villagers walk towards their assigned buildings!
            villager_speed = 1.5 * dt
            for v in villagers:
                if v[0] == current_planet_name and v[3] != "homeless":
                    # Check if villager has a target position
                    if len(v) >= 7 and (v[5] != 0 or v[6] != 0):
                        target_x = v[5]
                        target_y = v[6]

                        # Move towards target
                        dx = target_x - v[1]
                        dy = target_y - v[2]
                        dist = (dx * dx + dy * dy) ** 0.5

                        if dist > 30:  # Not at building yet
                            # Normalize and move
                            v[1] = v[1] + (dx / dist) * villager_speed
                            v[2] = v[2] + (dy / dist) * villager_speed
                        else:
                            # At building! Do a little wobble to look busy
                            v[1] = target_x + random.randint(-20, 20) * 0.1
                            v[2] = target_y + random.randint(-20, 20) * 0.1

                # Homeless villagers wander randomly
                elif v[0] == current_planet_name and v[3] == "homeless":
                    if random.random() < 0.02:  # Occasionally change direction
                        v[1] = v[1] + random.randint(-30, 30)
                        v[2] = v[2] + random.randint(-30, 30)
                    # Keep on screen
                    v[1] = max(50, min(SCREEN_WIDTH - 50, v[1]))
                    v[2] = max(50, min(SCREEN_HEIGHT - 50, v[2]))

        # --- PLANET ECONOMIES (BACKGROUND)! ---
        # All planets produce/consume even when you're not there!
        # This runs every frame for ALL planets!
        economy_dt = delta_ms / 1000.0  # Convert to seconds
        for planet in planets:
            planet_name = planet[2]
            if planet_name not in planet_economy:
                continue

            eco = planet_economy[planet_name]

            # Count farmers and villagers on this planet
            farmers_here = sum(1 for v in villagers if v[0] == planet_name and v[3] == "farmer")
            villagers_here = sum(1 for v in villagers if v[0] == planet_name)

            # Count farms on this planet
            farms_here = sum(1 for b in buildings if b[0] == planet_name and b[3] == "farm")

            # PRODUCTION: Farmers produce food (need a farm to work at!)
            if farms_here > 0 and farmers_here > 0:
                food_produced = min(farmers_here, farms_here * 3) * FOOD_PER_FARMER * economy_dt
                eco["food_supply"] = eco["food_supply"] + food_produced

            # CONSUMPTION: Villagers eat food
            if villagers_here > 0:
                food_eaten = villagers_here * FOOD_PER_VILLAGER * economy_dt
                eco["food_supply"] = eco["food_supply"] - food_eaten

                # If no food, villagers get unhappy!
                if eco["food_supply"] < 0:
                    eco["food_supply"] = 0
                    for v in villagers:
                        if v[0] == planet_name:
                            v[4] = max(0, v[4] - 0.1 * economy_dt)  # Lose happiness

            # Cap food supply at 200
            eco["food_supply"] = min(200, eco["food_supply"])

        # --- HUNGER! ---
        # Food decreases while playing (you get hungry!)
        if game_state == "playing" and not game_over:
            food = food - hunger_rate * dt
            if food <= 0:
                food = 0
                # Starving = lose health!
                lives = lives - 1
                food = 30  # Get a little food back
                print("STARVING! Lost a life!")

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

        # --- TURRETS ON PLANETS SHOOT AT ENEMIES! ---
        # Turrets you built on planets will help you fight!
        if not game_over and game_state == "playing":
            turret_shoot_timer = turret_shoot_timer + delta_ms

            # Turrets shoot every 1.5 seconds
            shoot_rate = 1500

            if turret_shoot_timer >= shoot_rate:
                # Check each building - if it's a turret and on screen, shoot!
                for building in buildings:
                    if building[3] == "turret":
                        # Find which planet this turret is on
                        turret_planet = None
                        for planet in planets:
                            if planet[2] == building[0]:  # Match planet name
                                turret_planet = planet
                                break

                        if turret_planet is not None:
                            # Get planet's screen position
                            planet_screen_x = turret_planet[0] - camera_x
                            planet_screen_y = turret_planet[1] - camera_y

                            # Only shoot if planet is on screen!
                            if planet_screen_x > -100 and planet_screen_x < SCREEN_WIDTH + 100:
                                if planet_screen_y > -100 and planet_screen_y < SCREEN_HEIGHT + 100:
                                    # Find a target (zelda or boss!)
                                    target = None

                                    # First try to target the boss if there is one!
                                    if boss_active and boss_x > 0 and boss_x < SCREEN_WIDTH:
                                        target = [boss_x, boss_y]

                                    # Otherwise target a random zelda!
                                    elif len(zeldas) > 0:
                                        target = random.choice(zeldas)

                                    # If we found a target, shoot at it!
                                    if target is not None:
                                        # Turret laser comes from the planet!
                                        start_x = planet_screen_x
                                        start_y = planet_screen_y

                                        # Calculate direction to target
                                        dx = target[0] - start_x
                                        dy = target[1] - start_y
                                        dist = max(1, (dx * dx + dy * dy) ** 0.5)

                                        # Normalize and set speed
                                        turret_speed = 8
                                        dx = (dx / dist) * turret_speed
                                        dy = (dy / dist) * turret_speed

                                        # Create the turret laser! [x, y, dx, dy]
                                        turret_lasers.append([start_x, start_y, dx, dy])

                turret_shoot_timer = 0

        # --- TURRETS GET HIT BY ENEMY WEAPONS! ---
        # Swords can destroy turrets on visible planets!
        buildings_to_remove = []
        for building in buildings:
            if building[3] == "turret":
                # Find which planet this turret is on
                turret_planet = None
                for planet in planets:
                    if planet[2] == building[0]:
                        turret_planet = planet
                        break

                if turret_planet is not None:
                    # Get planet's screen position
                    planet_screen_x = turret_planet[0] - camera_x
                    planet_screen_y = turret_planet[1] - camera_y

                    # Only check hits if planet is on screen
                    if planet_screen_x > -100 and planet_screen_x < SCREEN_WIDTH + 100:
                        if planet_screen_y > -100 and planet_screen_y < SCREEN_HEIGHT + 100:
                            # Initialize health if not set (old turrets)
                            if len(building) < 5:
                                building.append(3)  # Add health = 3

                            # Check if hit by swords
                            for sword in swords:
                                dist = ((planet_screen_x - sword[0]) ** 2 + (planet_screen_y - sword[1]) ** 2) ** 0.5
                                if dist < 50:
                                    building[4] = building[4] - 1  # Lose health!
                                    if sword in swords:
                                        swords.remove(sword)
                                    explosions.append([int(planet_screen_x), int(planet_screen_y), 0])
                                    if building[4] <= 0:
                                        buildings_to_remove.append(building)
                                        print("A turret on " + building[0] + " was destroyed!")
                                    break

                            # Check if hit by boss lasers
                            for blaser in boss_lasers:
                                dist = ((planet_screen_x - blaser[0]) ** 2 + (planet_screen_y - blaser[1]) ** 2) ** 0.5
                                if dist < 50:
                                    building[4] = building[4] - 1  # Lose health!
                                    if blaser in boss_lasers:
                                        boss_lasers.remove(blaser)
                                    explosions.append([int(planet_screen_x), int(planet_screen_y), 0])
                                    if building[4] <= 0:
                                        buildings_to_remove.append(building)
                                        print("A turret on " + building[0] + " was destroyed!")
                                    break

        # Remove destroyed turrets
        for building in buildings_to_remove:
            if building in buildings:
                buildings.remove(building)

        # --- MOVE TURRET LASERS ---
        for laser in turret_lasers:
            laser[0] = laser[0] + laser[2] * dt  # Move x
            laser[1] = laser[1] + laser[3] * dt  # Move y

        # Remove turret lasers that went off screen
        turret_lasers_to_keep = []
        for laser in turret_lasers:
            if laser[1] > -50 and laser[1] < SCREEN_HEIGHT + 50:
                if laser[0] > -50 and laser[0] < SCREEN_WIDTH + 50:
                    turret_lasers_to_keep.append(laser)
        turret_lasers = turret_lasers_to_keep

        # --- TURRET LASERS HIT ENEMIES! ---
        # Check if turret lasers hit zeldas!
        zeldas_hit = []
        lasers_used = []
        for laser in turret_lasers:
            for zelda in zeldas:
                # Check distance between laser and zelda
                dist = ((laser[0] - zelda[0]) ** 2 + (laser[1] - zelda[1]) ** 2) ** 0.5
                if dist < 35:  # Hit!
                    if zelda not in zeldas_hit:
                        zeldas_hit.append(zelda)
                    if laser not in lasers_used:
                        lasers_used.append(laser)
                    score = score + 5  # Bonus points for turret kills!

        # Remove hit zeldas and used lasers
        for zelda in zeldas_hit:
            if zelda in zeldas:
                zeldas.remove(zelda)
                # Add explosion!
                explosions.append([zelda[0], zelda[1], 0])
        for laser in lasers_used:
            if laser in turret_lasers:
                turret_lasers.remove(laser)

        # Check if turret lasers hit the boss!
        if boss_active:
            for laser in turret_lasers:
                dist = ((laser[0] - boss_x) ** 2 + (laser[1] - boss_y) ** 2) ** 0.5
                if dist < 60:  # Hit the boss!
                    boss_health = boss_health - 1
                    if laser in turret_lasers:
                        turret_lasers.remove(laser)
                    # Add small explosion
                    explosions.append([laser[0], laser[1], 0])

        # --- TREASURE CHESTS! ---
        # --- ROBOT FACTORY SPAWNS HELPER ROBOTS! ---
        if game_state == "playing" and not game_over:
            factory_spawn_timer = factory_spawn_timer + delta_ms
            # Count how many factories we have
            factory_count = 0
            for building in buildings:
                if building[3] == "factory":
                    factory_count = factory_count + 1

            # Spawn robots every 5 seconds if we have factories!
            # Max 5 robots at a time!
            MAX_ROBOTS = 5
            if factory_count > 0 and factory_spawn_timer >= 5000 and len(helper_robots) < MAX_ROBOTS:
                factory_spawn_timer = 0
                # Spawn one robot per factory (up to max!)
                robots_to_spawn = min(factory_count, MAX_ROBOTS - len(helper_robots))
                for i in range(robots_to_spawn):
                    # Robot spawns from bottom of screen
                    robot_x = random.randint(100, SCREEN_WIDTH - 100)
                    robot_y = SCREEN_HEIGHT + 30
                    helper_robots.append([robot_x, robot_y, 0, 0, 0])  # x, y, target_x, target_y, shoot_timer
                    print("Robot helper deployed! (" + str(len(helper_robots)) + "/" + str(MAX_ROBOTS) + ")")

        # --- MOVE HELPER ROBOTS! ---
        robots_to_remove = []
        for robot in helper_robots:
            # Find nearest enemy to target
            nearest_dist = 9999
            nearest_target = None
            # Check zeldas
            for zelda in zeldas:
                dist = ((robot[0] - zelda[0]) ** 2 + (robot[1] - zelda[1]) ** 2) ** 0.5
                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest_target = zelda
            # Check boss if active
            if boss_active and nearest_dist > 200:
                nearest_target = [boss_x, boss_y]
                nearest_dist = ((robot[0] - boss_x) ** 2 + (robot[1] - boss_y) ** 2) ** 0.5

            # Move robot towards target (or hover in position)
            if nearest_target is not None:
                robot[2] = nearest_target[0]
                robot[3] = nearest_target[1]
                # Move towards target
                dx = robot[2] - robot[0]
                dy = robot[3] - robot[1]
                dist = max(1, (dx * dx + dy * dy) ** 0.5)
                robot_speed = 3 * dt
                robot[0] = robot[0] + (dx / dist) * robot_speed
                robot[1] = robot[1] + (dy / dist) * robot_speed
            else:
                # No target - fly up slowly
                robot[1] = robot[1] - 1 * dt

            # Keep robot on screen
            robot[0] = max(30, min(SCREEN_WIDTH - 30, robot[0]))
            robot[1] = max(50, min(SCREEN_HEIGHT - 50, robot[1]))

            # Robot shoots at enemies!
            robot[4] = robot[4] + delta_ms
            if robot[4] >= 800 and nearest_target is not None:  # Shoot every 0.8 seconds
                robot[4] = 0
                # Calculate direction to target
                dx = nearest_target[0] - robot[0]
                dy = nearest_target[1] - robot[1]
                dist = max(1, (dx * dx + dy * dy) ** 0.5)
                speed = 10
                turret_lasers.append([robot[0], robot[1], (dx / dist) * speed, (dy / dist) * speed])

            # Remove robot if it goes off screen (after 30 seconds of life)
            if robot[1] < -100:
                robots_to_remove.append(robot)

        for robot in robots_to_remove:
            if robot in helper_robots:
                helper_robots.remove(robot)

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

                # --- MEGA WORM MOVEMENT ---
                elif boss_type == "mega_worm":
                    # Slithers like a snake across the screen!
                    dragon_fire_timer = dragon_fire_timer + 0.04 * dt
                    boss_x = SCREEN_WIDTH // 2 + math.sin(dragon_fire_timer * 1.5) * 400
                    boss_y = 80 + math.sin(dragon_fire_timer * 3) * 30

                # --- DEATH STAR MOVEMENT ---
                elif boss_type == "death_star":
                    # Slow and menacing, hovers in the center!
                    boss_x = SCREEN_WIDTH // 2 + math.sin(dragon_fire_timer * 0.3) * 100
                    boss_y = 100
                    dragon_fire_timer = dragon_fire_timer + 0.02 * dt

                # --- THE BUGGER MOVEMENT ---
                elif boss_type == "the_bugger":
                    # Erratic bug movement - jumps around!
                    dance_angle = dance_angle + 0.08 * dt
                    boss_x = SCREEN_WIDTH // 2 + math.sin(dance_angle * 4) * 350
                    boss_y = 100 + abs(math.sin(dance_angle * 6)) * 60

                # --- DANCING APPLE MOVEMENT ---
                elif boss_type == "dancing_apple":
                    # Happy dancing movement! Bounces and spins!
                    dance_angle = dance_angle + 0.1 * dt
                    boss_x = SCREEN_WIDTH // 2 + math.sin(dance_angle * 3) * 300
                    # Bouncy up and down like dancing!
                    boss_y = 120 + abs(math.sin(dance_angle * 8)) * 50

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
                elif boss_type == "mega_worm":
                    # Spits acid in waves!
                    for i in range(5):
                        angle = -0.2 + i * 0.1
                        boss_lasers.append([boss_x, boss_y + 30, angle])
                    # Also spawns mini zeldas!
                    if random.randint(0, 100) < 30:
                        zeldas.append([boss_x, boss_y + 50, random.choice([-1, 1])])
                elif boss_type == "death_star":
                    # SUPER LASER! One massive beam that spreads!
                    for i in range(12):
                        angle = -0.6 + i * 0.1
                        boss_lasers.append([boss_x, boss_y + 60, angle])
                elif boss_type == "the_bugger":
                    # Shoots bug spit everywhere chaotically!
                    for i in range(6):
                        angle = random.uniform(-0.5, 0.5)
                        boss_lasers.append([boss_x + random.randint(-50, 50), boss_y + 40, angle])
                elif boss_type == "dancing_apple":
                    # Shoots apple seeds in a spiral pattern!
                    for i in range(8):
                        angle = -0.4 + i * 0.1 + math.sin(dance_angle) * 0.2
                        boss_lasers.append([boss_x + random.randint(-30, 30), boss_y + 50, angle])
                    # Sometimes spawns worm helpers!
                    if random.randint(0, 100) < 20:
                        zeldas.append([boss_x - 40, boss_y + 60, -1])
                        zeldas.append([boss_x + 40, boss_y + 60, 1])
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

            # After 3 seconds (3000ms), go to the SHOP!
            if level_complete_timer > 3000:
                # PLANET CLEARED! Time to shop!
                level = level + 1  # You've beaten more planets!
                level_complete = False
                level_complete_timer = 0
                boss_defeated = False
                boss_defeated_timer = 0

                # Go to LOBBY after beating a boss!
                game_state = "lobby"
                lobby_selection = 0
                lobby_reason = "level"  # We beat the level!
                quit_confirm = False  # Reset quit confirmation
                # Center camera on player
                camera_x = player_world_x - SCREEN_WIDTH // 2
                camera_y = player_world_y - SCREEN_HEIGHT // 2

                # Reset Thrawn to starting position for next battle
                thrawn_x = SCREEN_WIDTH // 2
                thrawn_y = SCREEN_HEIGHT // 2

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

                # Reset difficulty for next planet - ZELDAS GET STRONGER!
                zelda_speed = 1.5 + (level * 0.2)  # Faster each level!
                zelda_spawn_rate = max(800, 2000 - (level * 150))  # Spawn faster!
                sword_rate = max(500, 1500 - (level * 100))  # Throw swords faster!
                boss_max_health = 20 + (level * 5)  # Harder on each planet!

                # Cycle through different bosses based on level!
                # Level 1: Star Destroyer, 2: Zelda Queen, 3: Giant Robot,
                # 4: Space Dragon, 5: Dancing 67, 6: Mega Worm,
                # 7: Death Star, 8: The Bugger (giant bug!)
                boss_types = ["star_destroyer", "zelda_queen", "giant_robot", "space_dragon", "dancing_67", "mega_worm", "death_star", "the_bugger", "dancing_apple"]
                boss_type = boss_types[(level - 1) % len(boss_types)]


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
                # REFUGEES! Sometimes survivors escape destroyed enemy ships!
                if random.random() < 0.15:  # 15% chance of refugees
                    refugees_waiting = refugees_waiting + random.randint(1, 3)
                    print("Refugees escaped! " + str(refugees_waiting) + " waiting!")

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
                # CHECK FOR GAME ENDING AT LEVEL 2000!
                if level >= 2000:
                    game_state = "story_ending"

        # --- BOSS LASERS HIT PLAYER? ---
        # Check if boss's green lasers hit the player (astronaut or ship)!
        boss_lasers_to_remove = []
        for laser in boss_lasers:
            # Use astronaut position when on planet, ship position in space!
            if on_planet:
                player_hit_x = planet_explore_x
                player_hit_y = planet_explore_y
                hit_range_x = 20  # Smaller hitbox for astronaut
                hit_range_y = 25
            else:
                player_hit_x = thrawn_x
                player_hit_y = thrawn_y
                hit_range_x = 25  # Normal hitbox for ship
                hit_range_y = 30

            distance_x = abs(laser[0] - player_hit_x)
            distance_y = abs(laser[1] - player_hit_y)

            if distance_x < hit_range_x and distance_y < hit_range_y:
                boss_lasers_to_remove.append(laser)
                # SHIELD CHECK! Does the shield block it?
                if shield_hits > 0:
                    shield_hits = shield_hits - 1  # Shield takes the hit!
                    print("Shield blocked! " + str(shield_hits) + " shields left!")
                else:
                    lives = lives - 1  # No shield? Lose a life!
                explosions.append([int(player_hit_x), int(player_hit_y), 300])

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

        # --- ZELDA HITS PLAYER? OUCH! ---
        # Check if any Zelda crashed into player (astronaut or ship)!
        for zelda in zeldas:
            # Use astronaut position when on planet, ship position in space!
            if on_planet:
                player_hit_x = planet_explore_x
                player_hit_y = planet_explore_y
                hit_range = 30  # Smaller hitbox for astronaut
            else:
                player_hit_x = thrawn_x
                player_hit_y = thrawn_y
                hit_range = 40  # Normal hitbox for ship

            distance_x = abs(zelda[0] - player_hit_x)
            distance_y = abs(zelda[1] - player_hit_y)

            # If Zelda is close to player = OUCH!
            if distance_x < hit_range and distance_y < hit_range:
                zeldas.remove(zelda)  # Remove the Zelda
                # SHIELD CHECK! Does the shield block it?
                if shield_hits > 0:
                    shield_hits = shield_hits - 1  # Shield takes the hit!
                    print("Shield blocked! " + str(shield_hits) + " shields left!")
                else:
                    lives = lives - 1  # No shield? Lose a life!
                # Make an explosion where player got hit!
                explosions.append([int(player_hit_x), int(player_hit_y), 300])

        # --- SWORD HITS PLAYER? OUCH! ---
        # Check if any sword hit the player (astronaut on planet or ship in space)!
        swords_to_remove = []
        for sword in swords:
            # Use astronaut position when on planet, ship position in space!
            if on_planet:
                player_hit_x = planet_explore_x
                player_hit_y = planet_explore_y
                hit_range_x = 20  # Smaller hitbox for astronaut
                hit_range_y = 25
            else:
                player_hit_x = thrawn_x
                player_hit_y = thrawn_y
                hit_range_x = 25  # Normal hitbox for ship
                hit_range_y = 30

            distance_x = abs(sword[0] - player_hit_x)
            distance_y = abs(sword[1] - player_hit_y)

            # If sword is close to player = HIT!
            if distance_x < hit_range_x and distance_y < hit_range_y:
                swords_to_remove.append(sword)  # Remove the sword
                # SHIELD CHECK! Does the shield block it?
                if shield_hits > 0:
                    shield_hits = shield_hits - 1  # Shield takes the hit!
                    print("Shield blocked! " + str(shield_hits) + " shields left!")
                else:
                    lives = lives - 1  # No shield? Lose a life!
                # Make an explosion where player got hit!
                explosions.append([int(player_hit_x), int(player_hit_y), 300])

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
                # SAVE TO LEADERBOARD before reset!
                final_score = score + coins  # Total progress this run
                if current_user != "" and final_score > 0:
                    leaderboard = save_to_leaderboard(current_user, final_score)
                    print("Final score: " + str(final_score) + " saved to leaderboard!")

                # ROGUELIKE: RESET EVERYTHING ON DEATH!
                print("=== GAME OVER - Starting fresh! ===")
                coins = STARTING_COINS  # Reset to starting coins
                score = 0
                materials = 0
                wood = 0
                stone = 0
                iron = 0
                gold = 0
                food = 100
                population = 0
                villagers = []
                soldiers = 0
                army_power = 0
                refugees_waiting = 0
                buildings = []
                bank_balance = 0
                # Reset planet economies
                for pname in planet_economy:
                    planet_economy[pname]["food_supply"] = 50
                    planet_economy[pname]["materials_supply"] = 0
                # Reset power-ups
                has_spread_shot = False
                has_homing_missiles = False
                has_piercing_laser = False
                has_double_points = False
                double_points_timer = 0
                homing_missiles = []
                wingmen = []
                wingmen_count = 0
                has_shield = False
                shield_hits = 0
                has_fast_shooting = False
                has_big_laser = False
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
                # Press any key to go to LOBBY!
                keys = pygame.key.get_pressed()
                if any(keys):
                    # Go to LOBBY after dying!
                    game_state = "lobby"
                    lobby_selection = 0
                    lobby_reason = "death"  # We died!
                    quit_confirm = False  # Reset quit confirmation

                    game_over = False
                    game_over_timer = 0
                    game_over_explosions = []

                    # Reset player stats
                    score = 0
                    lives = 3
                    level = 1

                    # Reset Thrawn position
                    thrawn_x = SCREEN_WIDTH // 2
                    thrawn_y = SCREEN_HEIGHT // 2
                    # Center camera on player
                    camera_x = player_world_x - SCREEN_WIDTH // 2
                    camera_y = player_world_y - SCREEN_HEIGHT // 2

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
                        # REALISTIC PLANET DRAWING!
                        # Outer atmosphere glow (soft halo)
                        for glow in range(3):
                            glow_size = size + 15 + glow * 5
                            glow_alpha = 30 - glow * 10
                            glow_color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50))
                            pygame.draw.circle(window, glow_color, (screen_x, screen_y), glow_size, 2)

                        # Main planet body
                        pygame.draw.circle(window, color, (screen_x, screen_y), size)

                        # Surface details - craters/features (darker spots)
                        crater_color = (max(0, color[0] - 40), max(0, color[1] - 40), max(0, color[2] - 40))
                        # Use planet position to make consistent craters
                        for c in range(3):
                            cx = screen_x + int(math.sin(planet[0] + c * 2) * size * 0.4)
                            cy = screen_y + int(math.cos(planet[1] + c * 3) * size * 0.3)
                            crater_size = int(size * 0.15) + c * 2
                            pygame.draw.circle(window, crater_color, (cx, cy), crater_size)

                        # Highlight (sun reflection) - top left
                        highlight_color = (min(255, color[0] + 60), min(255, color[1] + 60), min(255, color[2] + 60))
                        pygame.draw.circle(window, highlight_color, (screen_x - size//3, screen_y - size//3), size//4)

                        # Shadow on bottom right (3D effect)
                        shadow_color = (max(0, color[0] - 60), max(0, color[1] - 60), max(0, color[2] - 60))
                        pygame.draw.arc(window, shadow_color, (screen_x - size, screen_y - size, size*2, size*2),
                                       -0.5, 1.2, int(size * 0.3))

                        # Planet name with shadow
                        name_shadow = font.render(planet[2], True, (0, 0, 0))
                        name_text = font.render(planet[2], True, (255, 255, 255))
                        name_rect = name_text.get_rect(center=(screen_x, screen_y - size - 20))
                        window.blit(name_shadow, (name_rect.x + 2, name_rect.y + 2))
                        window.blit(name_text, name_rect)
                    else:
                        # Unknown planet - mysterious dark sphere
                        pygame.draw.circle(window, (30, 30, 40), (screen_x, screen_y), size)
                        pygame.draw.circle(window, (50, 50, 60), (screen_x, screen_y), size, 2)
                        # Mysterious glow
                        pygame.draw.circle(window, (40, 40, 60), (screen_x, screen_y), size + 8, 1)
                        question = font.render("?", True, (80, 80, 100))
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

            # Show "Press V to land" when near a planet!
            if near_planet is not None:
                land_text = medium_font.render("Press V to land on " + near_planet[2], True, (255, 255, 0))
                land_rect = land_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
                window.blit(land_text, land_rect)

            # Show turret count if you have turrets!
            turret_count = 0
            for building in buildings:
                if building[3] == "turret":
                    turret_count = turret_count + 1
            if turret_count > 0:
                turret_text = font.render("Turrets: " + str(turret_count), True, (100, 255, 100))
                window.blit(turret_text, (SCREEN_WIDTH - 120, 10))

        # --- DRAW PLANET SURFACE! ---
        if game_state == "on_planet":
            # Draw the planet surface (colored based on planet!)
            planet_color = current_planet[3] if current_planet else (100, 100, 100)
            window.fill((planet_color[0]//2, planet_color[1]//2, planet_color[2]//2))

            # Draw ground texture (simple lines)
            for i in range(0, SCREEN_WIDTH, 50):
                pygame.draw.line(window, planet_color, (i, 0), (i, SCREEN_HEIGHT), 1)
            for i in range(0, SCREEN_HEIGHT, 50):
                pygame.draw.line(window, planet_color, (0, i), (SCREEN_WIDTH, i), 1)

            # Draw buildings on this planet!
            for building in buildings:
                if building[0] == current_planet_name:
                    bx, by = int(building[1]), int(building[2])
                    if building[3] == "base":
                        # Base = big square
                        pygame.draw.rect(window, (100, 100, 200), (bx - 30, by - 30, 60, 60))
                        pygame.draw.rect(window, (150, 150, 255), (bx - 25, by - 25, 50, 50))
                        base_label = font.render("BASE", True, (255, 255, 255))
                        window.blit(base_label, (bx - 20, by - 10))
                    elif building[3] == "turret":
                        # Turret = triangle on circle
                        pygame.draw.circle(window, (200, 100, 100), (bx, by), 20)
                        pygame.draw.polygon(window, (255, 150, 150), [
                            (bx, by - 35), (bx - 15, by - 5), (bx + 15, by - 5)
                        ])
                    elif building[3] == "house":
                        # House = cute little house with roof!
                        pygame.draw.rect(window, (180, 130, 80), (bx - 20, by - 15, 40, 30))  # Walls
                        pygame.draw.polygon(window, (200, 80, 80), [
                            (bx - 25, by - 15), (bx, by - 40), (bx + 25, by - 15)  # Roof
                        ])
                        pygame.draw.rect(window, (100, 60, 40), (bx - 5, by, 10, 15))  # Door
                        pygame.draw.rect(window, (150, 200, 255), (bx + 8, by - 8, 8, 8))  # Window
                    elif building[3] == "spaceport":
                        # Space Port = landing pad with tower
                        pygame.draw.rect(window, (80, 80, 100), (bx - 40, by + 10, 80, 10))  # Landing pad
                        pygame.draw.rect(window, (100, 100, 120), (bx + 20, by - 40, 15, 50))  # Tower
                        pygame.draw.circle(window, (0, 255, 100), (bx + 27, by - 45), 5)  # Light
                    elif building[3] == "market":
                        # Market = stall with awning
                        pygame.draw.rect(window, (180, 140, 100), (bx - 25, by - 10, 50, 30))  # Counter
                        pygame.draw.rect(window, (200, 50, 50), (bx - 30, by - 25, 60, 15))  # Awning
                        pygame.draw.rect(window, (255, 200, 100), (bx - 30, by - 40, 60, 15))  # Stripes
                    elif building[3] == "barracks":
                        # Barracks = military building with flag
                        pygame.draw.rect(window, (100, 80, 60), (bx - 30, by - 20, 60, 40))  # Building
                        pygame.draw.rect(window, (60, 50, 40), (bx - 5, by, 10, 20))  # Door
                        pygame.draw.line(window, (80, 60, 40), (bx + 20, by - 20), (bx + 20, by - 50), 3)  # Flagpole
                        pygame.draw.rect(window, (255, 0, 0), (bx + 20, by - 50, 15, 10))  # Flag
                    elif building[3] == "tavern":
                        # Tavern = cozy building with sign
                        pygame.draw.rect(window, (140, 100, 60), (bx - 25, by - 15, 50, 35))  # Building
                        pygame.draw.polygon(window, (120, 80, 40), [
                            (bx - 30, by - 15), (bx, by - 35), (bx + 30, by - 15)
                        ])  # Roof
                        pygame.draw.circle(window, (255, 200, 50), (bx, by - 5), 8)  # Light/sign
                    elif building[3] == "warehouse":
                        # Warehouse = big storage building
                        pygame.draw.rect(window, (120, 120, 130), (bx - 35, by - 20, 70, 40))  # Building
                        pygame.draw.rect(window, (100, 100, 110), (bx - 30, by - 10, 25, 30))  # Door1
                        pygame.draw.rect(window, (100, 100, 110), (bx + 5, by - 10, 25, 30))  # Door2
                    elif building[3] == "farm":
                        # Farm = field with crops
                        pygame.draw.rect(window, (80, 50, 30), (bx - 25, by - 15, 50, 30))  # Field
                        for i in range(-20, 25, 10):
                            pygame.draw.line(window, (100, 200, 50), (bx + i, by - 10), (bx + i, by + 10), 2)  # Crops
                    elif building[3] == "bank":
                        # Bank = fancy building with columns
                        pygame.draw.rect(window, (200, 180, 150), (bx - 25, by - 15, 50, 30))  # Building
                        pygame.draw.rect(window, (180, 160, 130), (bx - 30, by - 25, 60, 10))  # Roof top
                        pygame.draw.line(window, (160, 140, 110), (bx - 20, by - 15), (bx - 20, by + 15), 4)  # Column
                        pygame.draw.line(window, (160, 140, 110), (bx + 20, by - 15), (bx + 20, by + 15), 4)  # Column
                        pygame.draw.circle(window, (255, 215, 0), (bx, by - 5), 8)  # Gold coin symbol
                    elif building[3] == "factory":
                        # Robot Factory
                        pygame.draw.rect(window, (80, 80, 90), (bx - 25, by - 20, 50, 40))
                        pygame.draw.rect(window, (100, 100, 110), (bx - 10, by - 35, 20, 15))  # Smokestack
                        pygame.draw.circle(window, (150, 150, 150), (bx, by), 12)  # Robot symbol

            # Draw materials to collect!
            for mat in planet_materials:
                mx, my = int(mat[0]), int(mat[1])
                if mat[2] == "crystal":
                    # Crystal = blue diamond (gives gold!)
                    pygame.draw.polygon(window, (100, 200, 255), [
                        (mx, my - 15), (mx + 10, my), (mx, my + 15), (mx - 10, my)
                    ])
                    pygame.draw.polygon(window, (150, 230, 255), [
                        (mx, my - 10), (mx + 5, my), (mx, my + 10), (mx - 5, my)
                    ])
                elif mat[2] == "metal":
                    # Metal = shiny gray (gives iron!)
                    pygame.draw.rect(window, (180, 180, 190), (mx - 10, my - 10, 20, 20))
                    pygame.draw.rect(window, (220, 220, 230), (mx - 7, my - 7, 8, 8))  # Shine
                elif mat[2] == "wood":
                    # Wood = brown log
                    pygame.draw.ellipse(window, (120, 70, 30), (mx - 15, my - 8, 30, 16))
                    pygame.draw.circle(window, (100, 60, 25), (mx - 12, my), 6)  # End
                    pygame.draw.circle(window, (80, 50, 20), (mx - 12, my), 3)  # Rings
                elif mat[2] == "stone":
                    # Stone = gray rock
                    pygame.draw.polygon(window, (140, 140, 150), [
                        (mx - 10, my + 8), (mx - 12, my - 5), (mx - 3, my - 12),
                        (mx + 8, my - 8), (mx + 12, my + 3), (mx + 5, my + 10)
                    ])
                else:  # rock
                    # Rock = brown circle (gives stone!)
                    pygame.draw.circle(window, (139, 90, 43), (mx, my), 12)
                    pygame.draw.circle(window, (160, 110, 60), (mx - 3, my - 3), 4)  # Highlight

            # Draw VILLAGERS on this planet!
            for v in villagers:
                if v[0] == current_planet_name:
                    vx, vy = int(v[1]), int(v[2])
                    job = v[3]
                    # Different colors for different jobs!
                    if job == "homeless":
                        body_color = (150, 150, 150)  # Gray
                    elif job == "farmer":
                        body_color = (100, 200, 100)  # Green
                    elif job == "miner":
                        body_color = (200, 150, 100)  # Brown
                    elif job == "soldier":
                        body_color = (200, 50, 50)  # Red
                    elif job == "banker":
                        body_color = (255, 215, 0)  # Gold
                    elif job == "shopkeeper":
                        body_color = (200, 100, 200)  # Purple
                    else:
                        body_color = (100, 150, 200)  # Blue

                    # Draw little person!
                    pygame.draw.circle(window, body_color, (vx, vy - 12), 8)  # Head
                    pygame.draw.line(window, body_color, (vx, vy - 4), (vx, vy + 8), 3)  # Body
                    pygame.draw.line(window, body_color, (vx - 6, vy + 2), (vx + 6, vy + 2), 2)  # Arms
                    pygame.draw.line(window, body_color, (vx, vy + 8), (vx - 5, vy + 16), 2)  # Leg
                    pygame.draw.line(window, body_color, (vx, vy + 8), (vx + 5, vy + 16), 2)  # Leg

            # Draw food to collect!
            for fd in planet_food:
                fx, fy = int(fd[0]), int(fd[1])
                if fd[2] == "apple":
                    # Apple = red circle with stem
                    pygame.draw.circle(window, (255, 50, 50), (fx, fy), 12)
                    pygame.draw.line(window, (100, 60, 20), (fx, fy - 12), (fx + 3, fy - 18), 3)
                elif fd[2] == "meat":
                    # Meat = brown oval
                    pygame.draw.ellipse(window, (180, 100, 80), (fx - 15, fy - 8, 30, 16))
                    pygame.draw.ellipse(window, (200, 120, 100), (fx - 12, fy - 5, 24, 10))
                else:  # berry
                    # Berry = small purple circles
                    pygame.draw.circle(window, (150, 50, 200), (fx - 5, fy), 6)
                    pygame.draw.circle(window, (150, 50, 200), (fx + 5, fy), 6)
                    pygame.draw.circle(window, (150, 50, 200), (fx, fy - 6), 6)

            # Draw the player (astronaut!)
            px, py = int(planet_explore_x), int(planet_explore_y)
            pygame.draw.circle(window, (0, 100, 200), (px, py), 20)  # Body
            pygame.draw.circle(window, (200, 200, 255), (px, py - 5), 12)  # Helmet
            pygame.draw.circle(window, (255, 0, 0), (px - 4, py - 5), 3)  # Red eye
            pygame.draw.circle(window, (255, 0, 0), (px + 4, py - 5), 3)  # Red eye

            # Draw UI
            planet_title = big_font.render(current_planet_name, True, (255, 255, 255))
            window.blit(planet_title, (20, 20))

            # Resources panel on right side
            res_x = SCREEN_WIDTH - 200
            res_y = 20
            pygame.draw.rect(window, (0, 0, 0, 128), (res_x - 10, res_y - 5, 195, 180))

            mat_text = font.render("Materials: " + str(materials), True, (200, 200, 100))
            window.blit(mat_text, (res_x, res_y))
            wood_text = font.render("Wood: " + str(wood), True, (180, 120, 60))
            window.blit(wood_text, (res_x, res_y + 25))
            stone_text = font.render("Stone: " + str(stone), True, (150, 150, 160))
            window.blit(stone_text, (res_x, res_y + 50))
            iron_text = font.render("Iron: " + str(iron), True, (200, 200, 210))
            window.blit(iron_text, (res_x, res_y + 75))
            gold_text = font.render("Gold: " + str(gold), True, (255, 215, 0))
            window.blit(gold_text, (res_x, res_y + 100))
            pop_text = font.render("Population: " + str(population), True, (100, 200, 255))
            window.blit(pop_text, (res_x, res_y + 125))
            army_text = font.render("Soldiers: " + str(soldiers), True, (255, 100, 100))
            window.blit(army_text, (res_x, res_y + 150))

            # Food bar on left
            food_label = font.render("Food:", True, (255, 255, 255))
            window.blit(food_label, (20, 80))
            pygame.draw.rect(window, (50, 50, 50), (100, 80, 150, 20))
            food_width = int((food / 100) * 146)
            food_color = (50, 200, 50) if food > 30 else (200, 50, 50)
            pygame.draw.rect(window, food_color, (102, 82, food_width, 16))

            # Refugees waiting?
            if refugees_waiting > 0:
                ref_text = font.render("Refugees waiting: " + str(refugees_waiting), True, (255, 255, 100))
                window.blit(ref_text, (20, 110))

            # Count villagers on this planet
            local_villagers = sum(1 for v in villagers if v[0] == current_planet_name)
            if local_villagers > 0:
                local_text = font.render("Villagers here: " + str(local_villagers), True, (150, 200, 255))
                window.blit(local_text, (20, 140))

            # Planet food supply (economy)
            if current_planet_name in planet_economy:
                planet_supply = int(planet_economy[current_planet_name]["food_supply"])
                supply_color = (100, 255, 100) if planet_supply > 50 else (255, 255, 100) if planet_supply > 20 else (255, 100, 100)
                supply_text = font.render("Planet Food: " + str(planet_supply) + "/200", True, supply_color)
                window.blit(supply_text, (20, 170))

                # Show production info
                farmers_here = sum(1 for v in villagers if v[0] == current_planet_name and v[3] == "farmer")
                farms_here = sum(1 for b in buildings if b[0] == current_planet_name and b[3] == "farm")
                if farmers_here > 0 or local_villagers > 0:
                    prod = min(farmers_here, farms_here * 3) * FOOD_PER_FARMER if farms_here > 0 else 0
                    consume = local_villagers * FOOD_PER_VILLAGER
                    net = prod - consume
                    net_color = (100, 255, 100) if net > 0 else (255, 100, 100) if net < 0 else (200, 200, 200)
                    net_text = font.render("Food/sec: " + ("+" if net > 0 else "") + str(round(net, 1)), True, net_color)
                    window.blit(net_text, (20, 195))

            # Building controls at bottom
            controls1 = font.render("ARROWS = Move   V = Return   ENTER = Enter Building   TAB = Menu", True, (200, 200, 200))
            window.blit(controls1, (20, SCREEN_HEIGHT - 90))
            controls2 = font.render("BUILDINGS: B=Base T=Turret F=Farm K=Bank R=Factory Q=House P=Port E=Market X=Barracks", True, (200, 200, 200))
            window.blit(controls2, (20, SCREEN_HEIGHT - 60))
            controls3 = font.render("JOBS: 1=Farmer 2=Miner 3=Soldier 4=Banker 5=Shopkeeper 6=Builder", True, (255, 200, 100))
            window.blit(controls3, (20, SCREEN_HEIGHT - 30))

            # --- BUILDING MENU OVERLAY! ---
            if building_menu_open:
                # Dark overlay
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.fill((0, 0, 0))
                overlay.set_alpha(200)
                window.blit(overlay, (0, 0))

                # Menu box
                menu_width = 900
                menu_height = 650
                menu_x = (SCREEN_WIDTH - menu_width) // 2
                menu_y = (SCREEN_HEIGHT - menu_height) // 2

                pygame.draw.rect(window, (30, 30, 50), (menu_x, menu_y, menu_width, menu_height))
                pygame.draw.rect(window, (100, 150, 255), (menu_x, menu_y, menu_width, menu_height), 3)

                # Title
                menu_title = big_font.render("BUILDING GUIDE", True, (255, 215, 0))
                title_rect = menu_title.get_rect(center=(SCREEN_WIDTH // 2, menu_y + 40))
                window.blit(menu_title, title_rect)

                # Building data - [key, name, cost, extra_cost, requirement, description]
                all_buildings = [
                    ["B", "BASE", str(BASE_COST) + " mat", "", "None", "Command center! Unlocks advanced buildings."],
                    ["T", "TURRET", str(TURRET_COST) + " mat", "", "1 free, 3 with Base", "Auto-shoots enemies during battle!"],
                    ["F", "FARM", str(FARM_COST) + " mat", "", "Base required", "Generates food over time. Needs farmers!"],
                    ["K", "BANK", str(BANK_COST) + " mat", "", "Base required", "Generates coins over time. Needs bankers!"],
                    ["R", "ROBOT FACTORY", str(FACTORY_COST) + " mat", "", "Base required", "Spawns helper robots in battle!"],
                    ["G", "SHIELD GEN", str(SHIELD_GEN_COST) + " mat", "", "Base required", "Gives you a shield when you land!"],
                    ["M", "AUTO MINER", str(MINER_COST) + " mat", "", "Base required", "Auto-collects materials. Needs miners!"],
                    ["H", "HOSPITAL", str(HOSPITAL_COST) + " mat", "", "Base required", "Gives extra life when you land!"],
                    ["D", "RADAR", str(RADAR_COST) + " mat", "", "Base required", "Shows enemy direction warnings!"],
                    ["Y", "SHIPYARD", str(SHIPYARD_COST) + " mat", "", "Base required", "Upgrades ship damage/speed/fire rate!"],
                    ["Q", "HOUSE", str(HOUSE_COST) + " mat", str(HOUSE_WOOD) + " wood", "None", "Homes for 4 villagers. Build for refugees!"],
                    ["P", "SPACE PORT", str(SPACEPORT_COST) + " mat", str(SPACEPORT_IRON) + " iron", "Base required", "Dock your fleet ships here!"],
                    ["E", "MARKET", str(MARKET_COST) + " mat", str(MARKET_WOOD) + " wood", "None", "Trade goods for coins! Needs shopkeepers!"],
                    ["X", "BARRACKS", str(BARRACKS_COST) + " mat", str(BARRACKS_IRON) + " iron", "Base required", "Train villagers into soldiers!"],
                    ["C", "TAVERN", str(TAVERN_COST) + " mat", str(TAVERN_WOOD) + " wood", "None", "Makes villagers happy!"],
                    ["Z", "WAREHOUSE", str(WAREHOUSE_COST) + " mat", str(WAREHOUSE_WOOD) + " wood", "None", "Stores extra materials!"],
                ]

                # Job assignments section
                job_data = [
                    ["1", "FARMER", "Works at Farm", "Grows food faster!"],
                    ["2", "MINER", "Works at Auto Miner", "Collects materials faster!"],
                    ["3", "SOLDIER", "Needs Barracks", "Fights in your army!"],
                    ["4", "BANKER", "Works at Bank", "Generates more coins!"],
                    ["5", "SHOPKEEPER", "Works at Market", "Trades for better prices!"],
                    ["6", "BUILDER", "No building needed", "Builds things faster!"],
                ]

                # Draw buildings (with scroll)
                visible_buildings = 8
                start_y = menu_y + 80
                row_height = 65

                for i in range(visible_buildings):
                    idx = i + building_menu_scroll
                    if idx >= len(all_buildings):
                        break

                    b = all_buildings[idx]
                    row_y = start_y + i * row_height

                    # Alternating row colors
                    row_color = (40, 40, 60) if i % 2 == 0 else (35, 35, 55)
                    pygame.draw.rect(window, row_color, (menu_x + 10, row_y, menu_width - 20, row_height - 5))

                    # Key
                    key_text = medium_font.render("[" + b[0] + "]", True, (255, 200, 100))
                    window.blit(key_text, (menu_x + 20, row_y + 5))

                    # Name
                    name_text = medium_font.render(b[1], True, (255, 255, 255))
                    window.blit(name_text, (menu_x + 80, row_y + 5))

                    # Cost
                    cost_text = font.render(b[2], True, (200, 200, 100))
                    window.blit(cost_text, (menu_x + 280, row_y + 8))

                    # Extra cost (if any)
                    if b[3]:
                        extra_text = font.render("+ " + b[3], True, (200, 150, 100))
                        window.blit(extra_text, (menu_x + 380, row_y + 8))

                    # Requirement
                    req_color = (100, 255, 100) if b[4] == "None" else (255, 200, 100)
                    req_text = font.render(b[4], True, req_color)
                    window.blit(req_text, (menu_x + 500, row_y + 8))

                    # Description
                    desc_text = font.render(b[5], True, (180, 180, 180))
                    window.blit(desc_text, (menu_x + 20, row_y + 35))

                # Scroll indicator
                if building_menu_scroll > 0:
                    up_arrow = medium_font.render("^ MORE ABOVE ^", True, (150, 150, 200))
                    up_rect = up_arrow.get_rect(center=(SCREEN_WIDTH // 2, menu_y + 70))
                    window.blit(up_arrow, up_rect)

                if building_menu_scroll + visible_buildings < len(all_buildings):
                    down_arrow = medium_font.render("v MORE BELOW v", True, (150, 150, 200))
                    down_rect = down_arrow.get_rect(center=(SCREEN_WIDTH // 2, menu_y + menu_height - 70))
                    window.blit(down_arrow, down_rect)

                # Instructions
                instr_text = font.render("UP/DOWN = Scroll   TAB/ESC = Close", True, (150, 150, 150))
                instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH // 2, menu_y + menu_height - 30))
                window.blit(instr_text, instr_rect)

                # Column headers
                pygame.draw.line(window, (80, 80, 100), (menu_x + 10, start_y - 5), (menu_x + menu_width - 10, start_y - 5), 2)
                header_y = start_y - 25
                h1 = font.render("KEY", True, (150, 150, 200))
                window.blit(h1, (menu_x + 20, header_y))
                h2 = font.render("BUILDING", True, (150, 150, 200))
                window.blit(h2, (menu_x + 80, header_y))
                h3 = font.render("COST", True, (150, 150, 200))
                window.blit(h3, (menu_x + 280, header_y))
                h4 = font.render("EXTRA", True, (150, 150, 200))
                window.blit(h4, (menu_x + 380, header_y))
                h5 = font.render("REQUIRES", True, (150, 150, 200))
                window.blit(h5, (menu_x + 500, header_y))

        # --- DRAW BUILDING INTERIOR! ---
        if game_state == "inside_building" and inside_building:
            building_type = inside_building[3]

            # Background color based on building type
            if building_type == "farm":
                window.fill((60, 80, 40))  # Earthy green
            elif building_type == "bank":
                window.fill((50, 40, 30))  # Rich wood brown
            elif building_type == "market":
                window.fill((70, 50, 40))  # Market brown
            elif building_type == "barracks":
                window.fill((40, 40, 50))  # Military gray
            elif building_type == "house":
                window.fill((60, 50, 45))  # Cozy interior
            elif building_type == "tavern":
                window.fill((50, 35, 25))  # Warm tavern
            elif building_type == "warehouse":
                window.fill((45, 45, 50))  # Storage gray
            elif building_type == "hospital":
                window.fill((60, 70, 80))  # Clean blue
            else:
                window.fill((40, 40, 40))

            # Building title
            title_text = big_font.render(building_type.upper(), True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            window.blit(title_text, title_rect)

            # Different interiors for different buildings!
            if building_type == "farm":
                # --- FARM INTERIOR ---
                # Draw crop plots
                pygame.draw.rect(window, (80, 60, 30), (100, 150, 200, 150))  # Plot 1
                pygame.draw.rect(window, (80, 60, 30), (350, 150, 200, 150))  # Plot 2
                pygame.draw.rect(window, (80, 60, 30), (600, 150, 200, 150))  # Plot 3

                # Draw some crops
                for px in [150, 200, 250]:
                    for py in [180, 220, 260]:
                        pygame.draw.line(window, (50, 150, 50), (px, py), (px, py - 20), 3)
                        pygame.draw.circle(window, (100, 200, 50), (px, py - 25), 8)

                for px in [400, 450, 500]:
                    for py in [180, 220, 260]:
                        pygame.draw.line(window, (50, 150, 50), (px, py), (px, py - 15), 3)

                # Menu options
                farm_options = ["[1] Plant Crops (10 coins)", "[2] Harvest All (get food)", "[3] Water Crops (+growth)", "[ESC] Leave Farm"]
                for i, opt in enumerate(farm_options):
                    color = (255, 255, 100) if i == inside_menu_selection else (200, 200, 200)
                    opt_text = medium_font.render(opt, True, color)
                    window.blit(opt_text, (100, 350 + i * 40))

                # Show current food
                food_text = font.render("Food: " + str(food), True, (100, 255, 100))
                window.blit(food_text, (650, 350))

            elif building_type == "bank":
                # --- BANK INTERIOR ---
                # Draw vault
                pygame.draw.rect(window, (80, 80, 90), (SCREEN_WIDTH//2 - 100, 120, 200, 180))
                pygame.draw.circle(window, (150, 150, 160), (SCREEN_WIDTH//2, 210), 40)
                pygame.draw.circle(window, (100, 100, 110), (SCREEN_WIDTH//2, 210), 30)

                # Draw counter
                pygame.draw.rect(window, (120, 80, 40), (100, 350, SCREEN_WIDTH - 200, 40))

                # Draw gold coins
                for i in range(min(gold, 10)):
                    pygame.draw.circle(window, (255, 215, 0), (150 + i * 30, 340), 12)

                # Bank balance display
                balance_text = big_font.render("Bank Balance: " + str(bank_balance), True, (255, 215, 0))
                balance_rect = balance_text.get_rect(center=(SCREEN_WIDTH // 2, 320))
                window.blit(balance_text, balance_rect)

                # Menu options
                bank_options = ["[1] Deposit 100 Coins", "[2] Withdraw 100 Coins", "[3] Collect Interest", "[ESC] Leave Bank"]
                for i, opt in enumerate(bank_options):
                    color = (255, 255, 100) if i == inside_menu_selection else (200, 200, 200)
                    opt_text = medium_font.render(opt, True, color)
                    window.blit(opt_text, (100, 420 + i * 40))

                # Show coins
                coins_text = font.render("Your Coins: " + str(coins), True, (255, 215, 0))
                window.blit(coins_text, (650, 420))

            elif building_type == "market":
                # --- MARKET INTERIOR ---
                # Draw stall
                pygame.draw.rect(window, (140, 100, 60), (100, 180, SCREEN_WIDTH - 200, 80))
                pygame.draw.rect(window, (200, 80, 80), (100, 140, SCREEN_WIDTH - 200, 40))

                # Draw goods on counter
                pygame.draw.rect(window, (139, 90, 43), (150, 190, 40, 30))  # Wood
                pygame.draw.circle(window, (128, 128, 140), (250, 210), 15)  # Stone
                pygame.draw.rect(window, (180, 180, 195), (320, 195, 35, 25))  # Iron
                pygame.draw.circle(window, (255, 215, 0), (430, 205), 12)  # Gold

                # Prices display
                price_title = medium_font.render("PRICES:", True, (255, 255, 255))
                window.blit(price_title, (100, 280))

                price_y = 320
                items = [("Wood", wood, market_prices["wood"]), ("Stone", stone, market_prices["stone"]),
                        ("Iron", iron, market_prices["iron"]), ("Gold", gold, market_prices["gold"])]
                for item_name, amount, price in items:
                    item_text = font.render(item_name + ": " + str(amount) + " (sell for " + str(price) + " coins each)", True, (200, 200, 200))
                    window.blit(item_text, (120, price_y))
                    price_y += 25

                # Menu options
                market_options = ["[1] Sell 10 Wood", "[2] Sell 10 Stone", "[3] Sell 5 Iron", "[4] Sell 1 Gold", "[ESC] Leave Market"]
                for i, opt in enumerate(market_options):
                    color = (255, 255, 100) if i == inside_menu_selection else (200, 200, 200)
                    opt_text = medium_font.render(opt, True, color)
                    window.blit(opt_text, (100, 440 + i * 35))

                # Show coins
                coins_text = font.render("Your Coins: " + str(coins), True, (255, 215, 0))
                window.blit(coins_text, (650, 280))

            elif building_type == "barracks":
                # --- BARRACKS INTERIOR ---
                # Draw training area
                pygame.draw.rect(window, (60, 50, 40), (100, 150, SCREEN_WIDTH - 200, 200))

                # Draw weapon rack
                for i in range(5):
                    pygame.draw.line(window, (150, 150, 160), (150 + i * 80, 180), (150 + i * 80, 280), 5)
                    pygame.draw.polygon(window, (200, 200, 210), [
                        (150 + i * 80, 160), (140 + i * 80, 180), (160 + i * 80, 180)
                    ])

                # Draw some soldier silhouettes
                for i in range(min(soldiers, 5)):
                    sx = 550 + i * 40
                    pygame.draw.circle(window, (100, 80, 60), (sx, 200), 15)
                    pygame.draw.rect(window, (100, 80, 60), (sx - 12, 215, 24, 40))

                # Stats
                stats_text = medium_font.render("Army: " + str(soldiers) + " soldiers   Power: " + str(army_power), True, (255, 100, 100))
                window.blit(stats_text, (100, 370))

                # Menu options
                barracks_options = ["[1] Train Soldier (1 villager + 50 iron)", "[2] Upgrade Army Power (100 coins)", "[3] Deploy to Defense", "[ESC] Leave Barracks"]
                for i, opt in enumerate(barracks_options):
                    color = (255, 255, 100) if i == inside_menu_selection else (200, 200, 200)
                    opt_text = medium_font.render(opt, True, color)
                    window.blit(opt_text, (100, 420 + i * 40))

            elif building_type == "house":
                # --- HOUSE INTERIOR ---
                # Draw interior
                pygame.draw.rect(window, (120, 90, 60), (50, 120, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200))

                # Draw furniture
                pygame.draw.rect(window, (80, 60, 40), (100, 200, 120, 60))  # Table
                pygame.draw.rect(window, (100, 70, 45), (300, 180, 80, 100))  # Bed
                pygame.draw.rect(window, (140, 100, 60), (500, 200, 60, 80))  # Chair

                # Draw fireplace
                pygame.draw.rect(window, (60, 60, 70), (650, 160, 100, 120))
                pygame.draw.polygon(window, (255, 100, 0), [(675, 250), (700, 200), (725, 250)])

                # Count villagers living here
                house_villagers = sum(1 for v in villagers if v[0] == inside_building[0])
                house_text = medium_font.render("Villagers on planet: " + str(house_villagers), True, (200, 200, 255))
                window.blit(house_text, (100, 350))

                # Menu options
                house_options = ["[1] Rest (restore health)", "[2] Check Happiness", "[ESC] Leave House"]
                for i, opt in enumerate(house_options):
                    color = (255, 255, 100) if i == inside_menu_selection else (200, 200, 200)
                    opt_text = medium_font.render(opt, True, color)
                    window.blit(opt_text, (100, 420 + i * 40))

            elif building_type == "tavern":
                # --- TAVERN INTERIOR ---
                # Draw bar
                pygame.draw.rect(window, (100, 60, 30), (100, 300, SCREEN_WIDTH - 200, 50))

                # Draw tables
                for tx in [150, 350, 550]:
                    pygame.draw.circle(window, (90, 55, 25), (tx, 200), 40)

                # Draw mugs on bar
                for i in range(6):
                    pygame.draw.rect(window, (180, 140, 80), (150 + i * 100, 280, 25, 30))

                # Atmosphere
                atmo_text = medium_font.render("The tavern is warm and cheerful!", True, (255, 200, 100))
                window.blit(atmo_text, (100, 380))

                # Menu options
                tavern_options = ["[1] Buy Drink (5 coins, +happiness)", "[2] Listen to Stories", "[3] Recruit Adventurer", "[ESC] Leave Tavern"]
                for i, opt in enumerate(tavern_options):
                    color = (255, 255, 100) if i == inside_menu_selection else (200, 200, 200)
                    opt_text = medium_font.render(opt, True, color)
                    window.blit(opt_text, (100, 440 + i * 40))

            elif building_type == "warehouse":
                # --- WAREHOUSE INTERIOR ---
                # Draw shelves
                for sy in [150, 250, 350]:
                    pygame.draw.rect(window, (100, 80, 50), (100, sy, SCREEN_WIDTH - 200, 30))

                # Draw crates
                for cx in [120, 220, 320, 420, 520, 620]:
                    pygame.draw.rect(window, (140, 100, 60), (cx, 180, 50, 50))
                    pygame.draw.rect(window, (140, 100, 60), (cx, 280, 50, 50))

                # Show storage
                storage_text = medium_font.render("STORAGE:", True, (255, 255, 255))
                window.blit(storage_text, (100, 420))

                storage_info = "Materials: " + str(materials) + "  Wood: " + str(wood) + "  Stone: " + str(stone) + "  Iron: " + str(iron) + "  Gold: " + str(gold)
                info_text = font.render(storage_info, True, (200, 200, 200))
                window.blit(info_text, (100, 460))

                # Menu options
                warehouse_options = ["[1] Organize Storage (+capacity)", "[2] Check Inventory", "[ESC] Leave Warehouse"]
                for i, opt in enumerate(warehouse_options):
                    color = (255, 255, 100) if i == inside_menu_selection else (200, 200, 200)
                    opt_text = medium_font.render(opt, True, color)
                    window.blit(opt_text, (100, 520 + i * 40))

            elif building_type == "hospital":
                # --- HOSPITAL INTERIOR ---
                # Draw beds
                for bx in [100, 300, 500]:
                    pygame.draw.rect(window, (220, 220, 230), (bx, 180, 150, 80))
                    pygame.draw.rect(window, (180, 200, 220), (bx, 180, 150, 30))

                # Draw medicine cabinet
                pygame.draw.rect(window, (200, 200, 210), (700, 150, 80, 120))
                pygame.draw.line(window, (150, 150, 160), (740, 160), (740, 260), 2)
                pygame.draw.line(window, (150, 150, 160), (700, 210), (780, 210), 2)

                # Red cross
                pygame.draw.rect(window, (255, 50, 50), (725, 280, 30, 60))
                pygame.draw.rect(window, (255, 50, 50), (710, 295, 60, 30))

                # Menu options
                hospital_options = ["[1] Heal Villagers (50 coins)", "[2] Train Medic", "[ESC] Leave Hospital"]
                for i, opt in enumerate(hospital_options):
                    color = (255, 255, 100) if i == inside_menu_selection else (200, 200, 200)
                    opt_text = medium_font.render(opt, True, color)
                    window.blit(opt_text, (100, 420 + i * 40))

            # Controls hint at bottom
            controls_text = font.render("UP/DOWN = Select   ENTER = Choose   ESC = Leave", True, (150, 150, 150))
            window.blit(controls_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT - 40))

        # --- DRAW SIGN IN SCREEN! ---
        if game_state == "signin":
            window.fill((20, 20, 50))  # Dark blue background

            # Title
            signin_title = big_font.render("WELCOME!", True, (255, 255, 100))
            title_rect = signin_title.get_rect(center=(SCREEN_WIDTH // 2, 150))
            window.blit(signin_title, title_rect)

            # Instructions
            instr = medium_font.render("Enter your name:", True, (255, 255, 255))
            instr_rect = instr.get_rect(center=(SCREEN_WIDTH // 2, 300))
            window.blit(instr, instr_rect)

            # Username input box
            box_width = 400
            box_x = SCREEN_WIDTH // 2 - box_width // 2
            pygame.draw.rect(window, (50, 50, 80), (box_x, 350, box_width, 60))
            pygame.draw.rect(window, (255, 255, 255), (box_x, 350, box_width, 60), 3)

            # Show what they're typing
            name_text = big_font.render(username_input + "_", True, (255, 255, 255))
            name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, 380))
            window.blit(name_text, name_rect)

            # Hints
            hint1 = font.render("Press ENTER when done", True, (150, 150, 150))
            window.blit(hint1, (SCREEN_WIDTH // 2 - 100, 450))
            hint2 = font.render("Press TAB to see leaderboard", True, (150, 150, 150))
            window.blit(hint2, (SCREEN_WIDTH // 2 - 130, 480))

        # --- DRAW LEADERBOARD! ---
        if game_state == "leaderboard":
            window.fill((20, 20, 50))  # Dark blue background

            # Title
            lb_title = big_font.render("LEADERBOARD", True, (255, 215, 0))
            title_rect = lb_title.get_rect(center=(SCREEN_WIDTH // 2, 80))
            window.blit(lb_title, title_rect)

            # Show top scores
            leaderboard = load_leaderboard()
            if len(leaderboard) == 0:
                no_scores = medium_font.render("No high scores yet!", True, (150, 150, 150))
                ns_rect = no_scores.get_rect(center=(SCREEN_WIDTH // 2, 300))
                window.blit(no_scores, ns_rect)
            else:
                for i, entry in enumerate(leaderboard[:10]):
                    # Rank
                    rank_color = (255, 215, 0) if i == 0 else (200, 200, 200) if i == 1 else (180, 100, 50) if i == 2 else (255, 255, 255)
                    rank_text = medium_font.render(str(i + 1) + ".", True, rank_color)
                    window.blit(rank_text, (300, 150 + i * 50))
                    # Name
                    name_text = medium_font.render(entry["name"], True, (255, 255, 255))
                    window.blit(name_text, (380, 150 + i * 50))
                    # Score
                    score_text = medium_font.render(str(entry["score"]), True, (100, 255, 100))
                    window.blit(score_text, (700, 150 + i * 50))

            # Back hint
            back_hint = font.render("Press ENTER to go back", True, (150, 150, 150))
            bh_rect = back_hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            window.blit(back_hint, bh_rect)

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

        # --- DRAW THE LOBBY! ---
        # The hub between levels where you choose what to do!
        if game_state == "lobby":
            # Cool space gradient background!
            for y in range(SCREEN_HEIGHT):
                blue = int(10 + (y / SCREEN_HEIGHT) * 30)
                pygame.draw.line(window, (0, blue // 2, blue), (0, y), (SCREEN_WIDTH, y))

            # Draw some stars!
            for i in range(50):
                sx = (i * 127 + title_timer // 10) % SCREEN_WIDTH
                sy = (i * 89) % SCREEN_HEIGHT
                brightness = 100 + int(50 * math.sin(title_timer / 500 + i))
                pygame.draw.circle(window, (brightness, brightness, brightness + 50), (int(sx), int(sy)), 2)

            # Title based on what happened!
            if lobby_reason == "level":
                title_text = "LEVEL " + str(level) + " COMPLETE!"
                title_color = (100, 255, 100)  # Green for victory!
            else:
                title_text = "GAME OVER"
                title_color = (255, 100, 100)  # Red for death!

            lobby_title = big_font.render(title_text, True, title_color)
            lobby_title_rect = lobby_title.get_rect(center=(SCREEN_WIDTH // 2, 100))
            window.blit(lobby_title, lobby_title_rect)

            # Show stats!
            stats_y = 180
            coins_text = medium_font.render("COINS: " + str(coins), True, (255, 215, 0))
            coins_rect = coins_text.get_rect(center=(SCREEN_WIDTH // 2, stats_y))
            window.blit(coins_text, coins_rect)

            level_text = font.render("Level: " + str(level) + "  |  Materials: " + str(materials) + "  |  Food: " + str(food), True, (200, 200, 200))
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, stats_y + 40))
            window.blit(level_text, level_rect)

            # Menu options!
            # Change quit text if confirmation is needed
            quit_text = "QUIT TO TITLE"
            quit_desc = "Return to title screen"
            quit_color = (150, 150, 150)
            if quit_confirm and lobby_selection == 3:
                quit_text = "ARE YOU SURE?"
                quit_desc = "Press ENTER again to quit, or move away to cancel"
                quit_color = (255, 100, 100)

            lobby_options = [
                {"name": "SHOP", "desc": "Buy power-ups and upgrades!", "color": (255, 215, 0)},
                {"name": "CONTINUE", "desc": "Go back to space exploration!", "color": (100, 200, 255)},
                {"name": "LEADERBOARD", "desc": "View high scores!", "color": (255, 100, 255)},
                {"name": quit_text, "desc": quit_desc, "color": quit_color},
            ]

            menu_y = 300
            for i in range(len(lobby_options)):
                opt = lobby_options[i]
                y_pos = menu_y + i * 80

                # Is this option selected?
                if i == lobby_selection:
                    # Glowing box around selected option!
                    box_width = 500
                    box_x = (SCREEN_WIDTH - box_width) // 2
                    pygame.draw.rect(window, opt["color"], (box_x, y_pos - 10, box_width, 60), 3)

                    # Bouncy arrow!
                    arrow_x = box_x - 40 + int(math.sin(title_timer / 200) * 10)
                    arrow = medium_font.render(">", True, opt["color"])
                    window.blit(arrow, (arrow_x, y_pos + 5))

                    text_color = opt["color"]
                else:
                    text_color = (100, 100, 100)

                # Option name
                name_text = medium_font.render(opt["name"], True, text_color)
                name_rect = name_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 10))
                window.blit(name_text, name_rect)

                # Description (only for selected)
                if i == lobby_selection:
                    desc_text = font.render(opt["desc"], True, (150, 150, 150))
                    desc_rect = desc_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 35))
                    window.blit(desc_text, desc_rect)

            # Instructions at the bottom!
            instr_text = font.render("UP/DOWN = Select    ENTER = Choose", True, (150, 150, 150))
            instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH // 2, 700))
            window.blit(instr_text, instr_rect)

            # Update animation timer (reusing title_timer)
            title_timer = title_timer + delta_ms

        # --- DRAW THE SKIN SHOP! ---
        if game_state == "skin_shop":
            # Purple gradient background
            for y in range(SCREEN_HEIGHT):
                purple = int(20 + (y / SCREEN_HEIGHT) * 40)
                pygame.draw.line(window, (purple, 0, purple * 2), (0, y), (SCREEN_WIDTH, y))

            # Title
            skin_title = big_font.render("SKIN SHOP", True, (255, 100, 255))
            skin_title_rect = skin_title.get_rect(center=(SCREEN_WIDTH // 2, 50))
            window.blit(skin_title, skin_title_rect)

            # Coins display
            coins_text = medium_font.render("COINS: " + str(coins), True, (255, 215, 0))
            window.blit(coins_text, (20, 20))

            # Current skin equipped
            equip_text = font.render("Equipped: " + current_skin.upper(), True, (100, 255, 100))
            window.blit(equip_text, (SCREEN_WIDTH - 250, 20))

            # Draw skin cards in a row
            card_width = 140
            card_height = 200
            start_x = (SCREEN_WIDTH - (card_width * 4 + 30 * 3)) // 2  # Center 4 cards
            cards_per_row = 4

            for i, skin in enumerate(all_skins):
                row = i // cards_per_row
                col = i % cards_per_row
                card_x = start_x + col * (card_width + 30)
                card_y = 120 + row * (card_height + 20)

                # Card background
                is_selected = (i == skin_shop_selection)
                is_owned = skin["name"] in owned_skins
                is_equipped = skin["name"] == current_skin

                if is_selected:
                    # Glowing border for selected
                    pygame.draw.rect(window, (255, 255, 0), (card_x - 4, card_y - 4, card_width + 8, card_height + 8), 4)

                # Card body
                card_color = (60, 60, 80) if not is_selected else (80, 80, 100)
                pygame.draw.rect(window, card_color, (card_x, card_y, card_width, card_height))
                pygame.draw.rect(window, skin["colors"]["body"], (card_x, card_y, card_width, 5))

                # Draw skin preview (ship shape with skin colors)
                preview_x = card_x + card_width // 2
                preview_y = card_y + 70
                body_color = skin["colors"]["body"]
                accent_color = skin["colors"]["accent"]

                # Ship body
                pygame.draw.polygon(window, body_color, [
                    (preview_x, preview_y - 30),
                    (preview_x - 25, preview_y + 20),
                    (preview_x + 25, preview_y + 20)
                ])
                # Cockpit
                pygame.draw.ellipse(window, accent_color, (preview_x - 10, preview_y - 15, 20, 25))
                # Wings
                pygame.draw.polygon(window, accent_color, [
                    (preview_x - 20, preview_y + 10),
                    (preview_x - 40, preview_y + 25),
                    (preview_x - 15, preview_y + 20)
                ])
                pygame.draw.polygon(window, accent_color, [
                    (preview_x + 20, preview_y + 10),
                    (preview_x + 40, preview_y + 25),
                    (preview_x + 15, preview_y + 20)
                ])
                # Engine glow
                pygame.draw.circle(window, (255, 200, 100), (preview_x, preview_y + 25), 8)
                pygame.draw.circle(window, (255, 255, 200), (preview_x, preview_y + 25), 4)

                # Skin name
                name_text = font.render(skin["display"], True, (255, 255, 255))
                name_rect = name_text.get_rect(center=(card_x + card_width // 2, card_y + 130))
                window.blit(name_text, name_rect)

                # Description
                desc_text = font.render(skin["desc"], True, (150, 150, 150))
                desc_rect = desc_text.get_rect(center=(card_x + card_width // 2, card_y + 150))
                window.blit(desc_text, desc_rect)

                # Price or status
                if is_equipped:
                    status_text = font.render("EQUIPPED", True, (100, 255, 100))
                elif is_owned:
                    status_text = font.render("OWNED", True, (100, 200, 255))
                else:
                    status_text = font.render(str(skin["price"]) + " coins", True, (255, 215, 0))
                status_rect = status_text.get_rect(center=(card_x + card_width // 2, card_y + 180))
                window.blit(status_text, status_rect)

            # Instructions
            instr_text = font.render("LEFT/RIGHT = Browse    ENTER = Buy/Equip    D = Draw Custom    ESC = Back", True, (200, 200, 200))
            instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            window.blit(instr_text, instr_rect)

        # --- DRAW SKIN EDITOR! ---
        if game_state == "skin_editor":
            # Dark background
            window.fill((30, 20, 40))

            # Title
            title = big_font.render("DRAW YOUR SKIN!", True, (255, 200, 0))
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
            window.blit(title, title_rect)

            # Drawing canvas (32x32 pixels, scaled to 256x256)
            canvas_x = SCREEN_WIDTH // 2 - 128
            canvas_y = SCREEN_HEIGHT // 2 - 128

            # Draw canvas background (white)
            pygame.draw.rect(window, (255, 255, 255), (canvas_x, canvas_y, 256, 256))

            # Draw grid lines
            for i in range(33):
                pygame.draw.line(window, (200, 200, 200), (canvas_x + i * 8, canvas_y), (canvas_x + i * 8, canvas_y + 256), 1)
                pygame.draw.line(window, (200, 200, 200), (canvas_x, canvas_y + i * 8), (canvas_x + 256, canvas_y + i * 8), 1)

            # Draw all the pixels!
            for pixel in custom_skin_pixels:
                px = canvas_x + pixel[0] * 8
                py = canvas_y + pixel[1] * 8
                pygame.draw.rect(window, pixel[2], (px, py, 8, 8))

            # Canvas border
            pygame.draw.rect(window, (100, 100, 100), (canvas_x - 2, canvas_y - 2, 260, 260), 4)

            # Color palette on the side
            palette_x = canvas_x + 280
            palette_y = canvas_y
            palette_label = font.render("COLORS:", True, (255, 255, 255))
            window.blit(palette_label, (palette_x, palette_y - 30))

            for i, color in enumerate(drawing_colors):
                cy = palette_y + i * 22
                pygame.draw.rect(window, color, (palette_x, cy, 30, 20))
                pygame.draw.rect(window, (150, 150, 150), (palette_x, cy, 30, 20), 2)
                # Highlight selected color
                if i == drawing_color_index:
                    pygame.draw.rect(window, (255, 255, 0), (palette_x - 3, cy - 3, 36, 26), 3)

            # Current color preview
            preview_label = font.render("Current:", True, (255, 255, 255))
            window.blit(preview_label, (palette_x, palette_y + 280))
            pygame.draw.rect(window, drawing_color, (palette_x, palette_y + 305, 60, 30))
            pygame.draw.rect(window, (255, 255, 255), (palette_x, palette_y + 305, 60, 30), 2)

            # Preview of character on the left
            preview_x = canvas_x - 150
            preview_y = canvas_y + 128
            preview_label = font.render("PREVIEW:", True, (255, 255, 255))
            window.blit(preview_label, (preview_x - 30, preview_y - 80))

            # Draw character preview
            if len(custom_skin_pixels) > 0:
                for pixel in custom_skin_pixels:
                    px = preview_x + pixel[0] * 2 - 32
                    py = preview_y + pixel[1] * 2 - 32
                    pygame.draw.rect(window, pixel[2], (px, py, 2, 2))
            else:
                # Show default rainbow person
                pygame.draw.ellipse(window, (255, 100, 100), (preview_x - 12, preview_y - 6, 24, 20))
                pygame.draw.circle(window, (255, 200, 100), (preview_x, preview_y - 18), 12)

            # Instructions
            instr1 = font.render("Click and drag to draw!", True, (200, 200, 200))
            instr2 = font.render("LEFT/RIGHT = Change color", True, (200, 200, 200))
            instr3 = font.render("C = Clear    S = Save & Equip", True, (200, 200, 200))
            instr4 = font.render("ESC = Back to Skin Shop", True, (200, 200, 200))
            window.blit(instr1, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100))
            window.blit(instr2, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 75))
            window.blit(instr3, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 50))
            window.blit(instr4, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 25))

            # Cost info
            if "custom" in owned_skins:
                cost_text = font.render("Custom skin OWNED!", True, (0, 255, 0))
            else:
                cost_text = font.render("Cost: 100 coins (You have: " + str(coins) + ")", True, (255, 200, 0))
            window.blit(cost_text, (SCREEN_WIDTH // 2 - 100, 90))

        # --- DRAW STORY ENDING! ---
        # Epic story ending when you beat level 2000!
        if game_state == "story_ending":
            # Dark space background
            window.fill((5, 5, 20))

            # Draw stars in background
            for i in range(100):
                sx = (i * 137 + story_ending_timer // 50) % SCREEN_WIDTH
                sy = (i * 89) % SCREEN_HEIGHT
                pygame.draw.circle(window, (255, 255, 255), (sx, sy), 1)

            # Different pages of the story!
            if story_page == 0:
                # PAGE 1: Victory!
                title = big_font.render("YOU DID IT!", True, (255, 215, 0))
                title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
                window.blit(title, title_rect)

                text1 = medium_font.render("After 2000 levels of battle...", True, (255, 255, 255))
                text2 = medium_font.render("You have defeated every enemy!", True, (255, 255, 255))
                text3 = medium_font.render("The Zeldas have been vanquished!", True, (100, 255, 100))
                window.blit(text1, text1.get_rect(center=(SCREEN_WIDTH // 2, 250)))
                window.blit(text2, text2.get_rect(center=(SCREEN_WIDTH // 2, 300)))
                window.blit(text3, text3.get_rect(center=(SCREEN_WIDTH // 2, 350)))

                # Draw hero celebrating!
                pygame.draw.circle(window, (70, 130, 180), (SCREEN_WIDTH // 2, 500), 40)
                pygame.draw.ellipse(window, (255, 0, 0), (SCREEN_WIDTH // 2 - 10, 490, 8, 5))
                pygame.draw.ellipse(window, (255, 0, 0), (SCREEN_WIDTH // 2 + 2, 490, 8, 5))

            elif story_page == 1:
                # PAGE 2: The Journey
                title = big_font.render("THE JOURNEY", True, (100, 200, 255))
                title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
                window.blit(title, title_rect)

                text1 = medium_font.render("From Earth, you explored the galaxy.", True, (255, 255, 255))
                text2 = medium_font.render("You discovered planets, built bases,", True, (255, 255, 255))
                text3 = medium_font.render("and made robot friends!", True, (255, 200, 100))
                text4 = medium_font.render("Total Score: " + str(score), True, (255, 215, 0))
                window.blit(text1, text1.get_rect(center=(SCREEN_WIDTH // 2, 250)))
                window.blit(text2, text2.get_rect(center=(SCREEN_WIDTH // 2, 300)))
                window.blit(text3, text3.get_rect(center=(SCREEN_WIDTH // 2, 350)))
                window.blit(text4, text4.get_rect(center=(SCREEN_WIDTH // 2, 450)))

                # Draw planets
                pygame.draw.circle(window, (50, 150, 50), (200, 550), 30)  # Earth
                pygame.draw.circle(window, (200, 80, 50), (400, 580), 25)  # Mars
                pygame.draw.circle(window, (150, 200, 255), (600, 550), 28)  # Ice
                pygame.draw.circle(window, (30, 180, 30), (800, 570), 32)  # Jungle
                pygame.draw.circle(window, (220, 180, 100), (1000, 560), 26)  # Desert

            elif story_page == 2:
                # PAGE 3: The Bosses
                title = big_font.render("EPIC BOSSES DEFEATED", True, (255, 100, 100))
                title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
                window.blit(title, title_rect)

                bosses = ["Star Destroyer", "Zelda Queen", "Giant Robot",
                          "Space Dragon", "Dancing 67", "Mega Worm",
                          "Death Star", "The Bugger", "Dancing Apple"]
                for i, boss in enumerate(bosses):
                    row = i // 3
                    col = i % 3
                    x = 200 + col * 300
                    y = 250 + row * 120
                    boss_text = font.render(boss, True, (255, 200, 100))
                    window.blit(boss_text, boss_text.get_rect(center=(x, y)))
                    pygame.draw.circle(window, (0, 255, 0), (x - 80, y), 8)

            elif story_page == 3:
                # PAGE 4: Peace at last
                title = big_font.render("PEACE AT LAST", True, (100, 255, 100))
                title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
                window.blit(title, title_rect)

                text1 = medium_font.render("With the Zeldas gone...", True, (255, 255, 255))
                text2 = medium_font.render("The galaxy is finally at peace!", True, (255, 255, 255))
                text3 = medium_font.render("All planets are safe again.", True, (100, 255, 150))
                text4 = medium_font.render("You are the GREATEST HERO!", True, (255, 215, 0))
                window.blit(text1, text1.get_rect(center=(SCREEN_WIDTH // 2, 250)))
                window.blit(text2, text2.get_rect(center=(SCREEN_WIDTH // 2, 300)))
                window.blit(text3, text3.get_rect(center=(SCREEN_WIDTH // 2, 350)))
                window.blit(text4, text4.get_rect(center=(SCREEN_WIDTH // 2, 450)))

                # Draw peaceful scene with all planets
                for i in range(8):
                    angle = i * 0.785
                    px = SCREEN_WIDTH // 2 + int(math.cos(angle) * 200)
                    py = 600 + int(math.sin(angle) * 50)
                    colors = [(50, 150, 50), (200, 80, 50), (150, 200, 255),
                              (30, 180, 30), (220, 180, 100), (50, 100, 200),
                              (180, 50, 30), (180, 180, 180)]
                    pygame.draw.circle(window, colors[i], (px, py), 20)

            elif story_page == 4:
                # PAGE 5: Credits / The End
                title = big_font.render("THE END", True, (255, 255, 255))
                title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
                window.blit(title, title_rect)

                text1 = medium_font.render("Thank you for playing!", True, (255, 255, 200))
                text2 = medium_font.render("Created by LEO!", True, (255, 200, 100))
                text3 = medium_font.render("With help from Claude!", True, (200, 200, 255))
                text4 = font.render("Final Score: " + str(score), True, (255, 215, 0))
                text5 = font.render("Levels Completed: 2000", True, (100, 255, 100))
                window.blit(text1, text1.get_rect(center=(SCREEN_WIDTH // 2, 250)))
                window.blit(text2, text2.get_rect(center=(SCREEN_WIDTH // 2, 320)))
                window.blit(text3, text3.get_rect(center=(SCREEN_WIDTH // 2, 370)))
                window.blit(text4, text4.get_rect(center=(SCREEN_WIDTH // 2, 450)))
                window.blit(text5, text5.get_rect(center=(SCREEN_WIDTH // 2, 490)))

                # Sparkles
                for i in range(20):
                    sx = random.randint(100, SCREEN_WIDTH - 100)
                    sy = random.randint(550, 700)
                    pygame.draw.circle(window, (255, 255, 100), (sx, sy), 2)

            # Instructions to continue
            continue_text = font.render("Press SPACE to continue...", True, (150, 150, 150))
            window.blit(continue_text, continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)))

            story_ending_timer = story_ending_timer + 1

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

        # --- DRAW TURRET LASERS! ---
        # Green lasers from your turrets!
        for laser in turret_lasers:
            lx = int(laser[0])
            ly = int(laser[1])
            # Draw a glowing green laser
            pygame.draw.circle(window, (100, 255, 100), (lx, ly), 6)  # Outer glow
            pygame.draw.circle(window, (200, 255, 200), (lx, ly), 3)  # Inner bright

        # --- DRAW TURRETS ON PLANETS! ---
        # Turrets show on planets when visible on screen!
        for building in buildings:
            if building[3] == "turret":
                # Find which planet this turret is on
                for planet in planets:
                    if planet[2] == building[0]:
                        # Get planet's screen position
                        px = int(planet[0] - camera_x)
                        py = int(planet[1] - camera_y)
                        planet_size = planet[4]

                        # Only draw if on screen
                        if px > -100 and px < SCREEN_WIDTH + 100:
                            if py > -100 and py < SCREEN_HEIGHT + 100:
                                # Draw turret on top of planet
                                tx = px
                                ty = py - planet_size - 15  # Above the planet

                                # Get health (default 3 if not set)
                                health = building[4] if len(building) > 4 else 3

                                # Turret base
                                pygame.draw.rect(window, (80, 80, 80), (tx - 12, ty + 8, 24, 8))

                                # Turret body (green)
                                pygame.draw.rect(window, (50, 150, 50), (tx - 8, ty - 5, 16, 15))

                                # Turret cannon
                                pygame.draw.rect(window, (30, 100, 30), (tx - 3, ty - 15, 6, 12))

                                # Turret dome
                                pygame.draw.circle(window, (100, 200, 100), (tx, ty), 8)

                                # Health bars
                                for i in range(health):
                                    health_color = (50, 255, 50) if health == 3 else (255, 255, 0) if health == 2 else (255, 50, 50)
                                    pygame.draw.rect(window, health_color, (tx - 10 + (i * 8), ty + 18, 6, 3))
                        break

            # Draw ROBOT FACTORIES!
            if building[3] == "factory":
                for planet in planets:
                    if planet[2] == building[0]:
                        px = int(planet[0] - camera_x)
                        py = int(planet[1] - camera_y)
                        planet_size = planet[4]

                        if px > -100 and px < SCREEN_WIDTH + 100:
                            if py > -100 and py < SCREEN_HEIGHT + 100:
                                fx = px
                                fy = py - planet_size - 20

                                # Factory building (gray metal building)
                                pygame.draw.rect(window, (100, 100, 110), (fx - 20, fy - 5, 40, 25))
                                pygame.draw.rect(window, (80, 80, 90), (fx - 22, fy + 18, 44, 5))

                                # Factory chimney
                                pygame.draw.rect(window, (70, 70, 80), (fx + 8, fy - 20, 10, 18))
                                # Smoke puffs!
                                pygame.draw.circle(window, (150, 150, 150), (fx + 13, fy - 25), 5)
                                pygame.draw.circle(window, (170, 170, 170), (fx + 15, fy - 32), 4)

                                # Factory windows (glowing)
                                pygame.draw.rect(window, (0, 200, 255), (fx - 15, fy, 10, 8))
                                pygame.draw.rect(window, (0, 200, 255), (fx + 5, fy, 10, 8))

                                # Gear symbol on front
                                pygame.draw.circle(window, (150, 150, 160), (fx, fy + 10), 6)
                                pygame.draw.circle(window, (80, 80, 90), (fx, fy + 10), 3)

                                # Robot icon above
                                pygame.draw.circle(window, (200, 0, 0), (fx, fy - 10), 4)
                        break

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

            # === MEGA WORM ===
            elif boss_type == "mega_worm":
                # Long segmented worm body!
                worm_color = (100, 180, 60)  # Green worm
                # Draw segments
                for i in range(8):
                    seg_x = bx - i * 25 + math.sin(dragon_fire_timer * 2 + i * 0.5) * 10
                    seg_y = by + math.sin(dragon_fire_timer * 3 + i * 0.3) * 5
                    seg_size = 25 - i * 2
                    pygame.draw.circle(window, worm_color, (int(seg_x), int(seg_y)), seg_size)
                    pygame.draw.circle(window, (80, 140, 40), (int(seg_x), int(seg_y)), seg_size, 3)
                # Worm head (bigger!)
                pygame.draw.circle(window, worm_color, (bx + 20, by), 35)
                pygame.draw.circle(window, (80, 140, 40), (bx + 20, by), 35, 4)
                # Angry eyes
                pygame.draw.circle(window, (255, 255, 0), (bx + 10, by - 10), 10)
                pygame.draw.circle(window, (255, 255, 0), (bx + 30, by - 10), 10)
                pygame.draw.circle(window, (0, 0, 0), (bx + 12, by - 8), 5)
                pygame.draw.circle(window, (0, 0, 0), (bx + 32, by - 8), 5)
                # Big scary mouth!
                pygame.draw.arc(window, (200, 0, 0), (bx, by + 5, 40, 25), 3.14, 6.28, 5)
                # Fangs!
                pygame.draw.polygon(window, (255, 255, 255), [(bx + 5, by + 15), (bx + 10, by + 30), (bx + 15, by + 15)])
                pygame.draw.polygon(window, (255, 255, 255), [(bx + 25, by + 15), (bx + 30, by + 30), (bx + 35, by + 15)])
                boss_name = "MEGA WORM"

            # === DEATH STAR ===
            elif boss_type == "death_star":
                # Big gray sphere!
                pygame.draw.circle(window, (120, 120, 130), (bx, by), 80)
                pygame.draw.circle(window, (90, 90, 100), (bx, by), 80, 5)
                # Surface details (lines)
                pygame.draw.line(window, (80, 80, 90), (bx - 80, by), (bx + 80, by), 3)
                pygame.draw.arc(window, (80, 80, 90), (bx - 80, by - 40, 160, 80), 0, 3.14, 2)
                # The super laser dish!
                pygame.draw.circle(window, (60, 60, 70), (bx - 30, by - 20), 30)
                pygame.draw.circle(window, (40, 40, 50), (bx - 30, by - 20), 25)
                pygame.draw.circle(window, (100, 200, 100), (bx - 30, by - 20), 15)
                # Charging effect when about to shoot!
                if boss_shoot_timer > boss_shoot_rate - 200:
                    pygame.draw.circle(window, (150, 255, 150), (bx - 30, by - 20), 20)
                    pygame.draw.circle(window, (200, 255, 200), (bx - 30, by - 20), 12)
                # Surface trenches
                pygame.draw.line(window, (70, 70, 80), (bx - 60, by + 30), (bx + 60, by + 30), 2)
                pygame.draw.line(window, (70, 70, 80), (bx - 50, by + 50), (bx + 50, by + 50), 2)
                boss_name = "DEATH STAR"

            # === THE BUGGER ===
            elif boss_type == "the_bugger":
                # Giant bug body!
                bug_color = (80, 50, 30)  # Brown bug
                # Abdomen (back part)
                pygame.draw.ellipse(window, bug_color, (bx - 60, by, 80, 50))
                pygame.draw.ellipse(window, (60, 40, 20), (bx - 60, by, 80, 50), 3)
                # Stripes on abdomen
                for i in range(4):
                    pygame.draw.line(window, (100, 70, 40), (bx - 50 + i * 20, by + 5), (bx - 50 + i * 20, by + 45), 2)
                # Thorax (middle)
                pygame.draw.ellipse(window, bug_color, (bx - 20, by - 15, 50, 40))
                # Head
                pygame.draw.circle(window, bug_color, (bx + 40, by), 25)
                # Creepy bug eyes (big and red!)
                pygame.draw.circle(window, (200, 0, 0), (bx + 30, by - 10), 15)
                pygame.draw.circle(window, (200, 0, 0), (bx + 50, by - 10), 15)
                pygame.draw.circle(window, (0, 0, 0), (bx + 32, by - 10), 8)
                pygame.draw.circle(window, (0, 0, 0), (bx + 52, by - 10), 8)
                # Antennae
                pygame.draw.line(window, bug_color, (bx + 35, by - 20), (bx + 20, by - 50), 4)
                pygame.draw.line(window, bug_color, (bx + 45, by - 20), (bx + 60, by - 50), 4)
                # Creepy legs!
                for i in range(3):
                    leg_y = by + 10 + i * 12
                    # Left legs
                    pygame.draw.line(window, bug_color, (bx - 30, leg_y), (bx - 80, leg_y + 30), 4)
                    pygame.draw.line(window, bug_color, (bx - 80, leg_y + 30), (bx - 90, leg_y + 50), 3)
                    # Right legs
                    pygame.draw.line(window, bug_color, (bx + 10, leg_y), (bx + 60, leg_y + 30), 4)
                    pygame.draw.line(window, bug_color, (bx + 60, leg_y + 30), (bx + 70, leg_y + 50), 3)
                # Mandibles!
                pygame.draw.line(window, (60, 40, 20), (bx + 55, by + 5), (bx + 75, by + 20), 5)
                pygame.draw.line(window, (60, 40, 20), (bx + 55, by + 10), (bx + 75, by + 25), 5)
                boss_name = "THE BUGGER"

            # === DANCING APPLE ===
            elif boss_type == "dancing_apple":
                # This apple GLOWS and DANCES!
                glow_pulse = abs(math.sin(dance_angle * 4))

                # OUTER GLOW! (rainbow colors that pulse!)
                glow_colors = [
                    (255, int(100 + glow_pulse * 155), int(100 + glow_pulse * 155)),
                    (int(100 + glow_pulse * 155), 255, int(100 + glow_pulse * 155)),
                    (int(100 + glow_pulse * 155), int(100 + glow_pulse * 155), 255),
                ]
                glow_color = glow_colors[int(dance_angle) % 3]
                pygame.draw.circle(window, glow_color, (int(bx), int(by)), 90)
                pygame.draw.circle(window, (255, 255, 200), (int(bx), int(by)), 75)

                # APPLE BODY! (big red apple!)
                apple_red = (220, 30, 30)
                # Main apple shape (round with slight indent at top)
                pygame.draw.circle(window, apple_red, (int(bx), int(by + 10)), 60)
                pygame.draw.circle(window, (200, 20, 20), (int(bx - 25), int(by)), 45)
                pygame.draw.circle(window, (200, 20, 20), (int(bx + 25), int(by)), 45)
                # Shiny highlight
                pygame.draw.circle(window, (255, 150, 150), (int(bx - 20), int(by - 20)), 15)
                pygame.draw.circle(window, (255, 200, 200), (int(bx - 15), int(by - 25)), 8)

                # STEM! (brown stick on top)
                pygame.draw.rect(window, (100, 60, 20), (int(bx - 5), int(by - 55), 10, 25))
                pygame.draw.rect(window, (80, 40, 10), (int(bx - 3), int(by - 55), 6, 25))

                # LEAF! (green leaf on stem)
                pygame.draw.ellipse(window, (50, 180, 50), (int(bx + 5), int(by - 50), 30, 15))
                pygame.draw.ellipse(window, (80, 220, 80), (int(bx + 8), int(by - 48), 24, 10))

                # CUTE FACE! (this apple is happy but EVIL!)
                # Big happy eyes (but with angry eyebrows!)
                pygame.draw.circle(window, (255, 255, 255), (int(bx - 18), int(by)), 14)
                pygame.draw.circle(window, (255, 255, 255), (int(bx + 18), int(by)), 14)
                # Pupils
                pygame.draw.circle(window, (0, 0, 0), (int(bx - 15), int(by + 2)), 7)
                pygame.draw.circle(window, (0, 0, 0), (int(bx + 21), int(by + 2)), 7)
                # Eye sparkle
                pygame.draw.circle(window, (255, 255, 255), (int(bx - 17), int(by - 2)), 3)
                pygame.draw.circle(window, (255, 255, 255), (int(bx + 19), int(by - 2)), 3)
                # EVIL EYEBROWS!
                pygame.draw.line(window, (0, 0, 0), (int(bx - 30), int(by - 18)), (int(bx - 8), int(by - 12)), 4)
                pygame.draw.line(window, (0, 0, 0), (int(bx + 30), int(by - 18)), (int(bx + 8), int(by - 12)), 4)
                # Big happy smile (but creepy!)
                pygame.draw.arc(window, (0, 0, 0), (int(bx - 25), int(by + 5), 50, 35), 3.3, 6.1, 4)
                # Teeth!
                pygame.draw.rect(window, (255, 255, 255), (int(bx - 15), int(by + 18), 10, 8))
                pygame.draw.rect(window, (255, 255, 255), (int(bx + 5), int(by + 18), 10, 8))

                # DANCING ARMS! (wiggling!)
                arm_wave = math.sin(dance_angle * 8) * 20
                # Left arm
                pygame.draw.line(window, apple_red, (int(bx - 50), int(by + 10)), (int(bx - 80), int(by - 20 + arm_wave)), 10)
                pygame.draw.circle(window, apple_red, (int(bx - 80), int(by - 20 + arm_wave)), 12)
                # Right arm
                pygame.draw.line(window, apple_red, (int(bx + 50), int(by + 10)), (int(bx + 80), int(by - 20 - arm_wave)), 10)
                pygame.draw.circle(window, apple_red, (int(bx + 80), int(by - 20 - arm_wave)), 12)

                # DANCING LEGS! (kicking!)
                leg_kick = math.sin(dance_angle * 6) * 15
                # Left leg
                pygame.draw.line(window, apple_red, (int(bx - 20), int(by + 55)), (int(bx - 30 + leg_kick), int(by + 90)), 10)
                pygame.draw.circle(window, (80, 40, 20), (int(bx - 30 + leg_kick), int(by + 90)), 10)
                # Right leg
                pygame.draw.line(window, apple_red, (int(bx + 20), int(by + 55)), (int(bx + 30 - leg_kick), int(by + 90)), 10)
                pygame.draw.circle(window, (80, 40, 20), (int(bx + 30 - leg_kick), int(by + 90)), 10)

                # SPARKLES around the dancing apple!
                for i in range(8):
                    sparkle_angle = dance_angle * 2 + i * 0.785
                    sx = bx + math.cos(sparkle_angle) * 100
                    sy = by + math.sin(sparkle_angle) * 100
                    sparkle_size = int(3 + glow_pulse * 5)
                    pygame.draw.circle(window, (255, 255, 100), (int(sx), int(sy)), sparkle_size)

                boss_name = "DANCING APPLE"

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
            # Get the current skin colors!
            skin_body = (0, 100, 255)  # Default blue
            skin_accent = (50, 80, 200)  # Default darker blue
            skin_name = current_skin
            for skin in all_skins:
                if skin["name"] == current_skin:
                    skin_body = skin["colors"]["body"]
                    skin_accent = skin["colors"]["accent"]
                    break

            # SHIELD BUBBLE! Draw it behind Thrawn if you have shields!
            if shield_hits > 0:
                # Glowing blue bubble around Thrawn!
                # Outer glow
                pygame.draw.circle(window, (50, 100, 200), (int(thrawn_x), int(thrawn_y)), 45, 3)
                # Inner bubble (semi-transparent look with multiple circles)
                pygame.draw.circle(window, (100, 150, 255), (int(thrawn_x), int(thrawn_y)), 42, 2)
                pygame.draw.circle(window, (150, 200, 255), (int(thrawn_x), int(thrawn_y)), 38, 1)

            # Draw different skins - COOL SPACESHIPS!
            tx = int(thrawn_x)
            ty = int(thrawn_y)

            # Ship body - main triangle
            pygame.draw.polygon(window, skin_body, [
                (tx, ty - 30),
                (tx - 25, ty + 20),
                (tx + 25, ty + 20)
            ])

            # Cockpit (oval in center)
            pygame.draw.ellipse(window, skin_accent, (tx - 10, ty - 15, 20, 25))

            # Wings!
            pygame.draw.polygon(window, skin_accent, [
                (tx - 20, ty + 10),
                (tx - 40, ty + 25),
                (tx - 15, ty + 20)
            ])
            pygame.draw.polygon(window, skin_accent, [
                (tx + 20, ty + 10),
                (tx + 40, ty + 25),
                (tx + 15, ty + 20)
            ])

            # Engine glow!
            pygame.draw.circle(window, (255, 200, 100), (tx, ty + 25), 8)
            pygame.draw.circle(window, (255, 255, 200), (tx, ty + 25), 4)

            # Special effects for each skin!
            if skin_name == "thrawn":
                # Red glowing cockpit windows (eyes!)
                pygame.draw.ellipse(window, (255, 0, 0), (tx - 8, ty - 8, 6, 4))
                pygame.draw.ellipse(window, (255, 0, 0), (tx + 2, ty - 8, 6, 4))

            elif skin_name == "ender":
                # Battle school lights
                pygame.draw.line(window, (100, 255, 100), (tx - 15, ty + 5), (tx + 15, ty + 5), 2)
                pygame.draw.circle(window, (255, 215, 0), (tx, ty - 5), 4)  # Command star

            elif skin_name == "robot":
                # Scanner visor
                pygame.draw.rect(window, (255, 0, 0), (tx - 8, ty - 10, 16, 4))
                pygame.draw.circle(window, (0, 200, 255), (tx, ty + 5), 5)  # Reactor

            elif skin_name == "ninja":
                # Red headband stripe
                pygame.draw.rect(window, (150, 0, 0), (tx - 20, ty - 5, 40, 4))
                # Glowing red eyes
                pygame.draw.circle(window, (255, 0, 0), (tx - 5, ty - 8), 3)
                pygame.draw.circle(window, (255, 0, 0), (tx + 5, ty - 8), 3)

            elif skin_name == "alien":
                # Big alien eyes
                pygame.draw.ellipse(window, (0, 0, 0), (tx - 10, ty - 15, 8, 12))
                pygame.draw.ellipse(window, (0, 0, 0), (tx + 2, ty - 15, 8, 12))
                pygame.draw.ellipse(window, (100, 255, 150), (tx - 8, ty - 13, 4, 6))
                pygame.draw.ellipse(window, (100, 255, 150), (tx + 4, ty - 13, 4, 6))
                # Antennae!
                pygame.draw.line(window, skin_accent, (tx - 5, ty - 28), (tx - 12, ty - 40), 2)
                pygame.draw.line(window, skin_accent, (tx + 5, ty - 28), (tx + 12, ty - 40), 2)
                pygame.draw.circle(window, (255, 255, 0), (tx - 12, ty - 40), 3)
                pygame.draw.circle(window, (255, 255, 0), (tx + 12, ty - 40), 3)

            elif skin_name == "fire":
                # Flame trails!
                for fx in [-10, 0, 10]:
                    pygame.draw.polygon(window, (255, 100, 0), [(tx + fx, ty + 20), (tx + fx - 5, ty + 35), (tx + fx + 5, ty + 35)])
                    pygame.draw.polygon(window, (255, 200, 50), [(tx + fx, ty + 22), (tx + fx - 3, ty + 32), (tx + fx + 3, ty + 32)])
                # Fiery eyes
                pygame.draw.circle(window, (255, 255, 0), (tx - 5, ty - 5), 4)
                pygame.draw.circle(window, (255, 255, 0), (tx + 5, ty - 5), 4)

            elif skin_name == "ice":
                # Ice crystals on wings
                pygame.draw.polygon(window, (200, 230, 255), [(tx - 30, ty + 15), (tx - 35, ty + 5), (tx - 25, ty + 10)])
                pygame.draw.polygon(window, (200, 230, 255), [(tx + 30, ty + 15), (tx + 35, ty + 5), (tx + 25, ty + 10)])
                # Icy blue eyes
                pygame.draw.circle(window, (100, 200, 255), (tx - 5, ty - 5), 4)
                pygame.draw.circle(window, (100, 200, 255), (tx + 5, ty - 5), 4)
                # Sparkles
                pygame.draw.circle(window, (255, 255, 255), (tx - 18, ty + 8), 2)
                pygame.draw.circle(window, (255, 255, 255), (tx + 18, ty + 8), 2)

            elif skin_name == "gold":
                # Crown on top!
                pygame.draw.polygon(window, (255, 215, 0), [
                    (tx - 10, ty - 28), (tx - 8, ty - 38), (tx - 4, ty - 32),
                    (tx, ty - 42), (tx + 4, ty - 32), (tx + 8, ty - 38), (tx + 10, ty - 28)
                ])
                # Jewels!
                pygame.draw.circle(window, (255, 0, 0), (tx - 4, ty - 35), 2)
                pygame.draw.circle(window, (0, 100, 255), (tx, ty - 38), 2)
                pygame.draw.circle(window, (0, 255, 0), (tx + 4, ty - 35), 2)
                # Sparkles!
                for sx, sy in [(tx - 22, ty), (tx + 22, ty), (tx - 15, ty + 15), (tx + 15, ty + 15)]:
                    pygame.draw.circle(window, (255, 255, 200), (sx, sy), 2)

            elif skin_name == "custom":
                # Custom skin - draw pixels over ship!
                if len(custom_skin_pixels) > 0:
                    for pixel in custom_skin_pixels:
                        px = tx + pixel[0] - 16
                        py = ty + pixel[1] - 16
                        pygame.draw.rect(window, pixel[2], (px, py, 2, 2))

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

        # --- DRAW HELPER ROBOTS! ---
        # Robots from factories that help you fight!
        if game_state == "playing":
            for robot in helper_robots:
                rx = int(robot[0])
                ry = int(robot[1])

                # Robot body (chrome rectangle)
                pygame.draw.rect(window, (150, 150, 160), (rx - 12, ry - 15, 24, 30))
                pygame.draw.rect(window, (180, 180, 190), (rx - 8, ry - 10, 16, 20))

                # Robot head
                pygame.draw.rect(window, (130, 130, 140), (rx - 8, ry - 25, 16, 12))

                # Robot eyes (blue glowing)
                pygame.draw.rect(window, (0, 200, 255), (rx - 6, ry - 22, 5, 4))
                pygame.draw.rect(window, (0, 200, 255), (rx + 1, ry - 22, 5, 4))

                # Antenna
                pygame.draw.line(window, (100, 100, 110), (rx, ry - 25), (rx, ry - 32), 2)
                pygame.draw.circle(window, (255, 0, 0), (rx, ry - 32), 3)

                # Robot arms
                pygame.draw.line(window, (120, 120, 130), (rx - 12, ry - 5), (rx - 20, ry + 5), 4)
                pygame.draw.line(window, (120, 120, 130), (rx + 12, ry - 5), (rx + 20, ry + 5), 4)

                # Robot jets (flames coming out bottom!)
                pygame.draw.polygon(window, (255, 150, 0), [(rx - 6, ry + 15), (rx - 8, ry + 25), (rx - 4, ry + 25)])
                pygame.draw.polygon(window, (255, 150, 0), [(rx + 6, ry + 15), (rx + 4, ry + 25), (rx + 8, ry + 25)])

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

            # Show food bar below score!
            food_label = font.render("FOOD:", True, (255, 200, 100))
            window.blit(food_label, (10, 35))
            pygame.draw.rect(window, (50, 50, 50), (80, 38, 100, 15))
            food_bar_width = int((food / 100) * 96)
            food_bar_color = (50, 200, 50) if food > 30 else (200, 50, 50)
            pygame.draw.rect(window, food_bar_color, (82, 40, food_bar_width, 11))

            # Show username
            if current_user != "":
                user_text = font.render("Player: " + current_user, True, (150, 150, 255))
                window.blit(user_text, (10, 55))

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
