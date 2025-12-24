# SPACE SHOOTER - by Commander Leo!
# ===================================

# This line gets Pygame ready (Pygame helps us make games!)
import pygame
# Random helps us put stars in random places!
import random

# Wake up Pygame! (like turning on a game console)
pygame.init()

# --- MAKE THE WINDOW ---
# These numbers are how big the window is (wide, tall)
window = pygame.display.set_mode((800, 600))

# Give our window a name at the top!
pygame.display.set_caption("Space Shooter - by thrawn geek !")

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
zeldas = []  # Empty list to hold our angry Zeldas
zelda_speed = .2  # How fast Zeldas fly down (bigger = faster!)
zelda_spawn_timer = 0  # Counts up until it's time to spawn a new Zelda
zelda_spawn_rate = 2000  # How often a new Zelda appears (bigger = less often)

# --- EXPLOSIONS ---
# When a laser hits a Zelda, BOOM! We show an explosion!
explosions = []  # Each explosion is [x, y, timer] - timer counts down then it disappears

# --- SCORE AND LIVES ---
score = 0  # Your score! Goes up when you destroy Zeldas!
lives = 3  # You start with 3 lives! Don't let Zeldas hit you!

# --- TEXT FOR SHOWING SCORE ---
# This sets up the font so we can write words on screen!
font = pygame.font.Font(None, 36)  # 36 = size of the text

# --- GAME LOOP ---
# The game keeps running until we close it
running = True

while running:
    # Check if player closes the window (clicks the X)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- SHOOTING LASERS ---
        # When SPACE bar is pressed, shoot a laser!
        if event.type == pygame.KEYDOWN:  # A key was just pressed
            if event.key == pygame.K_SPACE:  # Was it SPACE?
                # Create a new laser at Thrawn's nose (top of the ship!)
                new_laser = [thrawn_x, thrawn_y - 30]  # [x position, y position]
                lasers.append(new_laser)  # Add it to our laser list!

    # --- MOVE THRAWN WITH ARROW KEYS ---
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
    zelda_spawn_timer = zelda_spawn_timer + 1
    if zelda_spawn_timer >= zelda_spawn_rate:
        # Time to spawn a new angry Zelda!
        new_zelda_x = random.randint(30, 770)  # Random spot (not too close to edges)
        new_zelda_y = -30  # Start above the screen (so it flies in!)
        zeldas.append([new_zelda_x, new_zelda_y])
        zelda_spawn_timer = 0  # Reset the timer!

    # --- MOVE THE ANGRY ZELDAS ---
    # Each Zelda flies DOWN toward Thrawn!
    for zelda in zeldas:
        zelda[1] = zelda[1] + zelda_speed  # Move down (add to y)

    # Remove Zeldas that flew off the bottom of the screen
    zeldas_to_keep = []
    for zelda in zeldas:
        if zelda[1] < 650:  # If Zelda is still on screen
            zeldas_to_keep.append(zelda)
    zeldas = zeldas_to_keep

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

    # --- GAME OVER? ---
    # If you run out of lives, the game stops!
    if lives <= 0:
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
