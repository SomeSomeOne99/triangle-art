import pygame
from tkinter import filedialog, colorchooser, Tk, ttk, VERTICAL, N, E, W
from functools import partial
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
    def __init__(self, position, colour, command = None):
        self.rect = pygame.Rect(position[0], position[1], 50, 50)
        self.colour = colour
        self.command = command
    def draw(self, screen, mouse_pos, selected):
        pygame.draw.rect(screen, self.colour, self.rect)
        if selected:
            pygame.draw.rect(screen, (75,200,75), colour_button.rect, width = 2)
        else:
            pygame.draw.rect(screen, (200,200,200) if self.check_click(mouse_pos) else (100,100,100), colour_button.rect, width = 2)
class TextButton(Button):
    def __init__(self, position, text, width, height = 25, command = None, text_size = 25, text_offset = 5):
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.text = text
        self.command = command
        self.text_size = text_size
        self.text_offset = text_offset
    def draw(self, screen, mouse_pos):
        pygame.draw.rect(screen, (200,200,200), self.rect)
        pygame.draw.rect(screen, (100,100,100), self.rect, width = 2)
        font = pygame.font.Font(None, self.text_size)
        text = font.render(self.text, True, (0,0,0,0))
        text_rect = text.get_rect(left = self.rect.left + self.text_offset, centery = self.rect.centery)
        screen.blit(text, text_rect)
        if self.check_click(mouse_pos):
            pygame.draw.rect(screen, (200,200,200), canvas_button.rect, width = 2)
class IconButton(Button):
    def __init__(self, position, width, height, icon_command = None, command = None, icon_offset = (0, 0), value = None):
        self.rect = pygame.Rect(position[0], position[1], width, height)
        self.icon_command = icon_command
        self.command = command
        self.icon_position = (position[0] + icon_offset[0], position[1] + icon_offset[1])
        self.value = value
    def draw(self, screen, mouse_pos, selected):
        pygame.draw.rect(screen, (150,150,150) if selected else (200,200,200), self.rect)
        pygame.draw.rect(screen, (100,100,100), self.rect, width = 2)
        if self.check_click(mouse_pos):
            pygame.draw.rect(screen, (200,200,200), canvas_button.rect, width = 2)
        self.icon_command(screen, self.icon_position) # Draw button icon
# Icon drawing functions
def draw_quarter_triangles_icon(screen, position):
    draw_half_triangles1_icon(screen, position) # Quarter triangles are composed of both half triangles
    draw_half_triangles2_icon(screen, position)
def draw_half_triangles1_icon(screen, position):
    pygame.draw.polygon(screen, (0,0,0), [(position[0] + 30, position[1]), (position[0], position[1] + 30), (position[0], position[1]), (position[0] + 30, position[1]), (position[0] + 30, position[1] + 30), (position[0], position[1] + 30)], width = 1)
def draw_half_triangles2_icon(screen, position):
    pygame.draw.polygon(screen, (0,0,0), [(position[0], position[1]), (position[0] + 30, position[1] + 30), (position[0], position[1] + 30), (position[0], position[1]), (position[0] + 30, position[1]), (position[0] + 30, position[1] + 30)], width = 1)
def draw_squares_icon(screen, position):
    pygame.draw.rect(screen, (0,0,0), (position[0], position[1], 30, 30), width = 1)
# Button command functions
def select_colour(i):
    global selected_colour
    selected_colour = colour_buttons[i].colour
def set_colour(i):
    global colour_buttons, selected_colour
    chosen_colour = colorchooser.askcolor(colour_buttons[i].colour)[0]
    if chosen_colour != None:
        if colour_buttons[i].colour == selected_colour:
            selected_colour = chosen_colour
        colour_buttons[i].colour = chosen_colour
def reset_colours():
    global colour_buttons
    colour_buttons[0].colour = (0,0,0)
    colour_buttons[1].colour = (150,150,150)
    colour_buttons[2].colour = (255,255,255)
    colour_buttons[3].colour = (255,0,0)
    colour_buttons[4].colour = (0,255,0)
    colour_buttons[5].colour = (0,0,255)
def reset_canvas():
    global triangles, position
    triangles = [[[(0,0,0) for _ in range(4)]]]
    position = [0, 0]
def toggle_outlines():
    global show_outlines
    show_outlines = not show_outlines
def change_mode(mode):
    global triangle_mode
    triangle_mode = mode
def change_scale(change):
    global scale
    prev_y = position[1] / scale
    prev_x = position[0] / scale
    scale += change
    position[1] = prev_y * scale
    position[0] = prev_x * scale
