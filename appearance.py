from tkinter import *

root, canvas = 0, 0
def run(color_palettes, fonts, curr_font):
    global root, canvas
    scale = 60
    root = Tk()
    root.title("Change Appearance")
    root.resizable(False, False)
    root.geometry('200x' + str(max(len(color_palettes) * scale + 10, len(fonts) * scale + 10)) + '+1200+50')
    canvas = Canvas(root, highlightthickness = 0, background = '#1b1b1b')
    canvas.pack(expand=1, fill=BOTH)
    

    def draw():
        for i in range(len(color_palettes)):
            canvas.create_rectangle(10, i * scale + 10, 190, i * scale + scale, fill=color_palettes[i][0], outline='white')
            canvas.create_text(55, i * scale + int(scale / 2) + 5, fill=color_palettes[i][2], text='Sampl', font=(fonts[curr_font][0], 28))
            canvas.create_text(145, i * scale + int(scale / 2) + 5, fill=color_palettes[i][1], text='e tex', font=(fonts[curr_font][0], 28))
            canvas.create_rectangle(94, i * scale + 10 + 10, 96, i * scale + scale - 14, fill=color_palettes[i][3], outline='')
    draw()


    for i in range(len(fonts)):
        canvas.create_rectangle(210, i * scale + 10, 390, i * scale + scale, fill='#1b1b1b')
        canvas.create_text(255, i * scale + int(scale / 2) + 5, fill='#dfdfdf', text='Sampl', font=(fonts[i][0], 26))
        canvas.create_text(345, i * scale + int(scale / 2) + 5, fill='#dfdfdf', text='e font', font=(fonts[i][0], 26))
        canvas.create_rectangle(292, i * scale + 10 + 20, 294, i * scale + scale - 20, fill='#dfdfdf')
    root.mainloop
def kill():
    root.destroy()