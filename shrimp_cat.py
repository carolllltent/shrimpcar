from pathlib import Path
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageSequence, ImageTk, ImageEnhance

ROOT = Path(__file__).resolve().parent 
GIF_PATH = ROOT/'shrimp-posture-spinning-cat.gif'

COLS, ROWS = 85, 110 
CELL_W, CELL_H = 11, 14
BG = (9, 12, 22)
CHARS = '@%#*+=-:.'

def find_font():
    candidates = [
        '/System/Library/Fonts/Menlo.ttc', 
        '/System/Library/Fonts/Monaco.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
        'C:/Windows/Fonts/consola.ttf',
    ]
    #finds each font path 
    for candidate in candidates: 
        #check if the font thing exists
        if Path(candidate).exists(): 
            #return to stop 
            return ImageFont.truetype(candidate, 15)
        return ImageFont.load_default()

#makes the image ascii art 
def make_ascii_frame(original, font): 
    source = original.convert('RGB').resize((COLS, ROWS), Image.Resampling.LANCZOS)
    #turns the image in rgb 
    #resize it to the columns and rows 
    source = ImageEnhance.Contrast(source).enhance(1.3)
    #helps with contrast to make more distinguishable 
    source = ImageEnhance.Color(source).enhance(1.25)
    #increase saturation by 25% 
    picture = Image.new('RGB', (COLS * CELL_W, ROWS * CELL_H), BG)
    #create empty image to draw ascii character 
    draw = ImageDraw.Draw(picture)
    #creates a drawing object to darw on the picture 
    pixels = source.load()

    #loops in eveyr row 
    for y in range(ROWS): 
        #loops in every column in the row 
        for x in range(COLS): 
            r, g, b = pixels[x, y]
            #more green 
            brightness = (0.2126 * r + 0.7152 * g + 0.0722 * b)/255
            #brightness correpsond to character nad index 
            index = min(len(CHARS) - 1, int((1 - brightness) * len(CHARS)))
            symbol = CHARS[index]
            colour = (r, g, b)
            #if the pixel is dark, replace with dark grey 
            if max(colour) < 34: 
                colour = (36, 43, 56) 
                #draw cat 
            draw.text((x * CELL_W, y * CELL_H - 1), symbol, 
                      font=font, fill=colour, stroke_width = 0)
    return picture 

def main(): 
    if not GIF_PATH.exists(): 
        raise SystemExit (
            'Could not find the shrimp-posture-spinning-cat.gif. \n'
            'Place it in the same folder as disco_cat.py and run again.'
        )

window = tk.Tk()
window.title('Disco Cat - animated gif to ascii art')
window.configure(bg='#090c16')
window.geometry("1050x1700")
window.resizable(True,True)

header = tk.Label(window, text=" shrimp car", 
                  font=('Menlo', 18, 'bold'), fg='#ffbb78', bg='#090c16')
header.pack(pady=(12,4))
label = tk.Label(window, bg='#090c16', bd=0)
label.pack(padx=12)
footer = tk.Label(window, text='Animated gif - Space to pause', 
                  font=('Menlo', 10), fg='#adb5c6', bg='#090c16')
footer.pack(pady=(4,12))
font = find_font()
image = Image.open(GIF_PATH)
frames = []
durations = []
for frame in ImageSequence.Iterator(image): 
    ascii_image = make_ascii_frame(frame.copy(), font) 
    frames.append(ImageTk.PhotoImage(ascii_image, master=window))
    durations.append(max(40, frame.info.get('duration', 100)))

state= {'index': 0, 'paused': False}

def toggle_pause(event=None): 
        state['paused'] = not state['paused']

window.bind('<space>', toggle_pause)

def tick(): 
    if not state['paused']: 
            index = state['index']
            label.configure(image=frames[index])
            state['index'] = (index + 1) % len(frames)
            delay = durations[index]
    else: 
            delay = 80 
    window.after(delay, tick)

tick()
window.mainloop()

if __name__ == '__main__': 
    main()