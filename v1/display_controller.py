import time
import random

borderOffset = 0
screenSize = 127
borderMax = screenSize - borderOffset

cornerBoxSize = 5
cornerBoxSizeLarge = 9
cornerBoxSizeLarger = 13

internalDisplay = None

loadingFlavour = ["Pushing pixels",
"Doing warpdrive",
"Collecting bits",
"Stirring whimsy",
"Warming hamster",
"Attaching leech",
"Detaching leech",
"Counting sheep",
"Getting sleepy",
"Warming CO2",
"Counting to 10",
"Almost there...",
"Zapping Bits",
"Clipping Code",
"Ionizing Data",
"Sparking I/O",
"Salting Keys",
"Hashing Loops",
"Twisting Bits",
"Priming Cache",
"Nudging Bytes",
"Tuning Gizmos",
"Loading...",
"Loading...",
"Loading...",
"Loading...",
"Loading...",
"Loading...",
"Loading...",
"Loading...",
"Loading...",
"Loading..."]

char_map = {
    '0': {
        (0,0),(1,0),(2,0),
        (0,1),(2,1),
        (0,2),(2,2),
        (0,3),(2,3),
        (0,4),(1,4),(2,4),
    },
    '1': {
        (1,0),
        (1,1),
        (1,2),
        (1,3),
        (1,4),
    },
    '2': {
        (0,0),(1,0),(2,0),
        (2,1),
        (0,2),(1,2),(2,2),
        (0,3),
        (0,4),(1,4),(2,4),
    },
    '3': {
        (0,0),(1,0),(2,0),
        (2,1),
        (0,2),(1,2),(2,2),
        (2,3),
        (0,4),(1,4),(2,4),
    },
    '4': {
        (0,0),(2,0),
        (0,1),(2,1),
        (0,2),(1,2),(2,2),
        (2,3),
        (2,4),
    },
    '5': {
        (0,0),(1,0),(2,0),
        (0,1),
        (0,2),(1,2),(2,2),
        (2,3),
        (0,4),(1,4),(2,4),
    },
    '6': {
        (0,0),(1,0),(2,0),
        (0,1),
        (0,2),(1,2),(2,2),
        (0,3),(2,3),
        (0,4),(1,4),(2,4),
    },
    '7': {
        (0,0),(1,0),(2,0),
        (2,1),
        (2,2),
        (2,3),
        (2,4),
    },
    '8': {
        (0,0),(1,0),(2,0),
        (0,1),(2,1),
        (0,2),(1,2),(2,2),
        (0,3),(2,3),
        (0,4),(1,4),(2,4),
    },
    '9': {
        (0,0),(1,0),(2,0),
        (0,1),(2,1),
        (0,2),(1,2),(2,2),
        (2,3),
        (0,4),(1,4),(2,4),
    }
    # Add more characters if needed
}

def draw_loading_screen(display):
    display.fill(0)
    draw_border(display)
    selected_message = random.choice(loadingFlavour)
    draw_text(selected_message, 0, 46, display)
    display.show()
    
def draw_stats_screen(co2, temperature, humidity, batteryPercentage, display):
    display.fill(0)
    draw_border(display)

    draw_string_in_fixed_box(batteryPercentage, 94, 4, display.pixel, char_width=3, char_height=5, spacing=1, border_margin=2, max_chars=3)
    
    draw_text(co2, determine_co2_draw_position(co2), 48, display)
    #draw_text("ppm", 0, 46, display)
    #draw_big_text(temperature + "oC" , 0, 20, display)
    #draw_big_text(batteryPercentage + "%", 0, 60, display)
    display.show()
    
def determine_co2_draw_position(co2):
    middlePoint = 63
    widthOfOneCharacter = 8
    lengthOfString = len(co2)
    return int(middlePoint - ((lengthOfString*widthOfOneCharacter)/2))  
    
def draw_text(text, x, y, display):
    display.text(text, x+borderOffset + 1, y+borderOffset + cornerBoxSizeLarger + 2, 1)
    
def draw_big_text(text, x, y, display):
    display.large_text(text, x+borderOffset + 1, y+borderOffset + cornerBoxSizeLarger + 2, 2)

