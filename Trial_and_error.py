import pygame
import time

pygame.init()
pygame.mixer.init()

# Game window dimensions
screen_width = 1000
screen_height = 600

# Create game window
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Cross Road Journey')

# Load and resize the standing character image
char = pygame.image.load('sprites/standing.png')
char = pygame.transform.scale(char, (80, 100))

# Load and resize sprite animations
walkLeft = [pygame.transform.scale(pygame.image.load(f'sprites/L{i}.png'), (80, 100)) for i in range(1, 5)]
walkRight = [pygame.transform.scale(pygame.image.load(f'sprites/R{i}.png'), (80, 100)) for i in range(1, 5)]
walkUp = [pygame.transform.scale(pygame.image.load(f'sprites/U{i}.png'), (80, 100)) for i in range(1, 5)]
walkDown = [pygame.transform.scale(pygame.image.load(f'sprites/D{i}.png'), (80, 100)) for i in range(1, 5)]

# Backgrounds for different phases
bg_spawning = pygame.image.load('Background/spawning_area.png')
bg_phase1 = pygame.image.load('Background/phase1.png')
bg_phase2 = pygame.image.load('Background/phase2.png')
bg_phase3 = pygame.image.load('Background/phase3.png')
bg_phase4 = pygame.image.load('Background/phase4.jpg')
bg_phase5 = pygame.image.load('Background/phase5.jpg')
bg_phase6 = pygame.image.load('background/phase6.png')
bg_phase7 = pygame.image.load('background/phase7.jpg')
bg_phase8 = pygame.image.load('background/phase8.jpg')
#bg_phase9 = pygame.image.load('background/phase9.png')
bg_phase10 = pygame.image.load('background/phase10.jpg')
bg_phase11 = pygame.image.load('background/phase11.jpg')
bg_phase12 = pygame.image.load('background/phase12.png')

# Initial positions for each phase (x, y)
initial_positions = {
    'spawning': (200, 220),
    1: (350, 250),
    2: (0, 260),
    3: (0, 360),
    4: (0, 430), 
    5: (0, 340),
    6: (460, 265),
    7: (0, 300),
    8: (120, 358),
    9: (50, 430),
    10: (50, 430),
    11: (465, 550),
    12: (465, 470)
}

# Restricted areas in the spawning phase (x, y, width, height)
restricted_areas = [
    pygame.Rect(0, 0, 302, 190),     # Stair
    pygame.Rect(505, 0, 490, 120),   # Kitchen counter area
    pygame.Rect(0, 0, 1000, 80),     # Griller
    pygame.Rect(0, 0, 170, 600),     # Left border
    pygame.Rect(810, 0, 170, 600),   # Right border
    pygame.Rect(0, 490, 295, 103),   # Bottom left border
    pygame.Rect(490, 540, 500, 55),  # Bottom right border
    pygame.Rect(385, 320, 255, 35),  # Table area
    pygame.Rect(480, 400, 120, 20),  # Chair
    pygame.Rect(430, 290, 205, 20),  # Top area of table
    pygame.Rect(750, 270, 70, 130),  # TV area
]

# Start at the spawning area
current_phase = 'spawning'
#current_phase = 11

# Game character initial position and movement variables
x, y = initial_positions['spawning']
vel = 8
left = False
right = False
up = False
down = False
walkCount = 0
clock = pygame.time.Clock()
feedback_displayed = False
feedback_start_time = 0


# Spawn Area Objective variables
spawn_objective_rect = pygame.Rect(210, 500, 70, 50)  # Example position and size of the objective
spawn_text_rect = pygame.Rect (30, 90, 320, 50)
bag_image = pygame.image.load('images/bag.png')
bg_spawning_task = pygame.image.load('images/spawntask.png')
objective_completed = False
task_screen = False



# things to bring objectives image
image1 = pygame.image.load('images/notebook.png')
image2 = pygame.image.load('images/ballpen.png')
image3 = pygame.image.load('images/pencil.png')
image4 = pygame.image.load('images/phone.png')
image5 = pygame.image.load('images/lunchbox.png')
image6 = pygame.image.load('images/waterbottle.png')

# Spawn_Area Task variables / x, y, width, height
things_to_bring = [
    {'rect': pygame.Rect(350, 100, 120, 100), 'completed': False, 'image': image1, 'initial_pos': (350, 100)},
    {'rect': pygame.Rect(600, 100, 70, 100), 'completed': False,'image': image2, 'initial_pos': (600, 100)},
    {'rect': pygame.Rect(800, 100, 70, 80), 'completed': False,'image': image3, 'initial_pos': (800, 100)},
    {'rect': pygame.Rect(400, 300, 70, 100), 'completed': False,'image': image4, 'initial_pos': (400, 300)},
    {'rect': pygame.Rect(600, 300, 70, 100), 'completed': False,'image': image5, 'initial_pos': (600, 300)},
    {'rect': pygame.Rect(800, 300, 70, 100), 'completed': False,'image': image6, 'initial_pos': (800, 300)}
    ]

# Large Bag to put the things
large_obj_rect = pygame.Rect(150, 250, 180, 245) # Example position and size
bag_image2 = pygame.image.load('images/Bag_task.png')
dragging = None

