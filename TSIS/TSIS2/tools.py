import pygame
import math

def flood_fill(surface, x, y, target_color, fill_color):
    """
    Standard stack-based flood fill algorithm.
    Fills a closed area starting from (x, y) if it matches target_color.
    """
    # If the target color is the same as the fill color, no action is needed
    if target_color == fill_color: return

    width, height = surface.get_size()
    # Use a list as a stack for coordinates to visit
    stack = [(x, y)]

    while stack:
        curr_x, curr_y = stack.pop()

        # Check if coordinates are within the canvas boundaries
        if 0 <= curr_x < width and 0 <= curr_y < height:
            # Check if the current pixel matches the color we want to replace
            if surface.get_at((curr_x, curr_y)) == target_color:
                # Set the new color
                surface.set_at((curr_x, curr_y), fill_color)

                # Add all 4 neighboring pixels (Up, Down, Left, Right) to the stack
                stack.append((curr_x + 1, curr_y))
                stack.append((curr_x - 1, curr_y))
                stack.append((curr_x, curr_y + 1))
                stack.append((curr_x, curr_y - 1))

def draw_shape(surface, tool, color, start, end, radius):
    """
    Main dispatcher function to draw different geometric shapes
    based on the selected tool and mouse positions.
    """
    # Rectangle tool
    if tool == "rect":
        # Calculate top-left corner and dimensions
        x, y = min(start[0], end[0]), min(start[1], end[1])
        width, height = abs(start[0] - end[0]), abs(start[1] - end[1])
        pygame.draw.rect(surface, color, (x, y, width, height), radius)

    # Circle tool
    elif tool == "circle":
        # Calculate radius using the distance formula between start and end points
        r = int(math.sqrt((end[0]-start[0])**2 + (end[1]-start[1])**2))
        pygame.draw.circle(surface, color, start, r, radius)

    # Straight line tool
    elif tool == "line":
        pygame.draw.line(surface, color, start, end, radius)

    # Square tool (forces equal width and height)
    elif tool == "square":
        side = max(abs(end[0] - start[0]), abs(end[1] - start[1]))
        # Determine direction based on mouse position relative to start
        x = start[0] if end[0] > start[0] else start[0] - side
        y = start[1] if end[1] > start[1] else start[1] - side
        pygame.draw.rect(surface, color, (x, y, side, side), radius)

    # Right-angled triangle tool
    elif tool == "right_triangle":
        # Points: Start, Vertex forming the 90-degree angle, End
        points = [start, (start[0], end[1]), end]
        pygame.draw.polygon(surface, color, points, radius)

    # Equilateral triangle tool
    elif tool == "equilateral_triangle":
        base_width = end[0] - start[0]
        # Height of an equilateral triangle: side * sqrt(3)/2
        h = base_width * (math.sqrt(3) / 2)
        # Calculate 3 vertices
        points = [
            ((start[0] + end[0]) / 2, start[1]), # Top vertex
            (start[0], start[1] + h),            # Bottom-left
            (end[0], start[1] + h)               # Bottom-right
        ]
        pygame.draw.polygon(surface, color, points, radius)

    # Rhombus (Diamond) tool
    elif tool == "rhombus":
        # Find center points between start and end coordinates
        mid_x, mid_y = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        # Points: Top, Left, Bottom, Right midpoints
        points = [
            (mid_x, start[1]), # Top
            (start[0], mid_y), # Left
            (mid_x, end[1]),   # Bottom
            (end[0], mid_y)    # Right
        ]
        pygame.draw.polygon(surface, color, points, radius)