def draw_border(display):
    display.line(borderOffset, borderOffset, borderMax, borderOffset, 1) # top
    display.line(borderOffset, borderOffset, borderOffset, borderMax, 1) # left
    display.line(borderMax, borderOffset, borderMax, borderMax, 1) # right
    display.line(borderOffset, borderMax, borderMax, borderMax, 1) # bottom
    
    # draw boxes at corners
    display.rect(borderOffset, borderOffset, cornerBoxSize, cornerBoxSize, 1)
    display.rect(borderOffset, borderMax - cornerBoxSize + 1, cornerBoxSize, cornerBoxSize, 1)
    display.rect(borderMax - cornerBoxSize + 1, borderMax - cornerBoxSize + 1, cornerBoxSize, cornerBoxSize, 1)
    display.rect(borderMax - cornerBoxSize + 1, borderOffset, cornerBoxSize, cornerBoxSize, 1)
    
    # draw large boxes at corners
    display.rect(borderOffset, borderOffset, cornerBoxSizeLarge, cornerBoxSizeLarge, 1)
    display.rect(borderOffset, borderMax - cornerBoxSizeLarge + 1, cornerBoxSizeLarge, cornerBoxSizeLarge, 1)
    display.rect(borderMax - cornerBoxSizeLarge + 1, borderMax - cornerBoxSizeLarge + 1, cornerBoxSizeLarge, cornerBoxSizeLarge, 1)
    display.rect(borderMax - cornerBoxSizeLarge + 1, borderOffset, cornerBoxSizeLarge, cornerBoxSizeLarge, 1)
    
    # draw larger boxes at corners
    display.rect(borderOffset, borderOffset, cornerBoxSizeLarger, cornerBoxSizeLarger, 1)
    display.rect(borderOffset, borderMax - cornerBoxSizeLarger + 1, cornerBoxSizeLarger, cornerBoxSizeLarger, 1)
    display.rect(borderMax - cornerBoxSizeLarger + 1, borderMax - cornerBoxSizeLarger + 1, cornerBoxSizeLarger, cornerBoxSizeLarger, 1)
    display.rect(borderMax - cornerBoxSizeLarger + 1, borderOffset, cornerBoxSizeLarger, cornerBoxSizeLarger, 1)
    
def draw_char(ch, x_offset, y_offset, pixel_func):
    """Draw a single character at (x_offset, y_offset) using pixel_func(x, y)."""
    if ch not in char_map:
        return
    for (dx, dy) in char_map[ch]:
        pixel_func(x_offset + dx, y_offset + dy, 1)

def draw_string(text, x, y, pixel_func, char_width=4, char_height=5, spacing=1):
    """
    Draw a string of characters at (x, y) using pixel_func(x, y).
    Returns the total width and height of the rendered text area.
    """
    if not text:
        return 0, 0
    # Calculate width
    total_width = len(text) * (char_width + spacing) - spacing
    total_height = char_height

    # Draw each character
    for i, ch in enumerate(text):
        char_x = x + i*(char_width+spacing)
        draw_char(ch, char_x, y, pixel_func)
        
    return total_width, total_height

def draw_rectangle(x, y, width, height, pixel_func):
    """
    Draw a rectangle with top-left corner at (x, y), given width and height.
    """
    # Top border
    for dx in range(width):
        pixel_func(x + dx, y, 1)
    # Bottom border
    for dx in range(width):
        pixel_func(x + dx, y + height - 1, 1)
    # Left border
    for dy in range(height):
        pixel_func(x, y + dy, 1)
    # Right border
    for dy in range(height):
        pixel_func(x + width - 1, y + dy, 1)
        
def draw_battery_terminal(x, y, box_width, box_height, pixel_func):
    """
    Draw a small terminal on the right side of the box to represent a battery terminal.
    This will be a small vertical protrusion centered vertically on the right side of the box.
    """
    terminal_width = 2  # how wide the terminal protrusion is
    terminal_height = box_height // 3  # about a third of the box height
    # Center it vertically
    terminal_y = y + (box_height - terminal_height) // 2
    terminal_x = x + box_width  # starting just after the right border of the box

    # Draw the terminal as a filled rectangle (or just borders if preferred)
    for dx in range(terminal_width):
        for dy in range(terminal_height):
            pixel_func(terminal_x + dx, terminal_y + dy, 1)

def draw_string_in_fixed_box(text, x, y, pixel_func, 
                             char_width=4, char_height=5, spacing=1, 
                             border_margin=1, max_chars=3):
    """
    Draws the string inside a fixed-size box that can hold up to 'max_chars' characters.
    If fewer characters are drawn, they are centered horizontally inside the box.
    """
    # Calculate the maximum text width that can fit inside the box with max_chars
    max_text_width = max_chars*(char_width+spacing) - spacing
    max_text_height = char_height

    # Calculate the total box size including borders
    box_width = max_text_width + border_margin*2
    box_height = max_text_height + border_margin*2
    
    # Draw the box first
    draw_rectangle(x, y, box_width, box_height, pixel_func)
    
    draw_battery_terminal(x, y, box_width, box_height, pixel_func)
    
    # Now calculate the width of the actual text we want to draw
    text_width = len(text)*(char_width+spacing)-spacing if text else 0

    # Center the text horizontally
    # Starting X for the text inside the box
    text_x = x + border_margin + (max_text_width - text_width)//2
    # Starting Y for the text inside the box (top aligned; if you want vertical center, do similar calculation)
    text_y = y + border_margin
    
    # Draw the string inside the box
    draw_string(text, text_x, text_y, pixel_func, char_width, char_height, spacing)
