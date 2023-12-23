# Import pygame, pyttsx3, math and pygame_gui modules
import pygame, pyttsx3, math, pygame_gui

# Initialize pygame and create a screen
pygame.init()
screen = pygame.display.set_mode((640, 480))

# Define some colors and constants
back = (255, 255, 255) # White background
color = (255, 255, 0) # Yellow face
black = (0, 0, 0) # Black eyes and mouth
PI = math.pi # Pi constant

# Initialize pyttsx3 and set the voice and rate
engine = pyttsx3.init()
engine.setProperty('voice', 'en')
engine.setProperty('rate', 150)

# Define a function to draw a circle with an outline
def draw_circle(surface, x, y, radius, color, width):
    pygame.draw.circle(surface, color, (x, y), radius)
    pygame.draw.circle(surface, black, (x, y), radius, width)

# Define a function to draw an arc with an outline
def draw_arc(surface, x, y, radius, start_angle, end_angle, color, width):
    pygame.draw.arc(surface, color, (x - radius, y - radius, 2 * radius, 2 * radius), start_angle, end_angle, width)
    pygame.draw.arc(surface, black, (x - radius, y - radius, 2 * radius, 2 * radius), start_angle, end_angle, width + 2)

# Define a function to draw the face
def draw_face(surface, x, y, radius, mouth_angle, mouth_flag):
    # Draw the head
    draw_circle(surface, x, y, radius, color, 4)
    # Draw the eyes
    draw_circle(surface, x - radius // 4, y - radius // 4, radius // 10, black, 0)
    draw_circle(surface, x + radius // 4, y - radius // 4, radius // 10, black, 0)
    # Draw the mouth
    if mouth_flag: # Open mouth
        draw_arc(surface, x, y + radius // 4, radius // 2, mouth_angle, PI - mouth_angle, color, radius // 10)
    else: # Closed mouth
        draw_arc(surface, x, y + radius // 4, radius // 2, mouth_angle, PI - mouth_angle, black, 4)

# Define a function to make the face speak
def speak(text):
    # Split the text into words
    words = text.split()
    # Set the mouth angle and flag
    mouth_angle = PI / 6
    mouth_flag = False
    # Loop through the words
    for word in words:
        # Clear the screen
        screen.fill(back)
        # Draw the face
        draw_face(screen, 320, 240, 100, mouth_angle, mouth_flag)
        # Update the display
        pygame.display.update()
        # Toggle the mouth flag
        mouth_flag = not mouth_flag
        # Say the word
        engine.say(text)
        # Run and wait for the engine
        engine.runAndWait()
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

# Create a User Interface Manager
manager = pygame_gui.UIManager((640, 480))

# Create a label for the text input
text_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((50, 50), (200, 50)),
                                         text='Enter the text to speak:',
                                         manager=manager)

# Create a text entry for the text input
text_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((260, 50), (300, 50)),
                                                 manager=manager)

# Create a button for the speak function
speak_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 120), (100, 50)),
                                            text='Speak',
                                            manager=manager)

# Create a clock
clock = pygame.time.Clock()

# Main loop
running = True
while running:
    # Get the time delta
    time_delta = clock.tick(60)/1000.0
    # Handle events
    for event in pygame.event.get():
        # Quit event
        if event.type == pygame.QUIT:
            running = False
        # User interface event
        if event.type == pygame.USEREVENT:
            # Button pressed event
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # Speak button pressed
                if event.ui_element == speak_button:
                    # Get the text from the text entry
                    text = text_entry.get_text()
                    # Call the speak function
                    speak(text)
        # Pass the event to the manager
        manager.process_events(event)
    # Update the manager
    manager.update(time_delta)
    # Clear the screen
    screen.fill(back)
    # Draw the manager
    manager.draw_ui(screen)
    # Update the display
    pygame.display.update()


# Quit pygame
pygame.quit()
