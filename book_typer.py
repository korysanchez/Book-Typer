from tkinter import *
import time
import appearance


path = 'dracula'

curr_font = 4
current_theme = 5
font_size = 18

color_palettes = [['#fdfdfd', 'black', 'gray38', 'black'],
              ['lightgray', '#fdfdfd', 'black', 'black'],
              ['lightgray', 'black', 'gray38', 'white'],
              ['tan', '#D79771', '#964B00', 'saddlebrown'],
              ['#1b1b1b', 'lightgray', 'gray', 'white'],
              ['#1b1b1b', 'lightgray', '#Fc2AEC', 'white'],
              ['#1b1b1b', 'lightgray', 'red', 'white']]
background_color = color_palettes[current_theme][0]
text_color = color_palettes[current_theme][1]
highlighted_text_color = color_palettes[current_theme][2]
cursor_color = color_palettes[current_theme][3]

fonts = [('Courier', 6), ('Courier New', 2), ('Consolas', 1), ('Menlo', 2), ('Andale Mono', 2), ('Linux Libertine Mono O', 3)]
font, kerning = fonts[curr_font]


WINDOW_WIDTH = 700
WINDOW_HEIGHT = 800
MAX_WINDOW_ROWS = int(WINDOW_HEIGHT / font_size)
MAX_WINDOW_COLS = int(WINDOW_WIDTH / 10)
root = Tk()
root.title(str(path))
root.config(background = background_color)
root.minsize(WINDOW_WIDTH + 31, WINDOW_HEIGHT + 31)
root.geometry(str(WINDOW_WIDTH - 15) + 'x' + str(WINDOW_HEIGHT - 15))
canvas = Canvas(root, highlightthickness = 0, background = background_color)
canvas.config(height = WINDOW_HEIGHT + 1, width = WINDOW_WIDTH + 1)
canvas.pack(expand=1, padx = 15, pady = 15)



#========================================Initialize the book=================================================
full_text = open("./Resources/" + str(path) + '.txt', 'r').read()

text = [([], [])]

init_curr_row = 0
init_curr_width = 0
current_row = 0
current_column = 0
for i in full_text:
    if init_curr_row == 0 and init_curr_width == 0 and int(i) < len(color_palettes):
        color_theme = int(i)
    else:
        text[init_curr_row][0].append(i)
    if (init_curr_width == 0 and i == ' '):
        text[init_curr_row][0].remove(i)
    if i == '`':
        current_row = init_curr_row
        current_column = init_curr_width
        text[init_curr_row][0].remove(i)
    init_curr_width += 1
    if i == '\n' or init_curr_width >= WINDOW_WIDTH / 10:
        text.append(([], []))
        init_curr_row += 1
        init_curr_width = 0
cursor = canvas.create_rectangle(0, 0, 0, 0, fill = cursor_color, outline= '')

#==========================================Typing=====================================================
def get_key_bind(canvas_text, change):
    global current_column, current_row
    bind = canvas.itemcget(canvas_text, 'text')
    if (change):
        current_column += 1
        if canvas.coords(canvas_text)[1] > (current_row - top_most_row) * 18 + 10:
            current_column = 0
            current_row += 1
    if bind == " ":
        bind = '<space>'
    elif bind == '-':
        bind = '<minus>'
    elif bind == "’":
        bind = '<apostrophe>'
    elif bind == ',':
        bind = '<comma>'
    elif bind == '\n':
        bind = '<Return>'
        if change:
            current_row += 1
            current_column = 0
    return bind
def type_letter(event, canvas_text):
    global cursor
    canvas.itemconfig(canvas_text, fill=highlighted_text_color)
    root.unbind('<' + str(event.keysym) + '>')
    next = canvas_text + 1
    if 'Cursor' in canvas.gettags(canvas_text + 1):
        next = canvas_text + 2
    key_bind = get_key_bind(next, True)

    canvas.delete(cursor)
    if canvas.itemcget(canvas_text, 'text') != '\n':
        c = canvas.coords(canvas_text)
        cursor = canvas.create_line(c[0] + 5, c[1] - 10, c[0] + 5, c[1] + 8, fill = cursor_color, width = '1')
    else:
        c = canvas.coords(canvas_text + 1)
        cursor = canvas.create_line(c[0] - 5, c[1] - 10, c[0] - 5, c[1] + 8, fill = cursor_color, width = '1')
    root.bind(str(key_bind), lambda event, canvas_text = next: type_letter(event, canvas_text))


