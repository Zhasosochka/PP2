import pygame
import math

def main():
    pygame.init()

    # Window setup
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint - Extended Shapes")
    clock = pygame.time.Clock()

    BG_COLOR = (0, 0, 0)

    # Permanent surface to store the drawing (persistent data)
    canvas = pygame.Surface(screen.get_size())
    canvas.fill(BG_COLOR)

    # Initial state variables
    radius = 5
    drawing = False
    start_pos = None
    current_pos = None

    tool = "brush"
    color = (0, 0, 255)

    last_pos = None
    font = pygame.font.SysFont("Verdana", 15)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                # Color selection (R, G, B, White, Yellow)
                if event.key == pygame.K_r: color = (255, 0, 0)
                elif event.key == pygame.K_g: color = (0, 255, 0)
                elif event.key == pygame.K_b: color = (0, 0, 255)
                elif event.key == pygame.K_w: color = (255, 255, 255)
                elif event.key == pygame.K_y: color = (255, 255, 0)

                # Tool selection via number keys
                elif event.key == pygame.K_1: tool = "brush"
                elif event.key == pygame.K_2: tool = "rect"
                elif event.key == pygame.K_3: tool = "circle"
                elif event.key == pygame.K_4: tool = "eraser"
                elif event.key == pygame.K_5: tool = "square"
                elif event.key == pygame.K_6: tool = "right_triangle"
                elif event.key == pygame.K_7: tool = "equilateral_triangle"
                elif event.key == pygame.K_8: tool = "rhombus"

                # Adjust brush/eraser thickness
                elif event.key == pygame.K_UP: radius = min(50, radius + 1)
                elif event.key == pygame.K_DOWN: radius = max(1, radius - 1)

                # Reset the canvas to background color
                elif event.key == pygame.K_c: canvas.fill(BG_COLOR)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                drawing = True
                start_pos = event.pos
                current_pos = event.pos
                last_pos = event.pos # Track position for continuous brush strokes

                # Instant draw for single click tools
                if tool == "brush":
                    pygame.draw.circle(canvas, color, event.pos, radius)
                elif tool == "eraser":
                    pygame.draw.circle(canvas, BG_COLOR, event.pos, radius)

            if event.type == pygame.MOUSEMOTION:
                current_pos = event.pos
                if drawing:
                    # Continuous line drawing for brush/eraser
                    if tool == "brush":
                        draw_line(canvas, color, last_pos, event.pos, radius)
                        last_pos = event.pos
                    elif tool == "eraser":
                        draw_line(canvas, BG_COLOR, last_pos, event.pos, radius)
                        last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing:
                    # Save the final shape to the permanent canvas surface
                    draw_shape(canvas, tool, color, start_pos, event.pos)
                drawing = False
                start_pos = None

        # Redraw the screen
        screen.fill(BG_COLOR)
        screen.blit(canvas, (0, 0)) # Display the saved drawing

        # Show "ghost" preview of the shape while dragging
        if drawing and start_pos and current_pos:
            draw_shape(screen, tool, color, start_pos, current_pos)

        # --- UI Rendering ---
        status_text = font.render(f"Tool: {tool.capitalize()} (Size: {radius})", True, (255, 255, 255))
        info_line1 = font.render("1:Brush 2:Rect 3:Circle 4:Eraser 5:Square 6:RightTri 7:EquiTri 8:Rhombus", True, (255, 255, 255))
        info_line2 = font.render("R G B W Y:Colors | UP/DOWN:Size | C:Clear", True, (255, 255, 255))

        screen.blit(status_text, (10, 10))
        screen.blit(info_line1, (10, 440))
        screen.blit(info_line2, (10, 460))

        pygame.display.flip() # Update the full display Surface to the screen
        clock.tick(60) # Limit frame rate to 60 FPS

# --- HELPER FUNCTIONS ---

def draw_shape(surface, tool, color, start, end):
    # Map tool names to specific drawing functions
    if tool == "rect": draw_rectangle(surface, color, start, end)
    elif tool == "circle": draw_circle(surface, color, start, end)
    elif tool == "square": draw_square(surface, color, start, end)
    elif tool == "right_triangle": draw_right_triangle(surface, color, start, end)
    elif tool == "equilateral_triangle": draw_equilateral_triangle(surface, color, start, end)
    elif tool == "rhombus": draw_rhombus(surface, color, start, end)

def draw_line(surface, color, start, end, width):
    # Interpolates points between mouse positions to avoid "dotted" lines
    dx, dy = end[0] - start[0], end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance + 1):
        x = int(start[0] + dx * i / distance)
        y = int(start[1] + dy * i / distance)
        pygame.draw.circle(surface, color, (x, y), width)

def draw_rectangle(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end
    # Construct a Rect object with correct top-left coordinates
    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))
    pygame.draw.rect(surface, color, rect, 2)

def draw_circle(surface, color, start, end):
    # Use Pythagorean theorem for radius calculation
    radius = int(math.sqrt((end[0]-start[0])**2 + (end[1]-start[1])**2))
    pygame.draw.circle(surface, color, start, radius, 2)

def draw_square(surface, color, start, end):
    x1, y1 = start
    side = max(abs(end[0] - x1), abs(end[1] - y1))
    # Determine direction of mouse movement (quadrants)
    sign_x = 1 if end[0] > x1 else -1
    sign_y = 1 if end[1] > y1 else -1
    rect = pygame.Rect(x1 if sign_x > 0 else x1 - side,
                        y1 if sign_y > 0 else y1 - side,
                        side, side)
    pygame.draw.rect(surface, color, rect, 2)

def draw_right_triangle(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, 2)

def draw_equilateral_triangle(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end
    base = x2 - x1
    height = base * (math.sqrt(3) / 2) # Geometric height formula
    points = [
        ((x1 + x2) / 2, y1), # Top vertex
        (x1, y1 + height),   # Bottom left
        (x2, y1 + height)    # Bottom right
    ]
    pygame.draw.polygon(surface, color, points, 2)

def draw_rhombus(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    # Vertices at center-points of the bounding box sides
    points = [
        (mid_x, y1), # Top
        (x1, mid_y), # Left
        (mid_x, y2), # Bottom
        (x2, mid_y)  # Right
    ]
    pygame.draw.polygon(surface, color, points, 2)

main()