def perform_spawn_task():
    global things_to_bring, large_obj_rect, dragging, task_screen, objective_completed, feedback_displayed, feedback_start_time
    win.blit(bg_spawning_task, (0, 0))  # background

    # Draw large objective
    win.blit(bag_image2, large_obj_rect) 

    # Draw things to bring objectives
    for obj in things_to_bring:
        if not obj['completed']:
            win.blit(obj['image'], obj['rect']) # Blit the specific image for this object

    #pygame.display.update()

    # Check for completion
    if all(obj['completed'] for obj in things_to_bring) and not feedback_displayed:
        feedback_displayed = True
        feedback_start_time = pygame.time.get_ticks()
        objective_completed = True
    
    if feedback_displayed:
        font = pygame.font.Font(None, 48)
        feedback_text = "Off we Go!"
        feedback_color = (0, 255, 0)
        text = font.render(feedback_text, True, feedback_color)
        win.blit(text, (200, 100))
        
        # Check if the feedback display duration has passed
        if pygame.time.get_ticks() - feedback_start_time > 2000:  # 1 second duration
            task_screen = False  # Exit the task screen
            feedback_displayed = False  # Reset the feedback display flag
    pygame.display.update()


# PHASE 2

# Phase 2 objective
phase2_objective_rect = pygame.Rect(600, 100, 200, 300) # Example position and size of the phase 2 objective
phase2_task_screen_bg = pygame.image.load('images/phase2_task.png')
phase2_task_completed = False


# Load the sprite sheet for phase 2 objectives\ 
sprite_sheet_cat = pygame.image.load('images/cat.png')
sprite_sheet_dog = pygame.image.load('images/dog.png')
frame_width = 75
frame_height = 75
cat_num_frames = 7
dog_num_frames = 5

# Extract frames from the sprite sheet
cat_frames = [sprite_sheet_cat.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(cat_num_frames)]
dog_frames = [sprite_sheet_dog.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height)) for i in range(dog_num_frames)]

# Animation variables 
current_cat_frame = 0
current_dog_frame = 0
animation_speed = 2 # Higher value means slower animation
frame_count = 0

# Task for phase 2
dog_rect = pygame.Rect(560, 350, 130, 130)    # Example position and size
dog_image = pygame.image.load('images/dog_stationary.png')

cat_rect = pygame.Rect(420, 350, 130, 130)    # Example position and size
cat_image = pygame.image.load('images/cat_stationary.png')
dragging_animal = None

feedback_displayed = False
feedback_start_time = 0

def phase2_update_animation():
    global current_cat_frame, current_dog_frame, frame_count
    frame_count += 1
    if frame_count >= animation_speed:
        current_cat_frame = (current_cat_frame + 1) % cat_num_frames
        current_dog_frame = (current_dog_frame + 1) % dog_num_frames
        frame_count = 0


def perform_phase2_task():
    global dragging_animal, task_screen, phase2_task_completed, feedback_displayed, feedback_start_time
    win.fill((0, 0, 0))  # Black background
    win.blit(phase2_task_screen_bg, (0, 0))


    # Draw the dog and cat
    win.blit(dog_image, dog_rect)
    #pygame.draw.rect(win, (255, 0, 0), dog_rect)
    #pygame.draw.rect(win, (255, 0, 0), cat_rect)  # Cat color
    win.blit(cat_image, cat_rect)
    

    # Check for task completion
    if abs(dog_rect.x - cat_rect.x) > 300 and not feedback_displayed:  # Arbitrary separation distance for completion
        phase2_task_completed = True
        feedback_displayed = True
        feedback_start_time = pygame.time.get_ticks()
        #task_screen = False

    if feedback_displayed:
        font = pygame.font.Font(None, 48)
        feedback_text = "Well done!"
        feedback_color = (0, 255, 0)
        text = font.render(feedback_text, True, feedback_color)
        win.blit(text, (200, 100))
        
        # Check if the feedback display duration has passed
        if pygame.time.get_ticks() - feedback_start_time > 2000:  # 1 second duration
            task_screen = False  # Exit the task screen
            feedback_displayed = False  # Reset the feedback display flag
    pygame.display.update()

# PHASE 3

# Task for phase 3. Help the Grandma cross the pedestrian lane
grandma_rect = pygame.Rect(200, 340, 60, 100) # Example position and size for grandma


grandma_image = pygame.image.load('images/grandma.png')
holding_grandma = False # To check if player is helping the grandma
phase3_task_completed = False
slow_vel = 2


# PHASE 4

# Phase 4 objective
phase4_beggar_rect = pygame.Rect(600, 420, 100, 100)  # Example position and size of the beggar
beggar_image = pygame.image.load('images/beggar.png')
phase4_bg = pygame.image.load('images/phase4_bg.jpg')

# Task for phase 4
beggar_task_rect = pygame.Rect(300, 300, 400, 300)# Example position and size of the beggar in the task screen
beggar_task_image = pygame.image.load('images/beggar2.png')
phase4_task_completed = False

