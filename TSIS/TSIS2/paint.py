import pygame
import datetime
from tools import draw_shape, flood_fill

def main():
    # Initialize all imported pygame modules
    pygame.init()

    # Set up the display window (900px width, 750px height)
    screen = pygame.display.set_mode((900, 750))
    pygame.display.set_caption("Paint - Pro (Zhaslan Edition)")

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # Create the main drawing surface (canvas)
    BG_COLOR = (0, 0, 0)
    canvas = pygame.Surface((900, 600))
    canvas.fill(BG_COLOR)

    # Initial drawing settings
    radius = 5
    drawing = False
    start_pos = None
    last_pos = None

    # Text tool state variables
    typing_text = False
    text_content = ""
    text_pos = (0, 0)

    # Default tool and color
    tool = "brush"
    color = (255, 255, 255)

    # Font settings for UI and Text Tool
    font_small = pygame.font.SysFont("Verdana", 14)
    font_bold = pygame.font.SysFont("Verdana", 16, bold=True)
    text_font = pygame.font.SysFont("Arial", 24)

    # Main application loop
    while True:
        for event in pygame.event.get():
            # Exit the app if the window is closed
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Logic for handling text input when Text Tool is active
            if typing_text:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Draw text onto the permanent canvas
                        render_txt = text_font.render(text_content, True, color)
                        canvas.blit(render_txt, text_pos)
                        typing_text = False
                        text_content = ""
                    elif event.key == pygame.K_ESCAPE:
                        # Cancel text input
                        typing_text = False
                        text_content = ""
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove the last character
                        text_content = text_content[:-1]
                    else:
                        # Add typed character to string
                        text_content += event.unicode
                continue

            # Handle keyboard shortcuts for tools and settings
            if event.type == pygame.KEYDOWN:
                # Tool selection (1-9, F, T)
                if event.key == pygame.K_1: tool = "brush"
                elif event.key == pygame.K_2: tool = "rect"
                elif event.key == pygame.K_3: tool = "circle"
                elif event.key == pygame.K_4: tool = "eraser"
                elif event.key == pygame.K_5: tool = "square"
                elif event.key == pygame.K_6: tool = "right_triangle"
                elif event.key == pygame.K_7: tool = "equilateral_triangle"
                elif event.key == pygame.K_8: tool = "rhombus"
                elif event.key == pygame.K_9: tool = "line"
                elif event.key == pygame.K_f: tool = "fill"
                elif event.key == pygame.K_t: tool = "text"

                # Color selection shortcuts
                elif event.key == pygame.K_r: color = (255, 0, 0)
                elif event.key == pygame.K_g: color = (0, 255, 0)
                elif event.key == pygame.K_b: color = (0, 0, 255)
                elif event.key == pygame.K_w: color = (255, 255, 255)
                elif event.key == pygame.K_y: color = (255, 255, 0)

                # Brush thickness shortcuts
                elif event.key == pygame.K_F1: radius = 2
                elif event.key == pygame.K_F2: radius = 5
                elif event.key == pygame.K_F3: radius = 10

                # Clear the entire canvas
                elif event.key == pygame.K_c: canvas.fill(BG_COLOR)

                # Save canvas as PNG (Ctrl+S)
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    # Generate filename based on current timestamp
                    name = f"paint_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    pygame.image.save(canvas, name)

            # Handle mouse click start
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Only allow drawing if click is within canvas area
                if event.pos[1] < 600:
                    if tool == "fill":
                        # Execute flood fill algorithm
                        flood_fill(canvas, event.pos[0], event.pos[1], canvas.get_at(event.pos), color)
                    elif tool == "text":
                        # Set cursor position for typing
                        typing_text = True
                        text_pos = event.pos
                    else:
                        # Start shape or freehand drawing
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos

            # Handle mouse movement for freehand drawing
            if event.type == pygame.MOUSEMOTION and drawing:
                if tool in ["brush", "eraser"]:
                    # Set drawing color (erase uses background color)
                    draw_color = color if tool == "brush" else BG_COLOR
                    # Connect points with a line for smooth freehand drawing
                    pygame.draw.line(canvas, draw_color, last_pos, event.pos, radius * 2)
                    last_pos = event.pos

            # Handle mouse release to finish shapes
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing and tool not in ["brush", "eraser"]:
                    # Draw the final shape onto the permanent canvas
                    draw_shape(canvas, tool, color, start_pos, event.pos, radius)
                drawing = False

        # Clear the base screen
        screen.fill((30, 30, 30))
        # Draw the current canvas state
        screen.blit(canvas, (0, 0))

        # Show live preview for shapes while dragging
        if drawing and start_pos and tool not in ["brush", "eraser"]:
            draw_shape(screen, tool, color, start_pos, pygame.mouse.get_pos(), radius)

        # Show text preview while typing
        if typing_text:
            screen.blit(text_font.render(text_content + "|", True, color), text_pos)

        # --- UI LEGEND RENDERING ---
        ui_y = 615
        # Current tool/color/size status bar
        status = font_bold.render(f"TOOL: {tool.upper()} | SIZE: {radius} px | COLOR: {color}", True, (0, 255, 0))
        screen.blit(status, (20, ui_y))

        # Legend column layout
        col1 = [
            "1: Brush / 2: Rect / 3: Circle",
            "4: Eraser / 5: Square / 6: Right Tri",
            "7: Equi Tri / 8: Rhombus / 9: Line"
        ]
        col2 = [
            "F: Flood Fill",
            "T: Text Tool (Click & Type)",
            "C: Clear Canvas"
        ]
        col3 = [
            "F1: Small (2px) / F2: Med (5px) / F3: Large (10px)",
            "CTRL + S: Save to PNG",
            "R, G, B, W, Y: Change Colors"
        ]

        # Render legend text columns
        for i, text in enumerate(col1): screen.blit(font_small.render(text, True, (255, 255, 255)), (20, ui_y + 35 + i*22))
        for i, text in enumerate(col2): screen.blit(font_small.render(text, True, (255, 255, 255)), (290, ui_y + 35 + i*22))
        for i, text in enumerate(col3): screen.blit(font_small.render(text, True, (255, 255, 255)), (500, ui_y + 35 + i*22))

        # Update display and maintain 60 frames per second
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()