from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab


def upload():
    mark_file = "key_koncept_signature.png"

    img_file = filedialog.askopenfile(
        title="Select an image file",
        filetypes=[("Image Files", "*.jpg; *.jpeg; *.png; *.svg")]
    )

    if img_file:
        try:
            image = Image.open(img_file.name)
            photo = ImageTk.PhotoImage(image)

            canvas.main_image = photo
            canvas.config(width=(photo.width() - 2), height=(photo.height() - 2))
            canvas.create_image(0, 0, anchor="nw", image=photo)

            mark = Image.open(mark_file)
            mark.thumbnail((80, 80), Image.Resampling.LANCZOS)
            watermark = ImageTk.PhotoImage(mark)

            canvas.watermark_image = watermark
            canvas.create_image(
                (photo.width() - 10), (photo.height() - 10),  # bottom-right corner
                anchor="se",
                image=watermark
            )

        except Exception as e:
            print("No good")


def save():
    photo_frame.update_idletasks()

    # Get frame dimensions
    x0 = canvas.winfo_rootx() + 1
    y0 = canvas.winfo_rooty() + 1
    x1 = x0 + canvas.winfo_width() - 2
    y1 = y0 + canvas.winfo_height() -2

    tagged_image = ImageGrab.grab(bbox=(x0, y0, x1, y1))

    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")]
    )

    if file_path:
        tagged_image.save(file_path, "PNG")
        print("Your file has been saved!")


window = Tk()
window.title("Water Marker")

window.columnconfigure(0, weight=1, minsize=100)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1, minsize=100)
window.rowconfigure(0, weight=0)
window.rowconfigure(1, weight=2)

buttons_frame = ttk.Frame(window, height=200, padding=(0, 12, 0, 12))
buttons_frame.grid(row=0, column=0, columnspan=3, sticky='ew')

buttons_frame.columnconfigure(0, weight=1, minsize=100)
buttons_frame.columnconfigure(1, weight=0, minsize=160)
buttons_frame.columnconfigure(2, weight=1, minsize=100)

upload_button = ttk.Button(buttons_frame, text="Upload", command=upload)
upload_button.grid(row=0, column=1, sticky='w')

save_button = ttk.Button(buttons_frame, text="Save", command=save)
save_button.grid(row=0, column=1, sticky='e')

photo_frame = ttk.Frame(window, height=300, width=600)
photo_frame.grid(row=1, column=0, columnspan=3, sticky='news')

canvas = Canvas(photo_frame, height=300, width=500, background='darkgray')
canvas.grid(row=0, column=0, columnspan=3, sticky='news')

window.mainloop()