image1_money = pygame.image.load('images/money.png')
image2_toy = pygame.image.load('images/toy.png')
image3_food = pygame.image.load('images/bun.png')


food_items = [
    {'rect': pygame.Rect(150, 100, 150, 150), 'completed': False, 'image': image1_money, 'initial_pos': (150, 100)},  # Example image
    {'rect': pygame.Rect(480, 100, 150, 150), 'completed': False, 'image': image2_toy, 'initial_pos': (480, 100)},
    {'rect': pygame.Rect(800, 100, 150, 150), 'completed': False, 'image': image3_food, 'initial_pos': (800, 100)}
]
# Define the correct item index (3rd choice = Food)
correct_item_index = 2

def perform_phase4_task():
    global task_screen, phase4_task_completed, food_items, dragging, feedback_displayed, feedback_start_time
    win.blit(phase4_bg, (0, 0))

    win.blit(beggar_task_image, beggar_task_rect)
    #pygame.draw.rect(win, (255, 255, 0), food_items)

    # Draw food items
    for item in food_items:
        if not item['completed']:
            #pygame.draw.rect(win, (255, 255, 0), item['rect'])
            win.blit(item['image'], item['rect'])  # Blit the specific image for this food item

    
    # Check for completion
    if food_items[correct_item_index]['completed'] and not feedback_displayed:
        phase4_task_completed = True
        feedback_displayed = True
        feedback_start_time = pygame.time.get_ticks()

    if feedback_displayed:
        font = pygame.font.Font(None, 48)
        feedback_text = "Thank you for the Food!!"
        feedback_color = (0, 255, 0)
        text = font.render(feedback_text, True, feedback_color)
        win.blit(text, (300, 500)) # Adjust the center position
        
        # Check if the feedback display duration has passed
        if pygame.time.get_ticks() - feedback_start_time > 2000:  # 1 second duration
            task_screen = False  # Exit the task screen
            feedback_displayed = False  # Reset the feedback display flag

    pygame.display.update()




# PHASE 5 TASK AND OBJECTIVES

pedestrian_sign_rect = [pygame.Rect(190, 200, 60, 180), pygame.Rect(720, 200, 60, 180)]
pedestrian_sign_image = pygame.image.load('images/1.png')
pedestrian_sign_image2 = pygame.image.load('images/2.png')
pedestrian_image = [pedestrian_sign_image, pedestrian_sign_image2]

signage_questions_rect = [pygame.Rect(120, 200, 200, 200), pygame.Rect(420, 200, 200, 200), pygame.Rect(720, 200, 200, 200)]
road_sign1 = pygame.image.load ('images/dig.png')
road_sign2 = pygame.image.load ('images/bawal.png')
road_sign3 = pygame.image.load ('images/pedestrian.png')
signage_image = [road_sign1, road_sign2, road_sign3]

correct_signage_index = 2

phase5_task_completed = False
task_screen = False
feedback_displayed = False
right_indicator = False
wrong_indicator = False

def perform_phase5_task():
    global task_screen, current_phase, signage_questions_rect, correct_signage_index, feedback_displayed
    win.fill((0, 0, 0))  # Clear the screen

    # Draw the signage questions
    for i, rects in enumerate(signage_questions_rect):
        if i == correct_signage_index:
            win.blit(signage_image[i], rects)
        else:
            color = (255, 0, 0)  # Red for incorrect answers
        pygame.draw.rect(win, color, rects)  # Fill the rectangle with color

        # (Optional) Add border to the rectangle
        pygame.draw.rect(win, (255, 255, 255), rects, 2)  # White border, 2 pixels wide
        win.blit(signage_image[i], rects)

    if feedback_displayed:
        font = pygame.font.Font(None, 48)
        feedback_text = "Correct!" if right_indicator else "Wrong!"
        feedback_color = (0, 255, 0) if right_indicator else (255, 0, 0)
        text = font.render(feedback_text, True, feedback_color)
        win.blit(text, (430, 150))
    
    font = pygame.font.Font(None, 40)
    feedback_text = "Which sign shows that it's safe for pedestrians to cross the street?"
    feedback_color = (255, 255, 255)
    text = font.render(feedback_text, True, feedback_color)
    win.blit(text, (50, 100))

    pygame.display.update()



# PHASE6 OBJECTIVE AND TASK

traffic_light_color = "red"  # Initial color of the traffic light
traffic_light_rect_red = pygame.Rect(708, 174, 35, 35)  # Traffic light rectangle
traffic_light_rect_green = pygame.Rect(708, 119, 35, 35)  # Traffic light rectangle for green light
traffic_light_center = traffic_light_rect_red.center
traffic_light_radius = traffic_light_rect_red.width // 2
traffic_light_center1 = traffic_light_rect_green.center
traffic_light_radius2 = traffic_light_rect_green.width // 2
text_rect = pygame.Rect(20, 50, 15, 15)

# Car variables for phase 6
car_width = 350
car_height = 120
car_rect = pygame.Rect(-700, 400, car_width, car_height)  # Initial car position
phase6_car_image = pygame.image.load('images/phase6_car.png')

