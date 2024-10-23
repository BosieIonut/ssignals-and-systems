import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 1000  # Adjust width to have more space for the plot on the right
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Spring parameters
spring_anchor = (WIDTH // 4, 50)  # Adjust anchor to keep it on the left side
mass_radius = 20
spring_length = 200  # Rest length of the spring
spring_k = 0.05  # Spring constant
damping = 0.85  # Damping factor to simulate friction

# Initial conditions
initial_displacement = 0  # Initial displacement from the equilibrium position
initial_velocity = 0  # Initial velocity (e.g., upwards)

# Set initial position of the mass based on displacement
mass_pos = [WIDTH // 4, spring_anchor[1] + spring_length + initial_displacement]

# Set initial velocity
velocity = initial_velocity

# For the real-time plot
position_history = []  # List to store the position over time
input_history = []
history_length = 450  # How many points to display on the plot
fixed_y_range = (100, 500)  # Fixed y-axis range for the plot

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Smooth gravity
gravity = 0
paused = False
index = 0
def draw_hs_rectangle_with_arrows(surface, rect_pos, rect_size):
    # Draw the rectangle
    pygame.draw.rect(surface, GRAY, (rect_pos[0], rect_pos[1], rect_size[0], rect_size[1]))
    
    # Draw the text "H(s)" inside the rectangle
    font = pygame.font.Font(None, 36)
    text = font.render("H(s)", True, BLACK)
    text_rect = text.get_rect(center=(rect_pos[0] + rect_size[0] // 2, rect_pos[1] + rect_size[1] // 2))
    surface.blit(text, text_rect)

    # Draw arrow from left to rectangle
    start_pos = (rect_pos[0] - 60, rect_pos[1] + rect_size[1] // 2)  # Start point of the arrow
    end_pos = (rect_pos[0] - 5, rect_pos[1] + rect_size[1] // 2)  # End point of the arrow
    pygame.draw.line(surface, BLACK, start_pos, end_pos, 5)  # Draw line

    # Position for u(t) text
    u_t_text = font.render("u(t)", True, BLACK)
    u_t_rect = u_t_text.get_rect(center=(start_pos[0] + 25, start_pos[1] - 25))
    surface.blit(u_t_text, u_t_rect)

    start_pos = (start_pos[0] + 10, start_pos[1])
    end_pos = (end_pos[0] + 10, end_pos[1])
    pygame.draw.polygon(surface, BLACK, [(end_pos[0], end_pos[1]), (end_pos[0] - 10, end_pos[1] - 5), (end_pos[0] - 10, end_pos[1] + 5)])  # Draw arrowhead

    # Draw arrow from rectangle to the right
    start_pos = (rect_pos[0] + rect_size[0], rect_pos[1] + rect_size[1] // 2)  # Start point of the arrow
    end_pos = (start_pos[0] + 50, start_pos[1])  # End point of the arrow
    pygame.draw.line(surface, BLACK, start_pos, end_pos, 5)  # Draw line

    # Position for y(t) text
    y_t_text = font.render("y(t)", True, BLACK)
    y_t_rect = y_t_text.get_rect(center=(start_pos[0] + 25, start_pos[1] - 25))
    surface.blit(y_t_text, y_t_rect)

    start_pos = (start_pos[0] + 10, start_pos[1])
    end_pos = (end_pos[0] + 10, end_pos[1])
    pygame.draw.polygon(surface, BLACK, [(end_pos[0], end_pos[1]), (end_pos[0] - 10, end_pos[1] - 5), (end_pos[0] - 10, end_pos[1] + 5)])  # Draw arrowhead



    
def draw_position_plot(surface, history, current_y):
    # Define plot area (on the right side)
    plot_rect = pygame.Rect(WIDTH - 500, 100, 450, 400)  # Moved to the right side
    pygame.draw.rect(surface, BLACK, plot_rect, 2)

    # Draw the "Output: y(t)" text on top of the plot
    font = pygame.font.SysFont(None, 24)  # Create a font object
    output_text = font.render('Output: y(t)', True, BLACK)  # Render the text
    surface.blit(output_text, (plot_rect.x + 5, plot_rect.y + 5))  # Positioning the text

    # Normalize position history to fit in the plot area based on a fixed y-range
    min_pos, max_pos = fixed_y_range
    range_pos = max_pos - min_pos

    # Scale history to fit the plot area (without flipping)
    scaled_history = history
    # Plot points as a connected line
    for i in range(1, len(scaled_history)):
        pygame.draw.line(
            surface,
            GREEN,
            (plot_rect.x + i - 1, scaled_history[i - 1]),
            (plot_rect.x + i, scaled_history[i]),
            2,
        )

    plot_x = plot_rect.x + len(scaled_history)

    # Draw the horizontal line
    pygame.draw.line(surface, GRAY, (mass_pos[0], current_y), (plot_x + 1, current_y), 1)  # Dotted horizontal line

def draw_input_plot(surface, history, current_y):
    # Define plot area (on the right side)
    plot_rect = pygame.Rect(WIDTH - 500, 550, 450, 400)  # Moved to the right side
    pygame.draw.rect(surface, BLACK, plot_rect, 2)

    # Draw the "Output: y(t)" text on top of the plot
    font = pygame.font.SysFont(None, 24)  # Create a font object
    output_text = font.render('Input: u(t)', True, BLACK)  # Render the text
    surface.blit(output_text, (plot_rect.x + 5, plot_rect.y + 5))  # Positioning the text

    # Normalize position history to fit in the plot area based on a fixed y-range
    min_pos, max_pos = fixed_y_range
    range_pos = max_pos - min_pos

    # Scale history to fit the plot area (without flipping)
    scaled_history = history
    # Plot points as a connected line
    for i in range(1, len(scaled_history)):
        pygame.draw.line(
            surface,
            GREEN,
            (plot_rect.x + i - 1, scaled_history[i - 1]),
            (plot_rect.x + i, scaled_history[i]),
            2,
        )

    plot_x = plot_rect.x + len(scaled_history)

    # Draw the horizontal line
    pygame.draw.line(surface, GRAY, (mass_pos[0], current_y), (plot_x + 1, current_y), 1)  # Dotted horizontal line

# Function to draw a downward arrow
def draw_downward_arrow(surface, position):
    arrow_length = 30  # Doubled length of the arrow shaft
    arrow_width = 5  # Width of the arrowhead
    arrow_base = (position[0], position[1] + mass_radius)  # Base of the arrow at the mass's bottom

    # Draw the shaft
    pygame.draw.line(surface, BLACK, arrow_base, (arrow_base[0], arrow_base[1] + arrow_length), 2)

    # Draw the arrowhead
    pygame.draw.polygon(surface, BLACK, [
        (arrow_base[0] - arrow_width, arrow_base[1] + arrow_length),
        (arrow_base[0] + arrow_width, arrow_base[1] + arrow_length),
        (arrow_base[0], arrow_base[1] + arrow_length + arrow_width)
    ])

    # Draw the letter "u" to the left of the arrow
    font = pygame.font.SysFont(None, 24)  # Create a font object
    text_surface = font.render('u', True, BLACK)  # Render the letter "u"
    text_position = (arrow_base[0] - 20, arrow_base[1] + arrow_length // 2)  # Position of the text
    surface.blit(text_surface, text_position)  # Draw the text on the surface
# Function to draw the square output plot

running = True
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Space to pause
                paused = not paused
            if event.key == pygame.K_r:  # 'r' key to reset
                mass_pos = [WIDTH // 4, spring_anchor[1] + spring_length + initial_displacement]
                velocity = initial_velocity
                gravity = 0
                index = 0
                position_history.clear()

    # Skip the update and drawing steps when paused
    if not paused:
        index += 1
        if index > 50 and index < 250:
            gravity = 6
            ## HERE PLOT A LITTLE DOWN ARROW NEXT TO THE MASS
            draw_downward_arrow(screen, (mass_pos[0], mass_pos[1]))  # Draw downward arrow next to the mass
        else:
            gravity = 0
        # Calculate the spring force (Hooke's law)
        displacement = mass_pos[1] - (spring_anchor[1] + spring_length)
        spring_force = -spring_k * displacement

        # Add gravity
        total_force = spring_force + gravity

        # Update acceleration, velocity, and position
        acceleration = total_force
        velocity += acceleration
        velocity *= damping  # Apply damping to slow down over time
        mass_pos[1] += velocity

        # Limit spring stretch (not letting the mass go below the screen)
        if mass_pos[1] > HEIGHT - mass_radius:
            mass_pos[1] = HEIGHT - mass_radius
            velocity = 0

        # Keep track of the mass position for plotting
        if len(position_history) < history_length:
            position_history.append(mass_pos[1])
            input_history.append(gravity * 10 + 250 + 550)

        # Draw the spring (a simple line) and the mass (a circle)
        pygame.draw.line(screen, BLUE, spring_anchor, mass_pos, 3)  # Spring
        pygame.draw.circle(screen, RED, (int(mass_pos[0]), int(mass_pos[1])), mass_radius)  # Mass

        # Draw the real-time plot of position (on the right side)
        draw_position_plot(screen, position_history, mass_pos[1])
        draw_input_plot(screen, input_history,gravity)
        draw_hs_rectangle_with_arrows(screen, (150, 700), (200, 100))
        # Display speed, acceleration, and velocity in the left corner
        font = pygame.font.SysFont(None, 24)
        speed_text = font.render(f'Speed: {velocity:.2f}', True, BLACK)
        acceleration_text = font.render(f'Acceleration: {acceleration:.2f}', True, BLACK)
        velocity_text = font.render(f'Position: {int(mass_pos[1]) - 250:.2f}', True, BLACK)
        screen.blit(speed_text, (10, 10))
        screen.blit(acceleration_text, (10, 30))
        screen.blit(velocity_text, (10, 50))

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit pygame
pygame.quit()
