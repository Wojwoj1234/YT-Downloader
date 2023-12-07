from pytube import YouTube
from moviepy.editor import VideoFileClip
import tkinter as tk
from tkinter import filedialog
import os
import shutil



def download_video():
    url = url_entry.get()
    output_path = output_directory.get()
    download_format = format_selection.get()  

    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()

        if download_format == "MP3":
            cache_path = os.path.join(output_path, "cache")
            os.makedirs(cache_path, exist_ok=True)
            video.download(cache_path)
            status_label.config(text="Video downloaded successfully!")

            # kowertowanie do mp3
            audio_path = os.path.join(output_path, video.default_filename.replace(".mp4", ".mp3"))
            video_clip = VideoFileClip(os.path.join(cache_path, video.default_filename))
            audio_clip = video_clip.audio
            audio_clip.write_audiofile(audio_path)
            audio_clip.close()
            video_clip.close()
            status_label.config(text="Video converted to MP3 successfully!")

            # usuwanie cache
            shutil.rmtree(cache_path)
        else:
            video.download(output_path)
            status_label.config(text="Video downloaded successfully!")
            
    except Exception as e:
        status_label.config(text="Error: " + str(e))

# tworzenie okna programu
window = tk.Tk()
window.geometry("800x600")  
window.title("YouTube Downloader")

# pole url
url_label = tk.Label(window, text="Video URL:")
url_label.pack()

url_entry = tk.Entry(window, width=60, bd=2, relief="solid") 
url_entry.pack()

# wybór formatu
format_label = tk.Label(window, text="Download Format:")
format_label.pack()

format_selection = tk.StringVar()
format_selection.set("MP4")  

mp4_radio_button = tk.Radiobutton(window, text="MP4", variable=format_selection, value="MP4")
mp4_radio_button.pack()

mp3_radio_button = tk.Radiobutton(window, text="MP3", variable=format_selection, value="MP3")
mp3_radio_button.pack()

#wybieranie folderu
output_directory = tk.StringVar()
output_directory.set(os.path.dirname(os.path.abspath(__file__)))
output_button = tk.Button(window, text="Select Output Directory", command=lambda: output_directory.set(filedialog.askdirectory()))
output_button.pack(pady=10)

# przycisk download
download_button = tk.Button(window, text="Download", command=download_video)
download_button.pack(pady=10)

# status
status_label = tk.Label(window, text="")
status_label.pack()

# loop
window.mainloop()