car_rect2 = pygame.Rect(-1200, 450, car_width, car_height)  # Initial car position
phase6_car_image2 = pygame.image.load('images/phase6_car2.png')
car_vel = 4
walk_vel = 4
phase6_task_completed = False
phase6_upper_boundary = 260


def reset_car_position():
    global car_rect, car_rect2
    if not phase6_task_completed:
        car_rect.x = -800
        car_rect2.x = -600

def update_traffic_light():
    global traffic_light_color
    if car_rect and car_rect2.x >= 800:
        traffic_light_color = "green"
    else:
        traffic_light_color = "red"

def phase6_moving_car():
    global car_rect, car_rect2
    if not phase6_task_completed:
        car_rect.x += car_vel
        car_rect2.x += car_vel
    else:
        car_rect.x > screen_width
        car_rect2.x > screen_width
        reset_car_position()



# PHASE 7 TASK 

sit_down_rect = pygame.Rect(875, 290, 50, 51)
sit_down_image = pygame.image.load('images/arrow.png')

signages_rect = [pygame.Rect(120, 250, 200, 200), pygame.Rect(400, 250, 200, 200), pygame.Rect(700, 250, 200, 200),]
signage_image1 = pygame.image.load('images/stop.png')
signage_image2 = pygame.image.load('images/bus_sign.png')
signage_image3 = pygame.image.load('images/pedestrian.png')
correct_answer_index = 1
phase_7right_indicator = False
phase_7wrong_indicator = False

signage_images = [signage_image1, signage_image2, signage_image3]


# Function to handle the Phase 7 task
def perform_phase7_task():
    global task_screen, current_phase, signages_rect, correct_answer_index, feedback_start_time, feedback_displayed, phase_7right_indicator
    win.fill((0, 0, 0))  # Clear the screen

    # Draw the signages
    for i, rect in enumerate(signages_rect):
        win.blit(signage_images[i], rect)
        pygame.draw.rect(win, (255, 255, 255), rect, 2)  
        win.blit(signage_images[i], rect)

    if feedback_displayed:
        font = pygame.font.Font(None, 48)
        feedback_text = "Correct!" if phase_7right_indicator else "Wrong!"
        feedback_color = (0, 255, 0) if phase_7right_indicator else (255, 0, 0)
        text = font.render(feedback_text, True, feedback_color)
        win.blit(text, (430, 150))
    
    font = pygame.font.Font(None, 40)
    feedback_text = "Which sign shows the bus stop?"
    feedback_color = (255, 255, 255)
    text = font.render(feedback_text, True, feedback_color)
    win.blit(text, (50, 100))

    pygame.display.update()





# PHASE 8 RECT

phase8_rect = pygame.Rect(550, 250, 200, 200)


# PHASE 9

phase9_bus_rect = pygame.Rect(150, 410, 400, 122)
bus_image = pygame.image.load('images/bus.png')


background_loop_count = 0
max_background_loops = 2
bus_reached_end = False

background_image = pygame.image.load('images/mountain.png') 
background_image1 = pygame.image.load('images/trial.png') 
background_width2 = background_image.get_width()
background_width = background_image1.get_width()

background_scroll_speed2 = 1
background_scroll_speed = 11 
bg_x1 = 0
bg_x2 = background_width 

bg_x1_image = 0
bg_x2_image = background_width2


# PHASE 10 

Okay_botton_rect = pygame.Rect(400, 90, 80, 50)
okay_botton_image = pygame.image.load('images/okay.png')
phase10_start_time = None


# PHASE 11

Ending_rect = pygame.Rect(450, 270, 100, 100)


# 12 LOOP CONDITION

Exit_rect = pygame.Rect(100, 470, 100, 100)
Exit_image = pygame.image.load('images/quit.png')


main_menu_music = pygame.mixer.Sound("Music/menu.mp3")
game_music = pygame.mixer.Sound("Music/game.mp3")
end_music = pygame.mixer.Sound("Music/end.mp3")

def main_menu():
    global current_phase

    main_menu_music.play(-1) 

    # Colors
    white = (255, 255, 255)
    black = (0, 0, 0)

    # Fonts
    font = pygame.font.Font(None, 48)

    # Buttons
    start_button = pygame.Rect(360, 250, 300, 80)
    exit_button = pygame.Rect(360, 350, 300, 80)

    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    
    

    # Main Menu Loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    current_phase = 'spawning'  
                    running = False  
                if exit_button.collidepoint(event.pos):
                    pygame.quit()  # Quit Pygame
                    exit()

        # Fill the screen
        win.fill(white)  

        # Draw buttons
        pygame.draw.rect(win, black, start_button)
        pygame.draw.rect(win, black, exit_button)

        # Draw text
        draw_text("Start", font, white, win, start_button.centerx - 50, start_button.centery - 15)
        draw_text("Exit", font, white, win, exit_button.centerx - 40, exit_button.centery - 15)
        
        pygame.display.update()
        
    main_menu_music.stop()




