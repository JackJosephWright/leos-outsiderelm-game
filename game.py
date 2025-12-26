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

# Wake up Pygame! (like turning on a game console)
pygame.init()

# --- MUSIC! ---
# Initialize the music mixer and play some epic tunes!
pygame.mixer.init()

# Find all the songs in the music folder!
music_folder = "music"
songs = []  # List to hold all our song file paths

# Look for all mp3 and wav files in the music folder
if os.path.exists(music_folder):
    for file in os.listdir(music_folder):
        if file.endswith(".mp3") or file.endswith(".wav"):
            songs.append(os.path.join(music_folder, file))
    print("Found " + str(len(songs)) + " songs!")

# Function to play a random song!
def play_random_song():
    if len(songs) > 0:
        song = random.choice(songs)  # Pick a random song!
        pygame.mixer.music.load(song)
        pygame.mixer.music.set_volume(0.5)  # 50% volume
        pygame.mixer.music.play()  # Play once (we'll pick a new one when it ends!)
        print("Now playing: " + song)

# Start playing a random song!
play_random_song()

# Set up an event for when the music ends so we can play another!
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

# --- MAKE THE WINDOW ---
# These numbers are how big the window is (wide, tall)
window = pygame.display.set_mode((800, 600))

# Give our window a name at the top!
pygame.display.set_caption("In Outsiderelm")

# --- THRAWN THE HERO ---
# Thrawn starts at the bottom center of the screen
thrawn_x = 400  # Middle of screen (800 / 2)
thrawn_y = 500  # Near the bottom
thrawn_speed = .1  # How fast Thrawn moves (bigger = faster!)

# --- MAKE THE STARS ---
# We make 50 stars at random spots in our space!
stars = []  # Empty list to hold our stars
for i in range(50):  # Do this 50 times
    x = random.randint(0, 800)  # Random spot left-to-right
    y = random.randint(0, 600)  # Random spot top-to-bottom
    stars.append((x, y))  # Add this star to our list!

# --- LASERS ---
# This list holds all the lasers Thrawn shoots!
lasers = []  # Empty list - lasers get added when SPACE is pressed
laser_speed = .5  # How fast lasers fly up (bigger = faster!)

# --- ANGRY ZELDAS ---
# These are the bad guys! Green circles with angry faces!
zeldas = []  # Empty list to hold our angry Zeldas - each is [x, y, x_direction]
zelda_speed = .2  # How fast Zeldas fly down (bigger = faster!)
zelda_side_speed = .15  # How fast Zeldas move side to side!
zelda_spawn_timer = 0  # Counts up until it's time to spawn a new Zelda
zelda_spawn_rate = 2000  # How often a new Zelda appears (bigger = less often)

# --- ZELDA'S SWORDS ---
# The Zeldas fight back by throwing swords at Thrawn!
swords = []  # Each sword is [x, y] position
sword_speed = 0.3  # How fast swords fly down (bigger = faster!)
sword_timer = 0  # Counts up until Zeldas throw more swords
sword_rate = 1500  # How often Zeldas throw swords (bigger = less often)

# --- EXPLOSIONS ---
# When a laser hits a Zelda, BOOM! We show an explosion!
explosions = []  # Each explosion is [x, y, timer] - timer counts down then it disappears

# --- SCORE AND LIVES ---
score = 0  # Your score! Goes up when you destroy Zeldas!
lives = 3  # You start with 3 lives! Don't let Zeldas hit you!

# --- TEXT FOR SHOWING SCORE ---
# This sets up the font so we can write words on screen!
font = pygame.font.Font(None, 36)  # 36 = size of the text
big_font = pygame.font.Font(None, 100)  # BIG font for GAME OVER!
medium_font = pygame.font.Font(None, 50)  # Medium font for final score

# --- STAR DESTROYER BOSS ---
# The big bad boss! Appears after you get enough points!
boss_active = False  # Is the boss on screen?
boss_x = 400  # Boss x position (center of screen)
boss_y = -150  # Boss y position (starts above screen)
boss_health = 20  # How many hits to defeat the boss!
boss_max_health = 20  # For the health bar
boss_speed = 0.1  # How fast boss moves side to side
boss_direction = 1  # 1 = moving right, -1 = moving left
boss_shoot_timer = 0  # Timer for boss shooting
boss_shoot_rate = 800  # How often boss shoots
boss_lasers = []  # Boss's laser beams!
boss_spawn_score = 500  # Boss appears when you reach this score!
boss_defeated = False  # Did we beat the boss?
boss_defeated_timer = 0  # For boss explosion animation

# --- GAME OVER STUFF ---
game_over = False  # When True, show the game over screen!
game_over_timer = 0  # Counts up during game over for animations
game_over_explosions = []  # Extra explosions for the big finale!

# --- GAME LOOP ---
# The game keeps running until we close it
running = True