# Settings
def settings():
    def set_fps():
        global fps
        fps = int(fpsSpinbox.get())
        print(fps)
    def set_display():
        global screen_width, screen_height, screen, canvas_buttons, mode_buttons
        screen_width = int(displayWidthSpinbox.get())
        screen_height = int(displayHeightSpinbox.get())
        screen = pygame.display.set_mode((screen_width, screen_height))
        # placeholder, efficiency improvement intended
        canvas_buttons = tuple([TextButton((33 + 55*i, 45), "Edit", width = 27, height = 15, command = partial(set_colour, i), text_size = 15, text_offset = 3) for i in range(6)]) + (
            TextButton((10, 65), "Reset colours", 120, command = reset_colours), TextButton((10, 95), "Reset canvas", 116, command = reset_canvas), TextButton((10, 125), "Toggle outlines", 136, command = toggle_outlines),
            TextButton((10, 155), "Settings", 100, command = settings),
            TextButton((10, screen_height - 30), "Zoom +", 70, command = lambda : change_scale(2)), TextButton((85, screen_height - 30), "Zoom -", 68, command = lambda : change_scale(-2)),
            TextButton((screen_width - 61, 10), "Load", 51, command = load_file), TextButton((screen_width - 61, 40), "Save", 51, command = save_file))
        mode_buttons = (IconButton((screen_width - 45, screen_height - 180), 40, 40, draw_quarter_triangles_icon, command = lambda : change_mode(0), icon_offset = (5, 5), value = 0), IconButton((screen_width - 45, screen_height - 135), 40, 40, draw_half_triangles1_icon, command = lambda : change_mode(1), icon_offset = (5, 5), value = 1), IconButton((screen_width - 45, screen_height - 90), 40, 40, draw_half_triangles2_icon, command = lambda : change_mode(2), icon_offset = (5, 5), value = 2), IconButton((screen_width - 45, screen_height - 45), 40, 40, draw_squares_icon, command = lambda : change_mode(3), icon_offset = (5, 5), value = 3))
    root = Tk()
    mainframe = ttk.Frame(root)
    mainframe.grid(column = 0, row = 0)
    leftPanedwindow = ttk.Panedwindow(mainframe, orient = VERTICAL)
    leftPanedwindow.grid(column = 0, row = 0, padx = 5, sticky = (N))
    performanceFrame = ttk.Labelframe(leftPanedwindow, text = "Performance", width = 75, height = 75)
    ttk.Label(performanceFrame, text = "Target FPS: ").grid(column = 0, row = 0, padx = 5, sticky = (E))
    fpsSpinbox = ttk.Spinbox(performanceFrame, from_ = 0, to = float("inf"), command = set_fps, width = 3)
    fpsSpinbox.set(fps)
    fpsSpinbox.grid(column = 1, row = 0, padx = (0, 5))
    leftPanedwindow.add(performanceFrame)
    windowFrame = ttk.Labelframe(leftPanedwindow, text = "Display", width = 75, height = 75)
    ttk.Label(windowFrame, text = "Width: ").grid(column = 0, row = 0, padx = 5, sticky = (E))
    displayWidthSpinbox = ttk.Spinbox(windowFrame, from_ = 0, to = float("inf"), command = set_display, width = 5)
    displayWidthSpinbox.set(screen_width)
    displayWidthSpinbox.grid(column = 1, row = 0, padx = (0, 5))
    ttk.Label(windowFrame, text = "Height: ").grid(column = 0, row = 1, padx = 5, sticky = (E))
    displayHeightSpinbox = ttk.Spinbox(windowFrame, from_ = 0, to = float("inf"), command = set_display, width = 5)
    displayHeightSpinbox.set(screen_height)
    displayHeightSpinbox.grid(column = 1, row = 1, padx = (0, 5))
    leftPanedwindow.add(windowFrame)
    rightPanedwindow = ttk.Panedwindow(mainframe)
    rightPanedwindow.grid(column = 1, row = 0, padx = (0, 5))
    controlsFrame = ttk.Labelframe(rightPanedwindow, text = "Controls")
    controlsPanedwindow = ttk.Panedwindow(controlsFrame)
    controlsPanedwindow.grid(column = 0, row = 0)
    keyboardControlsFrame = ttk.Labelframe(controlsPanedwindow, text = "Keyboard")
    ttk.Label(keyboardControlsFrame, text = "W,A,S,D:").grid(column = 0, row = 0, sticky = (E))
    ttk.Label(keyboardControlsFrame, text = "Move camera").grid(column = 1, row = 0, sticky = (W))
    ttk.Label(keyboardControlsFrame, text = "Shift + W,A,S,D:").grid(column = 0, row = 1, sticky = (E))
    ttk.Label(keyboardControlsFrame, text = "Move camera at higher speed").grid(column = 1, row = 1, sticky = (W))
    ttk.Label(keyboardControlsFrame, text = "+/-:").grid(column = 0, row = 2, sticky = (E))
    ttk.Label(keyboardControlsFrame, text = "Zoom in/out").grid(column = 1, row = 2, sticky = (W))
    controlsPanedwindow.add(keyboardControlsFrame)
    mouseControlsFrame = ttk.Labelframe(controlsPanedwindow, text = "Mouse")
    ttk.Label(mouseControlsFrame, text = "Left Click:").grid(column = 0, row = 0, sticky = (E))
    ttk.Label(mouseControlsFrame, text = "Draw with selected colour").grid(column = 1, row = 0, sticky = (W))
    ttk.Label(mouseControlsFrame, text = "Scroll Click:").grid(column = 0, row = 1, sticky = (E))
    ttk.Label(mouseControlsFrame, text = "Set selected colour to hover target*").grid(column = 1, row = 1, sticky = (W))
    ttk.Label(mouseControlsFrame, text = "Right Click:").grid(column = 0, row = 2, sticky = (E))
    ttk.Label(mouseControlsFrame, text = "Erase (draw with #000000)").grid(column = 1, row = 2, sticky = (W))
    ttk.Label(mouseControlsFrame, text = "Scroll Up:").grid(column = 0, row = 3, sticky = (E))
    ttk.Label(mouseControlsFrame, text = "Cycle up colours*").grid(column = 1, row = 3, sticky = (W))
    ttk.Label(mouseControlsFrame, text = "Scroll Down:").grid(column = 0, row = 4, sticky = (E))
    ttk.Label(mouseControlsFrame, text = "Cycle down colours*").grid(column = 1, row = 4, sticky = (W))
    controlsPanedwindow.add(mouseControlsFrame)
    rightPanedwindow.add(controlsFrame)
    root.mainloop()
