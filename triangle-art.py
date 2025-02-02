import pygame
from tkinter import filedialog
def load_file():
    file_name = filedialog.askopenfilename(filetypes = [("Triangle Art Files", "*.tri")])
    if file_name != "":
        global triangles
        with open(file_name, "r") as file:
            triangles = [[[tuple([int(colour) for colour in triangle.split(",")]) for triangle in triangleset.split(";")] for triangleset in row.split("|")[:-1]] for row in file.read().split("\n")[:-1]]
def save_file():
    file_name = filedialog.asksaveasfilename(defaultextension = ".tri", filetypes = [("Triangle Art Files", "*.tri")])
    if file_name != "":    
        with open(file_name, "w") as file:
            file.write("".join(["".join(["".join(["".join([str(colour) + "," for colour in triangle])[:-1] + ";" for triangle in triangleset])[:-1] + "|" for triangleset in row]) + "\n" for row in triangles]))
class Button():
    def __init__(self, position, width, height, command = None):
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.command = command
    def draw(self, screen, mouse_pos):
        pygame.draw.rect(screen, (200,200,200), self.rect)
        pygame.draw.rect(screen, (100,100,100), self.rect, width = 2)
        if self.check_click(mouse_pos):
            pygame.draw.rect(screen, (200,200,200), canvas_button.rect, width = 2)
    def check_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
class ColourButton(Button):
    def __init__(self, position, colour):
        self.rect = pygame.Rect(position[0], position[1], 50, 50)
        self.colour = colour
    def draw(self, screen, mouse_pos, selected):
        pygame.draw.rect(screen, self.colour, self.rect)
        if selected:
            pygame.draw.rect(screen, (75,200,75), colour_button.rect, width = 2)
        else:
            pygame.draw.rect(screen, (200,200,200) if self.check_click(mouse_pos) else (100,100,100), colour_button.rect, width = 2)
class TextButton():
    def __init__(self, position, text, width, command = None):
        self.rect = pygame.Rect(position[0], position[1], width, 25)
        self.text = text
        self.command = command
    def draw(self, screen, mouse_pos):
        pygame.draw.rect(screen, (200,200,200), self.rect)
        pygame.draw.rect(screen, (100,100,100), self.rect, width = 2)
        font = pygame.font.Font(None, 25)
        text = font.render(self.text, True, (0,0,0,0))
        text_rect = text.get_rect(left = self.rect.left + 5, centery = self.rect.centery)
        screen.blit(text, text_rect)
        if self.check_click(mouse_pos):
            pygame.draw.rect(screen, (200,200,200), canvas_button.rect, width = 2)
def reset_canvas():
    global triangles
    triangles = [[[(0,0,0), (0,0,0), (0,0,0), (0,0,0)] for _ in range(len(triangles[y]))] for y in range(len(triangles))]
def toggle_outlines():
    global show_outlines
    show_outlines = not show_outlines
def cycle_mode():
    global triangle_mode
    triangle_mode += 1
    if triangle_mode > 3:
        triangle_mode = 0
def change_scale(change):
    global scale
    prev_y = position[1] / scale
    prev_x = position[0] / scale
    scale += change
    position[1] = prev_y * scale
    position[0] = prev_x * scale
