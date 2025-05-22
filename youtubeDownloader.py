import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yt_dlp
import threading
from PIL import Image, ImageTk


# Download function
def download_video():
    url = url_entry.get().strip()
    quality = resolution_var.get()
    audio_only = audio_var.get()

    if not url:
        messagebox.showwarning("Warning", "Please enter a YouTube URL.")
        return

    folder_selected = filedialog.askdirectory()
    if not folder_selected:
        return

    status_label.config(text="Downloading...")
    progress['value'] = 0
    root.update()

    ydl_opts = {
        'outtmpl': f'{folder_selected}/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
    }

    if audio_only:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        })
    else:
        if quality == "Best":
            ydl_opts['format'] = 'bestvideo+bestaudio/best'
        else:
            ydl_opts['format'] = f'bestvideo[height={quality}]+bestaudio/best'

        ydl_opts['merge_output_format'] = 'mp4'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        progress['value'] = 100
        status_label.config(text="Download complete!")
        messagebox.showinfo("Success", "Download completed successfully!")
    except Exception as e:
        status_label.config(text="")
        messagebox.showerror("Error", f"Download failed:\n{e}")

def progress_hook(d):
    if d['status'] == 'downloading':
        downloaded = d.get('_percent_str', '0.0%').replace('%', '')
        try:
            progress['value'] = float(downloaded)
            root.update()
        except:
            pass

# Run download in separate thread
def start_download_thread():
    threading.Thread(target=download_video).start()

# GUI setup
root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("600x400")
root.minsize(500, 300)
root.resizable(True, True)
root.configure(bg="#121212")



try:
    image = Image.open("images.jpeg")  # <- Your image file
    image = image.resize((600, 150), Image.ANTIALIAS)
    banner = ImageTk.PhotoImage(image)
    img_label = tk.Label(root, image=banner)
    img_label.image = banner
    img_label.pack(pady=5)
except Exception as e:
    print(f"Image load failed: {e}")




# Title

tk.Label(root, text="YouTube Video Downloader", font=("Helvetica", 20, "bold"), bg="#121212", fg="white").pack(pady=5)

# URL entry
tk.Label(root, text="Enter YouTube Video URL:", font=("Helvetica", 12)).pack()
url_entry = tk.Entry(root, width=80)
url_entry.pack(pady=5)

# Audio Only Checkbox
audio_var = tk.BooleanVar()
tk.Checkbutton(root, text="Audio Only (MP3)", variable=audio_var).pack()

# Resolution Dropdown
tk.Label(root, text="Select Video Quality:", font=("Helvetica", 12)).pack(pady=5)
resolution_var = tk.StringVar(value="Best")
res_options = ["Best", "144", "240", "360", "480", "720", "1080"]
ttk.Combobox(root, textvariable=resolution_var, values=res_options, state="readonly").pack()

# Download Button
tk.Button(root, text="Download", command=start_download_thread, bg="green", fg="white", font=("Helvetica", 12)).pack(pady=10)

# Progress Bar
progress = ttk.Progressbar(root, length=500, mode='determinate')
progress.pack(pady=10)

# Status
status_label = tk.Label(root, text="", font=("Helvetica", 10), fg="blue")
status_label.pack()

root.mainloop()