#========================================Drawing rows=================================================
def draw_row(row, y):
    global cursor
    color = text_color
    if (row < current_row):
        color = highlighted_text_color
    for i in range(len(text[row][0])):
        if row == current_row and i < current_column:
            color = highlighted_text_color
        elif row == current_row and i >= current_column:
            color = text_color
        canvas_text = canvas.create_text(i * 10 + 5, y, text = text[row][0][i], font = ("Consolas", font_size), fill = color)
        if row == current_row and i == current_column:
            cursor = canvas.create_rectangle(i * 10, y - 10 , i* 10 + 1, y  + 8, fill = cursor_color, outline='', tags=('Cursor'))
            key_bind = get_key_bind(canvas_text, False)
            root.bind('<' + str(key_bind) + '>', lambda event, canvas_text = canvas_text: type_letter(event, canvas_text))
        text[row][1].append(canvas_text)

def redraw_window(row):
    global cursor
    cursor = -1
    canvas.delete('all')
    root.unbind_all('q')
    y = 0
    for i in range(row, min(MAX_WINDOW_ROWS + row, len(text))):
        draw_row(i, y * font_size + 10)
        y += 1

top_most_row = 0
cursor = -1
redraw_window(top_most_row)

#========================================Shfiting=================================================
shifting = False
MAX_ROW = (len(text) - int(MAX_WINDOW_ROWS / 2))
def scroll(event):
    global text, top_most_row
    for i in range(top_most_row, MAX_WINDOW_ROWS):
        text[i] = (text[i][0], [])
    if event.keysym == 'Down' and top_most_row < MAX_ROW:
        top_most_row += 1
    elif event.keysym == 'Up' and top_most_row > 0:
        top_most_row -= 1
    elif shifting and event.keysym == 'Right':
        top_most_row = MAX_ROW
    elif shifting and event.keysym == 'Left':
        top_most_row = 0
    elif event.keysym == 'Right' and top_most_row <= MAX_ROW - (MAX_WINDOW_ROWS - 1):
        top_most_row += (MAX_WINDOW_ROWS - 1)
    elif event.keysym == 'Left' and top_most_row >= (MAX_WINDOW_ROWS - 1):
        top_most_row -= (MAX_WINDOW_ROWS - 1)
    redraw_window(top_most_row)
def toggle_shift(event):
    global shifting
    if (event.keysym == 'Shift_L'):
        if shifting:
            shifting = False
        else:
            shifting = True
    if (event.keysym == 'closed'):
        save()

root.bind("<Shift-KeyPress>", toggle_shift)
root.bind("<KeyRelease>", toggle_shift)
root.bind("<Down>", scroll)
root.bind("<Up>", scroll)
root.bind("<Left>", scroll)
root.bind("<Right>", scroll)

#========================================Saving location=================================================
def save():
    global current_row, current_column
    #doesnt currently save to the correct location
    with open("./Resources/" + str(path) + '.txt', 'w') as f:
        row, col = 0, 0
        f.write(str(current_theme))
        for i in range(1, len(full_text)):
            if (row < len(text)):
                if col < len(text[row][0]) - 1:
                    col += 1
                else:
                    col = 0
                    row += 1
            letter = full_text[i]
            if letter == '`':
                letter = ''
            if current_row == row and current_column == col - 1:
                f.write('`')
            f.write(letter)
    appearance.kill()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", save)

#=========================================Theme picking=================================================
def change_colors(event, color_theme):
    global current_theme, background_color, text_color, highlighted_text_color, cursor_color
    current_theme = color_theme
    background_color = color_palettes[current_theme][0]
    text_color = color_palettes[current_theme][1]
    highlighted_text_color = color_palettes[current_theme][2]
    cursor_color = color_palettes[current_theme][3]
    root.config(background = background_color)
    canvas.config(background = background_color)
    redraw_window(top_most_row)

def appearance_window(event):
    #fonts currently do not work
    appearance.run(color_palettes, fonts, curr_font)
    theme = 0
    for i in range(1, len(color_palettes) * 4, 4):
        appearance.canvas.tag_bind(i, "<Button-1>", lambda event, color_theme = theme: change_colors(event, color_theme))
        appearance.canvas.tag_bind(i+1, "<Button-1>", lambda event, color_theme = theme: change_colors(event, color_theme))
        appearance.canvas.tag_bind(i+2, "<Button-1>", lambda event, color_theme = theme: change_colors(event, color_theme))
        appearance.canvas.tag_bind(i+3, "<Button-1>", lambda event, color_theme = theme: change_colors(event, color_theme))
        theme += 1
appearance_window(None)
change_colors(None, color_theme)


root.mainloop()