def updateGameWindow():
    global walkCount, game_music_playing, current_phase, bg_x1, bg_x2, bg_x1_image, bg_x2_image, bus_reached_end, background_loop_count, phase10_start_time
    
    if current_phase == -1:
        main_menu()
    
    if current_phase == 'spawning':
        game_music.play(-1)  
        game_music_playing = True
        win.blit(bg_spawning, (0, 0))
        char_current = pygame.transform.scale(char, (100, 120))
        walkLeft_current = [pygame.transform.scale(img, (100, 120)) for img in walkLeft]
        walkRight_current = [pygame.transform.scale(img, (100, 120)) for img in walkRight]
        walkUp_current = [pygame.transform.scale(img, (100, 120)) for img in walkUp]
        walkDown_current = [pygame.transform.scale(img, (100, 120)) for img in walkDown]
        if not objective_completed:
            pygame.draw.rect(win, (255, 255, 255), spawn_text_rect)
            win.blit(bag_image, spawn_objective_rect)
            font = pygame.font.Font(None, 48)
            feedback_text = "GRAB YOUR BAG"
            feedback_color = (0, 0, 139)
            text = font.render(feedback_text, True, feedback_color)
            win.blit(text, (40, 100))
    else:
        if current_phase == 1:
            win.blit(bg_phase1, (0, 0))
            font = pygame.font.Font(None, 48)
            feedback_text = "GO RIGHT ------>"
            feedback_color = (0, 255, 0)
            text = font.render(feedback_text, True, feedback_color)
            win.blit(text, (200, 100))
        elif current_phase == 2:
            win.blit(bg_phase2, (0, 0))
            if not phase2_task_completed:
                win.blit(dog_frames[current_dog_frame], phase2_objective_rect.move(75, 0))
                win.blit(cat_frames[current_cat_frame], phase2_objective_rect) 
                font = pygame.font.Font(None, 40)
                feedback_text = "SEPARATE THE DOG AND CAT"
                feedback_color = (0, 255, 0)
                text = font.render(feedback_text, True, feedback_color)
                win.blit(text, (470, 70))
        elif current_phase == 3:
            win.blit(bg_phase3, (0, 0))
            phase3_task_rect = pygame.Rect(200, 200, 650, 50)
            pygame.draw.rect(win, (0, 0, 0), phase3_task_rect)
            win.blit(grandma_image, grandma_rect)

            font = pygame.font.Font(None, 48)
            feedback_text = "HELP THE GRANNY CROSS THE ROAD"
            feedback_color = (0, 255, 0)
            text = font.render(feedback_text, True, feedback_color)
            win.blit(text, (205, 210))

        elif current_phase == 4:
            win.blit(bg_phase4, (0, 0))
            if not phase4_task_completed:
                win.blit(beggar_image, phase4_beggar_rect)
                phase4_task_rect = pygame.Rect(190, 90, 440, 50)
                pygame.draw.rect(win, (0, 0, 0), phase4_task_rect)
                font = pygame.font.Font(None, 48)
                feedback_text = "GIVE FOOD TO A BEGGAR"
                feedback_color = (0, 255, 0)
                text = font.render(feedback_text, True, feedback_color)
                win.blit(text, (200, 100))
        elif current_phase == 5:
            win.blit(bg_phase5, (0, 0))
            for i, rect in enumerate(pedestrian_sign_rect):
                win.blit(pedestrian_image[i], rect)
        elif current_phase == 6:
            win.blit(bg_phase6, (0, 0))
            if traffic_light_color == "red":
                pygame.draw.circle(win, (0, 0, 0), traffic_light_center, traffic_light_radius)
            else:
                pygame.draw.circle(win, (0, 0, 0), traffic_light_center1, traffic_light_radius2)
            win.blit(phase6_car_image, car_rect)
            win.blit(phase6_car_image2, car_rect2)
            font = pygame.font.Font(None, 48)
            feedback_text1 = 'WAIT FOR THE LIGHT TO TURN'
            feedback_text2 = '"GREEN"'
            feedback_color1 = (0, 0, 0)
            feedback_color2 = (0, 255, 0)
            text1 = font.render(feedback_text1, True, feedback_color1)
            text2 = font.render(feedback_text2, True, feedback_color2)
            position1 = (50, 40)
            position2 = (570, 40)
            win.blit(text1, position1)
            win.blit(text2, position2)
            pygame.draw.rect(win, (0, 0, 0), text_rect)
        elif current_phase == 7:
            win.blit(bg_phase7, (0, 0))
            win.blit(sit_down_image, sit_down_rect)

            font = pygame.font.Font(None, 30)
            feedback_text = "SIT HERE"
            feedback_color = (0, 255, 0)
            text = font.render(feedback_text, True, feedback_color)
            win.blit(text, (860, 260))
        elif current_phase == 8:
            win.blit(bg_phase8, (0, 0))
        elif current_phase == 9:
            win.blit(background_image, (bg_x1_image, 0))
            win.blit(background_image, (bg_x2_image, 0))
            win.blit(background_image1, (bg_x1, 280))
            win.blit(background_image1, (bg_x2, 280))
            win.blit(bus_image, phase9_bus_rect)

            bg_x1_image -= background_scroll_speed2
            bg_x2_image -= background_scroll_speed2

            bg_x1 -= background_scroll_speed
            bg_x2 -= background_scroll_speed

            if bg_x1 <= -background_width:
                bg_x1 = bg_x2 + background_width  
                background_loop_count += 1 
            # Check if the second background has moved off-screen
            if bg_x2 <= -background_width:
                bg_x2 = bg_x1 + background_width 
                background_loop_count += 1  # Increment the loop count

            # Check if the first background has moved off-screen
            if bg_x1_image <= -background_width2:
                bg_x1_image = bg_x2_image + background_width2  # Position the first background just after the second
            # Check if the second background has moved off-screen
            if bg_x2_image <= -background_width2:
                bg_x2_image = bg_x1_image + background_width2  # Position the second background just after the first

            if background_loop_count == max_background_loops:
                bus_reached_end = True
        elif current_phase == 10:
            win.blit(bg_phase10, (0, 0))
            font = pygame.font.Font(None, 48)
            feedback_text = "ARRIVED!"
            feedback_color = (0, 255, 0)
            text = font.render(feedback_text, True, feedback_color)
            win.blit(text, (200, 100))
            if phase10_start_time is None:
                phase10_start_time = time.time() 
            elif time.time() - phase10_start_time >= 3:  # Check if 3 seconds have passed
                win.blit(okay_botton_image, Okay_botton_rect)
                
        elif current_phase == 11:
            win.blit(bg_phase11, (0, 0))
            
        elif current_phase == 12:
            game_music.stop()
            end_music.play()
            game_music_playing = True
            win.blit(bg_phase12, (0, 0))
            win.blit(Exit_image, Exit_rect)
        
        char_current = char
        walkLeft_current = walkLeft
        walkRight_current = walkRight
        walkUp_current = walkUp
        walkDown_current = walkDown

    if walkCount + 1 >= 12:
        walkCount = 0

    if current_phase != 9 and current_phase != 10:
        if left:
            win.blit(walkLeft_current[walkCount // 3], (x, y))
            walkCount += 1
        elif right:
            win.blit(walkRight_current[walkCount // 3], (x, y))
            walkCount += 1
        elif up:
            win.blit(walkUp_current[walkCount // 3], (x, y))
            walkCount += 1
        elif down:
            win.blit(walkDown_current[walkCount // 3], (x, y))
            walkCount += 1
        else:
            win.blit(char_current, (x, y))

    pygame.display.update()

def transition_to_task_screen():
    global task_screen
    win.fill((0, 0, 0))  # Black screen
    pygame.display.update()
    pygame.time.delay(500)  # Delay transition effect
    task_screen = True

def start_new_phase():
    global current_phase, x, y, left, right, up, down, background_loop_count, bus_reached_end, phase10_start_time

    if current_phase == 8:
        fade(win, screen_width, screen_height, fade_out=True)

    if current_phase == 9:
        fade(win, screen_width, screen_height, fade_out=True)

    if current_phase == 11:
        fade(win, screen_width, screen_height, fade_out=True)

    if current_phase == 'spawning':
        current_phase = 1
    elif current_phase == 1:
        current_phase = 2
    elif current_phase == 2:
        current_phase = 3
    elif current_phase == 3:
        current_phase = 4
    elif current_phase == 4:
        current_phase = 5
    elif current_phase == 5:
        current_phase = 6
    elif current_phase == 6:
        current_phase = 7
    elif current_phase == 7:
        current_phase = 8
    elif current_phase == 8:
        current_phase = 9
    elif current_phase == 9:
        bus_reached_end = True
        current_phase = 10
        background_loop_count = 0 
        phase10_start_time = None 
        # Reset bus_reached_end flag for next phase
    elif current_phase == 10:
        current_phase = 11
    elif current_phase == 11:
        current_phase = 12

    elif current_phase > 2:
        current_phase += 1


    x, y = initial_positions[current_phase] 

    # Reset movement flags
    left = False
    right = False
    up = False
    down = False

def fade(win, width, height, fade_out=True):
    fade_surface = pygame.Surface((width, height))
    fade_surface.fill((0, 0, 0))
    alpha_range = range(0, 100) if fade_out else range(300, -1, -1) 
    for alpha in alpha_range:
        fade_surface.set_alpha(alpha)
        win.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(30)

def is_restricted(new_x, new_y):
    char_rect = pygame.Rect(new_x, new_y, char.get_width(), char.get_height())
    for area in restricted_areas:
        if char_rect.colliderect(area):
            return True
    return False


game_music_playing = False  # Flag to track if game music is playing
current_phase = -1

# Main loop
run = True

while run:
    clock.tick(27)

    # Update the phase2 animation
    phase2_update_animation()

    # Adjust the speed based on whether the player is holding the grandma
    if holding_grandma:
        vel = slow_vel
    else:
        vel = 10

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if task_screen:
                if current_phase == 5:
                    for i, rects in enumerate(signage_questions_rect):
                        if rects.collidepoint(event.pos):
                            if i == correct_signage_index:
                                right_indicator = True
                                feedback_displayed = True

                            else:
                                wrong_indicator = True
                                feedback_displayed = True
                                x, y = initial_positions[current_phase]

                            # Display feedback for a short duration and then exit the task screen
                            pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1 second timer

                elif current_phase == 7:
                    for i, rect in enumerate(signages_rect):
                        if rect.collidepoint(event.pos):
                            if i == correct_answer_index:
                                phase_7right_indicator = True
                                feedback_displayed = True

                            else:
                                wrong_indicator = True
                                feedback_displayed = True

                            # Display feedback for a short duration and then exit the task screen
                            pygame.time.set_timer(pygame.USEREVENT, 2000)  # 1 second timer

                elif current_phase == 2 and not phase2_task_completed:
                    if dog_rect.collidepoint(event.pos):
                        dragging_animal = 'dog'
                        offset_x = dog_rect.x - event.pos[0]
                    elif cat_rect.collidepoint(event.pos):
                        dragging_animal = 'cat'
                        offset_x = cat_rect.x - event.pos[0]

                elif current_phase == 4 and not phase4_task_completed:
                    for item in food_items:
                        if item['rect'].collidepoint(event.pos) and not item['completed']:
                            dragging = item
                            mouse_x, mouse_y = event.pos
                            offset_x = item['rect'].x - mouse_x
                            offset_y = item['rect'].y - mouse_y

                else:
                    for obj in things_to_bring:
                        if obj['rect'].collidepoint(event.pos) and not obj['completed']:
                            dragging = obj
                            mouse_x, mouse_y = event.pos
                            offset_x = obj['rect'].x - mouse_x
                            offset_y = obj['rect'].y - mouse_y

            elif current_phase == 'spawning' and not objective_completed and spawn_objective_rect.collidepoint(event.pos):
                if abs(x - spawn_objective_rect.x) < 60 and abs(y - spawn_objective_rect.y) < 140:
                    transition_to_task_screen()
            elif current_phase == 2 and not phase2_task_completed and phase2_objective_rect.collidepoint(event.pos):
                if abs(x - phase2_objective_rect.x) < 100 and abs(y - phase2_objective_rect.y) < 500:
                    transition_to_task_screen()
            elif current_phase == 3 and grandma_rect.collidepoint(event.pos):
                holding_grandma = True
            elif current_phase == 4 and not phase4_task_completed and phase4_beggar_rect.collidepoint(event.pos):
                if abs(x - phase4_beggar_rect.x) < 50 and abs(y - phase4_beggar_rect.y) < 50:
                    transition_to_task_screen()
            elif current_phase == 7 and sit_down_rect.collidepoint(event.pos):
                if abs(x - sit_down_rect.x) < 50 and abs(y - sit_down_rect.y) < 50:
                    transition_to_task_screen()
            elif current_phase == 10 and Okay_botton_rect.collidepoint(event.pos):
                start_new_phase() 
            elif current_phase == 12 and Exit_rect.collidepoint(event.pos):
                if abs(x - Exit_rect.x) < 50 and abs(y - Exit_rect.y) < 50:
                    exit()

        elif event.type == pygame.MOUSEBUTTONUP:
            if task_screen:
                if current_phase == 2 and dragging_animal:
                    dragging_animal = None
                elif current_phase == 4 and dragging:
                    if beggar_task_rect.contains(dragging['rect']):
                        if food_items.index(dragging) == correct_item_index:
                            dragging['completed'] = True
                        else:
                            # reset the position if its the wrong item
                            dragging['rect'].topleft = dragging['initial_pos']
                    else:
                        dragging['rect'].topleft = dragging['initial_pos']
                    dragging = None
                elif current_phase == 'spawning' and dragging:
                    if large_obj_rect.contains(dragging['rect']):
                        dragging['completed'] = True
                    else:
                        # reset the position if its the wrong item
                        dragging['rect'].topleft = dragging['initial_pos']
                    dragging = None

            if current_phase == 3:
                holding_grandma = False

        elif event.type == pygame.USEREVENT:
            if feedback_displayed:
                feedback_displayed = False
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Stop the timer

                if right_indicator:
                    phase5_task_completed = True
                task_screen = False

                if phase_7right_indicator:
                    current_phase = 8
                    x, y = initial_positions[current_phase]

        elif event.type == pygame.MOUSEMOTION:
            if task_screen:
                if current_phase == 2 and dragging_animal:
                    mouse_x = event.pos[0]
                    if dragging_animal == 'dog':
                        dog_rect.x = mouse_x + offset_x
                    elif dragging_animal == 'cat':
                        cat_rect.x = mouse_x + offset_x
                elif current_phase == 'spawning' and dragging:
                    mouse_x, mouse_y = event.pos
                    dragging['rect'].x = mouse_x + offset_x
                    dragging['rect'].y = mouse_y + offset_y
                elif current_phase == 4 and dragging:
                    mouse_x, mouse_y = event.pos
                    dragging['rect'].x = mouse_x + offset_x
                    dragging['rect'].y = mouse_y + offset_y

    keys = pygame.key.get_pressed()

    # Movement logic
    if current_phase == 'spawning':
        if not task_screen:
            if keys[pygame.K_a] and x > 0:
                new_x = x - vel
                if not is_restricted(new_x, y):
                    x = new_x
                left = True
                right = False
            elif keys[pygame.K_d] and x < screen_width - char.get_width():
                new_x = x + vel
                if not is_restricted(new_x, y):
                    x = new_x
                right = True
                left = False
            else:
                right = False
                left = False

            if keys[pygame.K_w] and y > 0:
                new_y = y - vel
                if not is_restricted(x, new_y):
                    y = new_y
                up = True
                down = False
            elif keys[pygame.K_s] and y < screen_height - char.get_height():
                new_y = y + vel
                if not is_restricted(x, new_y):
                    y = new_y
                down = True
                up = False
            else:
                up = False
                down = False

            # Check if character has reached the bottom of the screen to transition to phase 1
            if y >= screen_height - char.get_height() and objective_completed:  
                start_new_phase()
            elif y >= screen_height - char.get_height() and not objective_completed:
                y = screen_height - char.get_height() - 1

    elif current_phase == 3:
        if keys[pygame.K_a] and x > 0:
            x -= vel
            left = True
            right = False
        elif keys[pygame.K_d] and x < screen_width - char.get_width():
            x += vel
            right = True
            left = False
        else:
            right = False
            left = False

        if keys[pygame.K_a] and holding_grandma and x > 0:
            grandma_rect.x = x + char.get_width() // 2 - grandma_rect.width // 2
        elif keys[pygame.K_d] and holding_grandma and x < screen_width - char.get_width():
            grandma_rect.x = x + char.get_width() // 2 - grandma_rect.width // 2

        if holding_grandma and abs(x - grandma_rect.x) > 50: 
            holding_grandma = False  # Stop holding the grandma

        if holding_grandma and grandma_rect.x > 700 and x > 700:
            phase3_task_completed = True
            holding_grandma = False
        
        if x >= screen_width - char.get_width() and phase3_task_completed:  
            start_new_phase()
        elif x >= screen_width - char.get_width() and not phase3_task_completed:
            x = screen_width - char.get_width() - 1

    elif current_phase == 6:
        update_traffic_light()  # Update the traffic light state
        phase6_moving_car()  # Move the car

        Player_rect = player_rect = pygame.Rect(x, y, 100, 80)

        if not task_screen:
            if keys[pygame.K_w] and y > phase6_upper_boundary:
                y -= walk_vel  # Subtract vel from y to move up
                up = True
                down = False
            elif keys[pygame.K_s] and y < screen_height - char.get_height():
                y += walk_vel  # Add vel to y to move down
                down = True
                up = False
            else:
                up = False
                down = False

            if Player_rect.colliderect(car_rect) or Player_rect.colliderect(car_rect2):
                # Reset to initial position if colliding with car on red light
                x, y = initial_positions[current_phase]
                reset_car_position()
    
            if y >= screen_height - char.get_height():
                if traffic_light_color == "green":
                    phase6_task_completed = True
                    start_new_phase()
                else:
                    y = screen_height - char.get_height() - 1

    elif current_phase == 11:
        if keys[pygame.K_w] and y > 0 :
            y -= vel
            up = True
            down = False
        elif keys[pygame.K_s]:
            y += vel
            down = True
            up = False

        elif current_phase == 11 and y >= screen_height - char.get_height():
                y = screen_height - char.get_height() - 1
        else:
            up = False
            down = False

        if current_phase == 11:
                Player_rect = player_rect = pygame.Rect(x, y, 20, 20)
                if Player_rect.colliderect(Ending_rect):
                    start_new_phase()
                    
    else:
        if keys[pygame.K_a] and x > 0:
            x -= vel
            left = True
            right = False
        elif keys[pygame.K_d]:
            x += vel
            right = True
            left = False
            if current_phase == 1 and x > screen_width:
                start_new_phase()
            elif current_phase == 2 and x >= screen_width - char.get_width() and not phase2_task_completed:
                x = screen_width - char.get_width() - 1  # Preventing moving further right     
            elif current_phase == 4 and x >= screen_width - char.get_width() and not phase4_task_completed:
                x = screen_width - char.get_width() - 1
            elif current_phase == 5 and x >= 180 and not phase5_task_completed:
                transition_to_task_screen()
            elif current_phase == 7 and x >= screen_width - char.get_width():
                x = screen_width - char.get_width() - 1
            elif current_phase == 8:
                Player_rect = player_rect = pygame.Rect(x, y, 20, 20)
                if Player_rect.colliderect(phase8_rect):
                    start_new_phase()
            elif current_phase == 12 and x >= screen_width - char.get_width():
                x = screen_width - char.get_width() - 1
            

            
        elif x > screen_width:
            start_new_phase()
        elif current_phase == 9 and bus_reached_end:
            start_new_phase()
        else:
            right = False
            left = False

    if task_screen:
        if current_phase == 2:
            perform_phase2_task()
        elif current_phase == 4:
            perform_phase4_task()
        elif current_phase == 5:
            perform_phase5_task()
        elif current_phase == 7:
            perform_phase7_task()
        else:
            perform_spawn_task()
    else:
        updateGameWindow()

pygame.mixer.quit()
pygame.quit()