# Calculation functions
def position_to_triangle(mouse_pos, triangle_mode_ = None):
    if triangle_mode_ is None: # No mode specified
        triangle_mode_ = triangle_mode
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
screen_width, screen_height = 500, 500
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
fps = 30
running = True
scale = 50
triangles = [[[(0,0,0), (0,0,0), (0,0,0), (0,0,0)] for _ in range(50)] for _ in range(50)]
colour_buttons = (ColourButton((10, 10), (0,0,0), command = partial(select_colour, 0)), ColourButton((65, 10), (150,150,150), command = partial(select_colour, 1)), ColourButton((120, 10), (255,255,255), command = partial(select_colour, 2)), ColourButton((175, 10), (255,0,0), command = partial(select_colour, 3)), ColourButton((230, 10), (0,255,0), command = partial(select_colour, 4)), ColourButton((285, 10), (0,0,255), command = partial(select_colour, 5)))
canvas_buttons = tuple([TextButton((33 + 55*i, 45), "Edit", width = 27, height = 15, command = partial(set_colour, i), text_size = 15, text_offset = 3) for i in range(6)]) + (
    TextButton((10, 65), "Reset colours", 120, command = reset_colours), TextButton((10, 95), "Reset canvas", 116, command = reset_canvas), TextButton((10, 125), "Toggle outlines", 136, command = toggle_outlines),
    TextButton((10, 155), "Settings", 81, command = settings),
    TextButton((10, screen_height - 30), "Zoom +", 70, command = lambda : change_scale(2)), TextButton((85, screen_height - 30), "Zoom -", 68, command = lambda : change_scale(-2)),
    TextButton((screen_width - 61, 10), "Load", 51, command = load_file), TextButton((screen_width - 61, 40), "Save", 51, command = save_file))