def position_to_triangle(mouse_pos):
    mouse_pos = [mouse_pos[0] + position[0], mouse_pos[1] + position[1]]
    triangles_y = int(mouse_pos[1] // scale)
    triangles_x = int(mouse_pos[0] // scale)
    if triangle_mode == 3:
        return triangles_y, triangles_x, (0, 1, 2, 3)
    triangle_side = (mouse_pos[1] - triangles_y*scale) + (mouse_pos[0] - triangles_x*scale) > scale
    if triangle_mode == 0:
        triangles_i = ([2] if triangle_side else [3]) if (mouse_pos[1] - triangles_y*scale) > (mouse_pos[0] - triangles_x*scale) else ([1] if triangle_side else [0])
    elif triangle_mode == 1:
        triangles_i = (1, 2) if triangle_side else (0, 3)
    elif triangle_mode == 2:
        triangles_i = (2, 3) if (mouse_pos[1] - triangles_y*scale) > (mouse_pos[0] - triangles_x*scale) else (0, 1)
    return triangles_y, triangles_x, triangles_i
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
FPS = 30
running = True
scale = 50
triangles = [[[(0,0,0), (0,0,0), (0,0,0), (0,0,0)] for _ in range(50)] for _ in range(50)]
colour_buttons = (ColourButton((10, 10), (0,0,0)), ColourButton((65, 10), (150,150,150)), ColourButton((120, 10), (255,255,255)))
canvas_buttons = (TextButton((10, 65), "Reset", 54, reset_canvas), TextButton((10, 95), "Toggle outlines", 136, toggle_outlines), TextButton((10, 125), "Cycle mode", 108, cycle_mode), TextButton((10, SCREEN_HEIGHT - 30), "Zoom +", 70, lambda : change_scale(2)), TextButton((85, SCREEN_HEIGHT - 30), "Zoom -", 68, lambda : change_scale(-2)), TextButton((SCREEN_WIDTH - 61, 10), "Load", 51, load_file), TextButton((SCREEN_WIDTH - 61, 40), "Save", 51, save_file))
position = [0, 0] # Camera position
show_outlines = True
selected_colour = (150,150,150)
button_selected = False
triangle_mode = 0 # 0 = quarter triangle, 1 = half triangle top-right/bottom-left, 2 = half triangle top-left/bottom-right, 3 = squares
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                button_selected = False
                for colour_button in colour_buttons:
                    if colour_button.check_click(pygame.mouse.get_pos()):
                        button_selected = True
                        selected_colour = colour_button.colour
                for canvas_button in canvas_buttons:
                    if canvas_button.check_click(pygame.mouse.get_pos()):
                        button_selected = True
                        canvas_button.command()
                if not button_selected:
                    triangles_y, triangles_x, triangles_i = position_to_triangle(pygame.mouse.get_pos())
                    for i in triangles_i:
                        triangles[triangles_y][triangles_x][i] = selected_colour
            elif event.button == 3: # Right click
                triangles_y, triangles_x, triangles_i = position_to_triangle(pygame.mouse.get_pos())
                for i in triangles_i:
                    triangles[triangles_y][triangles_x][i] = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: # Left click
                target_code = None
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_PLUS] or keys_pressed[pygame.K_KP_PLUS]: # Increase scale
            change_scale(2)
        elif (keys_pressed[pygame.K_MINUS] or keys_pressed[pygame.K_KP_MINUS]) and scale > 2: # Decrease scale
            change_scale(-2)
        if keys_pressed[pygame.K_w]:
            position[1] -= scale / (2 if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT] else 10)
        if keys_pressed[pygame.K_s]:
            position[1] += scale / (2 if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT] else 10)
        if keys_pressed[pygame.K_a]:
            position[0] -= scale / (2 if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT] else 10)
        if keys_pressed[pygame.K_d]:
            position[0] += scale / (2 if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT] else 10)
        if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]: # Left or right click
            triangles_y, triangles_x, triangles_i = position_to_triangle(pygame.mouse.get_pos())
            if pygame.mouse.get_pressed()[0] and not button_selected: # Left click
                for i in triangles_i:
                    triangles[triangles_y][triangles_x][i] = selected_colour # Set triangle to same colour as clicked
            elif pygame.mouse.get_pressed()[2]: # Right click
                for i in triangles_i:
                    triangles[triangles_y][triangles_x][i] = (0,0,0) # Clear triangle
        while position[0] < 0: # Add more triangles to the left
            position[0] += scale
            for row in triangles:
                row.insert(0, [(0,0,0), (0,0,0), (0,0,0), (0,0,0)])
        while position[1] < 0: # Add more triangles to the top
            position[1] += scale
            triangles.insert(0, [[(0,0,0), (0,0,0), (0,0,0), (0,0,0)] for _ in range(len(triangles[0]))])
        while (position[0] + SCREEN_WIDTH) // scale >= len(triangles[0]): # Add more triangles to the right
            for row in triangles:
                row.append([(0,0,0), (0,0,0), (0,0,0), (0,0,0)])
        while (position[1] + SCREEN_HEIGHT) // scale >= len(triangles): # Add more triangles to the bottom
            triangles.append([[(0,0,0), (0,0,0), (0,0,0), (0,0,0)] for _ in range(len(triangles[0]))])
    screen.fill((0, 0, 0)) # Reset screen
    for y in range(int(position[1] // scale), int((position[1] + SCREEN_HEIGHT) // scale) + 1):
        for x in range(int(position[0] // scale), int((position[0] + SCREEN_WIDTH) // scale) + 1):
            if show_outlines and (triangles[y][x][0] == (0,0,0) or triangles[y][x][1] == (0,0,0) or triangles[y][x][2] == (0,0,0) or triangles[y][x][3] == (0,0,0)):
                if triangle_mode == 3:
                    pygame.draw.rect(screen, (50,50,50), (x*scale - position[0], y*scale - position[1], scale, scale), width = 1)
                if triangle_mode == 0 or triangle_mode == 2:
                    pygame.draw.polygon(screen, (50,50,50), [(x*scale - position[0], y*scale - position[1]), (x*scale - position[0], y*scale+scale - position[1]), (x*scale+scale - position[0], y*scale+scale - position[1])], width = 1)
                if triangle_mode == 0 or triangle_mode == 1:
                    pygame.draw.polygon(screen, (50,50,50), [(x*scale+scale - position[0], y*scale - position[1]), (x*scale+scale - position[0], y*scale+scale - position[1]), (x*scale - position[0], y*scale+scale - position[1])], width = 1)
    for y in range(int(position[1] // scale), int((position[1] + SCREEN_HEIGHT) // scale) + 1):
        for x in range(int(position[0] // scale), int((position[0] + SCREEN_WIDTH) // scale) + 1):
            if triangles[y][x][0] != (0,0,0):
                pygame.draw.polygon(screen, triangles[y][x][0], [(x*scale - position[0], y*scale - position[1]), (x*scale+(scale/2) - position[0], y*scale+(scale/2) - position[1]), (x*scale+scale - position[0], y*scale - position[1])])
            if triangles[y][x][1] != (0,0,0):
                pygame.draw.polygon(screen, triangles[y][x][1], [(x*scale+scale - position[0], y*scale - position[1]), (x*scale+(scale/2) - position[0], y*scale+(scale/2) - position[1]), (x*scale+scale - position[0], y*scale+scale - position[1])])
            if triangles[y][x][2] != (0,0,0):
                pygame.draw.polygon(screen, triangles[y][x][2], [(x*scale - position[0], y*scale+scale - position[1]), (x*scale+(scale/2) - position[0], y*scale+(scale/2) - position[1]), (x*scale+scale - position[0], y*scale+scale - position[1])])
            if triangles[y][x][3] != (0,0,0):
                pygame.draw.polygon(screen, triangles[y][x][3], [(x*scale - position[0], y*scale - position[1]), (x*scale+(scale/2) - position[0], y*scale+(scale/2) - position[1]), (x*scale - position[0], y*scale+scale - position[1])])
    for colour_button in colour_buttons:
        colour_button.draw(screen, pygame.mouse.get_pos(), colour_button.colour == selected_colour)
    for canvas_button in canvas_buttons:
        canvas_button.draw(screen, pygame.mouse.get_pos())
    pygame.display.flip() # Update screen
    clock.tick(FPS) # Wait for next frame