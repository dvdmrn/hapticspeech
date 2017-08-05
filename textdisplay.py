import parameters
import pygame

# ----------------------------------------------
#  Text objects
#      - helper for text_display
# ----------------------------------------------

def text_objects(text, font, color=parameters.BLACK):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# ----------------------------------------------
#  text display
#      - renders text, does not wrap!
# ----------------------------------------------

def textLine(screenSurface, text, pos, font, color=parameters.BLACK, cH=0, cV=0):
    """
    screenSurface: a Surface that represents the global screen
    pos: mid, top, bottom, or custom
    font: a Font
    cH: custom horizontal pos in pixels expressed as an int
    cV: custom vertical pos in pixels expressed as an int

    """

    division = 1 # very top
    if pos=="mid": # middle of screen
        division = 2
    if pos=="top": # top 75% of screen
        division = 4
    if pos=="bottom": # bot. 25% of the screen
        division = 4/float(3)
    if pos=="custom":
        TextSurf, TextRect = text_objects(text, font, color)
        TextRect.center = (cH,cV)
        screenSurface.blit(TextSurf, TextRect)
        
        pygame.display.update()

    else:        
        TextSurf, TextRect = text_objects(text, font, color)
        TextRect.center = ((parameters.screen_width/2),(parameters.screen_height/float(division)))
        screenSurface.blit(TextSurf, TextRect)

        pygame.display.update()

class TextWrapException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

def textWrap(screenSurface, string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextWrapException if the text won't fit onto the surface.
    """

    
    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextWrapException("The word " + word + " is too long to fit in the rect passed.")
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line 
                else: 
                    final_lines.append(accumulated_line) 
                    accumulated_line = word + " " 
            final_lines.append(accumulated_line)
        else: 
            final_lines.append(requested_line) 

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size) 
    surface.fill(background_color) 

    accumulated_height = 0 
    for line in final_lines: 
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextWrapException("Once word-wrapped, the text string was too tall to fit in the rect.")
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextWrapException("Invalid justification argument: " + str(justification))
        accumulated_height += font.size(line)[1]


    horizontal_center = (surface.get_rect().right - surface.get_rect().left)/2
    vertical_center = (surface.get_rect().bottom - surface.get_rect().top)/2


    screenSurface.blit(surface, ((parameters.screen_width/2) - horizontal_center , (parameters.screen_height/2) - vertical_center+75)) 
    return surface
