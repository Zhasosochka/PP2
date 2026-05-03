import pygame

# class to handle clickable buttons
class Button:
    # set up button text, position, size, and colors
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        # create a rectangle for position and collision
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        # set font for the button label
        self.font = pygame.font.SysFont("Verdana", 20)

    # render the button on the screen
    def draw(self, surface):
        # get current mouse coordinates
        mouse_pos = pygame.mouse.get_pos()

        # change color if the mouse is hovering over the button
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.color

        # draw the button background
        pygame.draw.rect(surface, color, self.rect)

        # create the text surface
        txt_surface = self.font.render(self.text, True, (255, 255, 255))

        # center the text inside the button rectangle
        text_x = self.rect.centerx - txt_surface.get_width() // 2
        text_y = self.rect.centery - txt_surface.get_height() // 2
        surface.blit(txt_surface, (text_x, text_y))

    # check if the button was clicked
    def is_clicked(self, event):
        # look for left mouse button clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # return true if the click was inside the button area
            if self.rect.collidepoint(event.pos):
                return True
        return False

# helper function to draw plain text on any surface
def draw_text(surface, text, size, x, y, color=(0,0,0)):
    # set up the font style and size
    font = pygame.font.SysFont("Verdana", size)
    # render the text into an image object
    txt_obj = font.render(text, True, color)
    # draw the text at the chosen coordinates
    surface.blit(txt_obj, (x, y))