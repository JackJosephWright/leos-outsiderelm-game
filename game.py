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
laser_speed = 0.5  # How fast lasers fly up (bigger = faster!)

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

    # Fill the window with BLACK (like space!)
    window.fill((0, 0, 0))

    # --- DRAW THE STARS ---
    # Go through each star and draw a tiny white dot
    for star in stars:
        pygame.draw.circle(window, (255, 255, 255), star, 2)
        # (255, 255, 255) = WHITE, star = where to draw, 2 = tiny size

    # --- DRAW THE LASERS ---
    # Draw each laser as a RED rectangle (like a laser beam!)
    for laser in lasers:
        # pygame.draw.rect needs: window, color, (x, y, width, height)
        # laser[0] is x position, laser[1] is y position
        pygame.draw.rect(window, (255, 0, 0), (laser[0] - 2, laser[1], 4, 15))
        # (255, 0, 0) = RED!, width = 4 pixels, height = 15 pixels

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

    # Show everything on screen
    pygame.display.flip()

# Turn off Pygame when done
pygame.quit()