while running:
    # Check if player closes the window (clicks the X)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- PLAY NEXT SONG WHEN CURRENT ONE ENDS ---
        if event.type == SONG_END:
            play_random_song()  # Pick another random song!

        # --- SHOOTING LASERS ---
        # When SPACE bar is pressed, shoot a laser! (only if game is NOT over)
        if event.type == pygame.KEYDOWN and not game_over:  # A key was just pressed
            if event.key == pygame.K_SPACE:  # Was it SPACE?
                # Create a new laser at Thrawn's nose (top of the ship!)
                new_laser = [thrawn_x, thrawn_y - 30]  # [x position, y position]
                lasers.append(new_laser)  # Add it to our laser list!

    # --- MOVE THRAWN WITH ARROW KEYS ---
    # Only move if game is NOT over!
    if not game_over:
        # Check which keys are being pressed right now
        keys = pygame.key.get_pressed()

        # Move left (but don't go off screen!)
        if keys[pygame.K_LEFT] and thrawn_x > 25:
            thrawn_x = thrawn_x - thrawn_speed

        # Move right (but don't go off screen!)
        if keys[pygame.K_RIGHT] and thrawn_x < 775:
            thrawn_x = thrawn_x + thrawn_speed

        # Move up (but don't go off screen!)
        if keys[pygame.K_UP] and thrawn_y > 30:
            thrawn_y = thrawn_y - thrawn_speed

        # Move down (but don't go off screen!)
        if keys[pygame.K_DOWN] and thrawn_y < 580:
            thrawn_y = thrawn_y + thrawn_speed

    # --- MOVE THE LASERS ---
    # Each laser flies UP the screen!
    for laser in lasers:
        laser[1] = laser[1] - laser_speed  # Move up (subtract from y)

    # Remove lasers that flew off the top of the screen
    # (We don't need them anymore - they're in outer space now!)
    lasers_to_keep = []  # New list for lasers still on screen
    for laser in lasers:
        if laser[1] > 0:  # If laser is still visible
            lasers_to_keep.append(laser)  # Keep it!
    lasers = lasers_to_keep  # Replace old list with new list

    # --- SPAWN ANGRY ZELDAS ---
    # The timer counts up, and when it's big enough, a new Zelda appears!
    # (Don't spawn new ones if game is over!)
    if not game_over:
        zelda_spawn_timer = zelda_spawn_timer + 1
    if zelda_spawn_timer >= zelda_spawn_rate and not game_over:
        # Time to spawn a new angry Zelda!
        new_zelda_x = random.randint(30, 770)  # Random spot (not too close to edges)
        new_zelda_y = -30  # Start above the screen (so it flies in!)
        # Random direction: -1 = moving left, 1 = moving right
        new_zelda_dir = random.choice([-1, 1])
        zeldas.append([new_zelda_x, new_zelda_y, new_zelda_dir])
        zelda_spawn_timer = 0  # Reset the timer!

    # --- MOVE THE ANGRY ZELDAS ---
    # Each Zelda flies DOWN and SIDEWAYS in a zigzag pattern!
    for zelda in zeldas:
        zelda[1] = zelda[1] + zelda_speed  # Move down (add to y)
        zelda[0] = zelda[0] + (zelda_side_speed * zelda[2])  # Move sideways!

        # Bounce off the walls! If Zelda hits edge, reverse direction!
        if zelda[0] <= 30:  # Hit left wall?
            zelda[2] = 1    # Now move right!
        if zelda[0] >= 770:  # Hit right wall?
            zelda[2] = -1   # Now move left!

    # Remove Zeldas that flew off the bottom of the screen
    zeldas_to_keep = []
    for zelda in zeldas:
        if zelda[1] < 650:  # If Zelda is still on screen
            zeldas_to_keep.append(zelda)
    zeldas = zeldas_to_keep

    # --- ZELDAS THROW SWORDS! ---
    # Every so often, each Zelda on screen throws a sword at Thrawn!
    # (Don't throw if game is over!)
    if not game_over:
        sword_timer = sword_timer + 1
    if sword_timer >= sword_rate and not game_over:
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
        sword[1] = sword[1] + sword_speed  # Move down (add to y)

    # Remove swords that flew off the bottom of the screen
    swords_to_keep = []
    for sword in swords:
        if sword[1] < 650:
            swords_to_keep.append(sword)
    swords = swords_to_keep

    # --- STAR DESTROYER BOSS! ---
    # Spawn the boss when player reaches enough points!
    if score >= boss_spawn_score and not boss_active and not boss_defeated and not game_over:
        boss_active = True
        boss_x = 400
        boss_y = -150  # Start above screen
        boss_health = boss_max_health

    # Move the boss if it's active
    if boss_active and not game_over:
        # Fly down onto the screen first
        if boss_y < 80:
            boss_y = boss_y + 0.05
        else:
            # Move side to side once in position
            boss_x = boss_x + (boss_speed * boss_direction)

            # Bounce off walls
            if boss_x <= 150:
                boss_direction = 1
            if boss_x >= 650:
                boss_direction = -1

        # Boss shoots green lasers at Thrawn!
        boss_shoot_timer = boss_shoot_timer + 1
        if boss_shoot_timer >= boss_shoot_rate and boss_y > 50:
            # Shoot 3 lasers in a spread pattern!
            boss_lasers.append([boss_x - 60, boss_y + 50, -0.2])  # Left laser (angled left)
            boss_lasers.append([boss_x, boss_y + 60, 0])           # Middle laser (straight)
            boss_lasers.append([boss_x + 60, boss_y + 50, 0.2])   # Right laser (angled right)
            boss_shoot_timer = 0

    # Move boss lasers
    for laser in boss_lasers:
        laser[1] = laser[1] + 0.4  # Move down
        laser[0] = laser[0] + laser[2]  # Move sideways based on angle

    # Remove boss lasers that went off screen
    boss_lasers_to_keep = []
    for laser in boss_lasers:
        if laser[1] < 650:
            boss_lasers_to_keep.append(laser)
    boss_lasers = boss_lasers_to_keep

    # --- BOSS DEFEATED ANIMATION ---
    if boss_defeated:
        boss_defeated_timer = boss_defeated_timer + 1
        if boss_defeated_timer > 2000:
            # Reset for next boss (spawn at higher score next time)
            boss_defeated = False
            boss_defeated_timer = 0
            boss_spawn_score = boss_spawn_score + 1000  # Next boss at 1000 more points!


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
                lasers_to_remove.append(laser)
                zeldas_to_remove.append(zelda)
                # Create an explosion at the Zelda's position!
                explosions.append([zelda[0], zelda[1], 500])  # 500 = how long explosion lasts
                # Add 100 points to the score! Nice shot!
                score = score + 100

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
                if laser in lasers:
                    lasers.remove(laser)
                boss_health = boss_health - 1
                # Small explosion on the boss!
                explosions.append([laser[0], laser[1], 300])

                # Did we defeat the boss?
                if boss_health <= 0:
                    boss_active = False
                    boss_defeated = True
                    boss_defeated_timer = 0
                    # HUGE score bonus for defeating the boss!
                    score = score + 1000
                    # Create massive explosion!
                    for i in range(15):
                        ex = boss_x + random.randint(-100, 100)
                        ey = boss_y + random.randint(-50, 50)
                        explosions.append([ex, ey, 600 + random.randint(0, 300)])

    # --- BOSS LASERS HIT THRAWN? ---
    # Check if boss's green lasers hit the player!
    boss_lasers_to_remove = []
    for laser in boss_lasers:
        distance_x = abs(laser[0] - thrawn_x)
        distance_y = abs(laser[1] - thrawn_y)

        if distance_x < 25 and distance_y < 30:
            boss_lasers_to_remove.append(laser)
            lives = lives - 1
            explosions.append([thrawn_x, thrawn_y, 300])

    for laser in boss_lasers_to_remove:
        if laser in boss_lasers:
            boss_lasers.remove(laser)

    # --- UPDATE EXPLOSIONS ---
    # Count down the explosion timers, remove old ones
    explosions_to_keep = []
    for explosion in explosions:
        explosion[2] = explosion[2] - 1  # Count down the timer
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
            lives = lives - 1     # Lose a life!
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
            lives = lives - 1               # Lose a life!
            # Make an explosion where Thrawn got hit!
            explosions.append([thrawn_x, thrawn_y, 300])

    # Remove swords that hit Thrawn
    for sword in swords_to_remove:
        if sword in swords:
            swords.remove(sword)

    # --- GAME OVER? ---
    # If you run out of lives, start the epic game over sequence!
    if lives <= 0 and not game_over:
        game_over = True
        game_over_timer = 0
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
        game_over_timer = game_over_timer + 1
        # After showing explosions for a while, allow quitting
        if game_over_timer > 5000:
            # Press any key to quit after game over
            keys = pygame.key.get_pressed()
            if any(keys):
                running = False

    # Fill the window with BLACK (like space!)
    window.fill((0, 0, 0))

    # --- DRAW THE STARS ---
    # Go through each star and draw a tiny white dot
    for star in stars:
        pygame.draw.circle(window, (255, 255, 255), star, 2)
        # (255, 255, 255) = WHITE, star = where to draw, 2 = tiny size

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
        pygame.draw.rect(window, (255, 0, 0), (laser[0] - 2, laser[1], 4, 15))
        # (255, 0, 0) = RED!, width = 4 pixels, height = 15 pixels

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

    # --- DRAW THE STAR DESTROYER BOSS ---
    if boss_active or boss_defeated_timer > 0:
        bx = int(boss_x)
        by = int(boss_y)

        # Main body - big gray triangle (like a Star Destroyer!)
        # The iconic wedge shape!
        pygame.draw.polygon(window, (80, 80, 90), [
            (bx, by - 40),           # Front point (nose)
            (bx - 120, by + 40),     # Back left
            (bx + 120, by + 40)      # Back right
        ])

        # Bridge tower (the raised part on top)
        pygame.draw.polygon(window, (60, 60, 70), [
            (bx - 20, by + 10),      # Left
            (bx + 20, by + 10),      # Right
            (bx + 15, by - 10),      # Top right
            (bx - 15, by - 10)       # Top left
        ])
        # Bridge windows (glowing)
        pygame.draw.rect(window, (255, 255, 100), (bx - 10, by - 5, 20, 5))

        # Engine glow at the back (3 engines)
        pygame.draw.circle(window, (100, 150, 255), (bx - 60, by + 40), 12)  # Left engine
        pygame.draw.circle(window, (100, 150, 255), (bx, by + 40), 15)       # Center engine
        pygame.draw.circle(window, (100, 150, 255), (bx + 60, by + 40), 12)  # Right engine
        # Bright engine cores
        pygame.draw.circle(window, (200, 220, 255), (bx - 60, by + 40), 6)
        pygame.draw.circle(window, (200, 220, 255), (bx, by + 40), 8)
        pygame.draw.circle(window, (200, 220, 255), (bx + 60, by + 40), 6)

        # Detail lines on the hull
        pygame.draw.line(window, (50, 50, 60), (bx, by - 35), (bx - 100, by + 35), 2)
        pygame.draw.line(window, (50, 50, 60), (bx, by - 35), (bx + 100, by + 35), 2)
        pygame.draw.line(window, (50, 50, 60), (bx - 60, by + 20), (bx + 60, by + 20), 2)

        # Weapon turrets (little red dots)
        pygame.draw.circle(window, (255, 50, 50), (bx - 40, by + 15), 4)
        pygame.draw.circle(window, (255, 50, 50), (bx + 40, by + 15), 4)
        pygame.draw.circle(window, (255, 50, 50), (bx, by + 25), 4)

        # --- BOSS HEALTH BAR ---
        if boss_active:
            # Draw health bar above the boss
            bar_width = 150
            bar_height = 10
            bar_x = bx - bar_width // 2
            bar_y = by - 60

            # Background (dark red)
            pygame.draw.rect(window, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            # Health (bright red) - shrinks as boss takes damage
            health_width = int((boss_health / boss_max_health) * bar_width)
            pygame.draw.rect(window, (255, 0, 0), (bar_x, bar_y, health_width, bar_height))
            # Border
            pygame.draw.rect(window, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

            # "BOSS" label
            boss_label = font.render("STAR DESTROYER", True, (255, 255, 255))
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
                wave = math.sin(game_over_timer / 100 + i) * 10
                stink_y = thrawn_y - (game_over_timer / 10) - (i * 30)
                if stink_y > 50:
                    pygame.draw.line(window, (100, 150, 50),
                                   (stink_x + wave, stink_y),
                                   (stink_x - wave, stink_y - 30), 3)

        # Show GAME OVER text after farts start
        if game_over_timer > 500:
            # Draw "GAME OVER" in big green stinky letters!
            game_over_text = big_font.render("GAME OVER", True, (100, 180, 50))
            text_rect = game_over_text.get_rect(center=(400, 250))
            window.blit(game_over_text, text_rect)

            # Funny fart message!
            fart_text = medium_font.render("* PFFFFFTTT *", True, (150, 200, 80))
            fart_rect = fart_text.get_rect(center=(400, 310))
            window.blit(fart_text, fart_rect)

            # Show final score!
            final_score_text = medium_font.render("Final Score: " + str(score), True, (255, 255, 255))
            score_rect = final_score_text.get_rect(center=(400, 370))
            window.blit(final_score_text, score_rect)

        # Show "Press any key" after a bit
        if game_over_timer > 3000:
            press_key_text = font.render("Press any key to exit", True, (150, 150, 150))
            key_rect = press_key_text.get_rect(center=(400, 430))
            window.blit(press_key_text, key_rect)

    # --- DRAW SCORE AND LIVES ---
    # Show the score in the top left!
    score_text = font.render("SCORE: " + str(score), True, (255, 255, 255))
    window.blit(score_text, (10, 10))  # Put it at top-left corner

    # Show lives in the top right!
    lives_text = font.render("LIVES: " + str(lives), True, (255, 0, 0))
    window.blit(lives_text, (680, 10))  # Put it at top-right corner

    # Show everything on screen
    pygame.display.flip()

# Turn off Pygame when done
pygame.quit()