mode_buttons = (IconButton((screen_width - 45, screen_height - 180), 40, 40, draw_quarter_triangles_icon, command = lambda : change_mode(0), icon_offset = (5, 5), value = 0), IconButton((screen_width - 45, screen_height - 135), 40, 40, draw_half_triangles1_icon, command = lambda : change_mode(1), icon_offset = (5, 5), value = 1), IconButton((screen_width - 45, screen_height - 90), 40, 40, draw_half_triangles2_icon, command = lambda : change_mode(2), icon_offset = (5, 5), value = 2), IconButton((screen_width - 45, screen_height - 45), 40, 40, draw_squares_icon, command = lambda : change_mode(3), icon_offset = (5, 5), value = 3))
position = [0, 0] # Camera position
show_outlines = True
selected_colour = (150,150,150)
button_selected = False
clearCount = 0
triangle_mode = 0 # 0 = quarter triangle, 1 = half triangle top-right/bottom-left, 2 = half triangle top-left/bottom-right, 3 = squares
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                button_selected = False
                for button in canvas_buttons + colour_buttons + mode_buttons:
                    if button.check_click(pygame.mouse.get_pos()):
                        button_selected = True
                        button.command()
                        break
                if not button_selected:
                    triangles_y, triangles_x, triangles_i = position_to_triangle(pygame.mouse.get_pos())
                    for i in triangles_i:
                        triangles[triangles_y][triangles_x][i] = selected_colour
            elif event.button == 2:
                triangles_y, triangles_x, triangles_i = position_to_triangle(pygame.mouse.get_pos(), 0)
                selected_colour = triangles[triangles_y][triangles_x][triangles_i[0]]
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
    while position[0] < 0 or position[1] < 0 or (position[0] + screen_width) // scale >= len(triangles[0]) or (position[1] + screen_height) // scale >= len(triangles):
        while position[0] < 0: # Add more triangles to the left
            position[0] += scale
            for row in triangles:
                row.insert(0, [(0,0,0), (0,0,0), (0,0,0), (0,0,0)])
        while position[1] < 0: # Add more triangles to the top
            position[1] += scale
            triangles.insert(0, [[(0,0,0), (0,0,0), (0,0,0), (0,0,0)] for _ in range(len(triangles[0]))])
        while (position[0] + screen_width) // scale >= len(triangles[0]): # Add more triangles to the right
            for row in triangles:
                row.append([(0,0,0), (0,0,0), (0,0,0), (0,0,0)])
        while (position[1] + screen_height) // scale >= len(triangles): # Add more triangles to the bottom
            triangles.append([[(0,0,0), (0,0,0), (0,0,0), (0,0,0)] for _ in range(len(triangles[0]))])
    # Trim blank canvas rows/columns
    blank = True
    for y in range(0, int(position[1] // scale)): # Trim rows above camera
        for x in range(len(triangles[y])):
            for triangle in triangles[y][x]:
                if triangle != (0,0,0):
                    blank = False
                    break
            if not blank:
                break
        if not blank:
            break
        triangles.pop(0) # Clear first row if blank
        position[1] -= scale
    blank = True
    for x in range(0, int(position[0] // scale)): # Trim columns left of camera
        for y in range(len(triangles)):
            for triangle in triangles[y][x]:
                if triangle != (0,0,0):
                    blank = False
                    break
            if not blank:
                break
        if not blank:
            break
        for y in range(len(triangles)):
            triangles[y].pop(0) # Clear first column if blank
        position[0] -= scale
    blank = True
    for y in range(len(triangles) - 1, int((position[1] + screen_height) // scale), -1): # Trim rows below camera
        for x in range(len(triangles[y])):
            for triangle in triangles[y][x]:
                if triangle != (0,0,0):
                    blank = False
                    break
            if not blank:
                break
        if not blank:
            break
        triangles.pop(len(triangles) - 1) # Clear last row if blank
    blank = True
    for x in range(len(triangles[0]) - 1, int((position[0] + screen_width) // scale), -1): # Trim columns right of camera
        for y in range(len(triangles)):
            for triangle in triangles[y][x]:
                if triangle != (0,0,0):
                    blank = False
                    break
            if not blank:
                break
        if not blank:
            break
        for y in range(len(triangles)):
            triangles[y].pop(len(triangles[y]) - 1) # Clear last column if blank
    screen.fill((0, 0, 0)) # Reset screen
    for y in range(int(position[1] // scale), int((position[1] + screen_height) // scale) + 1):
        for x in range(int(position[0] // scale), int((position[0] + screen_width) // scale) + 1):
            if show_outlines and (triangles[y][x][0] == (0,0,0) or triangles[y][x][1] == (0,0,0) or triangles[y][x][2] == (0,0,0) or triangles[y][x][3] == (0,0,0)):
                if triangle_mode == 3:
                    pygame.draw.rect(screen, (50,50,50), (x*scale - position[0], y*scale - position[1], scale, scale), width = 1)
                if triangle_mode == 0 or triangle_mode == 2:
                    pygame.draw.polygon(screen, (50,50,50), [(x*scale - position[0], y*scale - position[1]), (x*scale - position[0], y*scale+scale - position[1]), (x*scale+scale - position[0], y*scale+scale - position[1])], width = 1)
                if triangle_mode == 0 or triangle_mode == 1:
                    pygame.draw.polygon(screen, (50,50,50), [(x*scale+scale - position[0], y*scale - position[1]), (x*scale+scale - position[0], y*scale+scale - position[1]), (x*scale - position[0], y*scale+scale - position[1])], width = 1)
    for y in range(int(position[1] // scale), int((position[1] + screen_height) // scale) + 1):
        for x in range(int(position[0] // scale), int((position[0] + screen_width) // scale) + 1):
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
    for mode_button in mode_buttons:
        mode_button.draw(screen, pygame.mouse.get_pos(), mode_button.value == triangle_mode)
    pygame.display.flip() # Update screen
    clock.tick(fps) # Wait for next frame