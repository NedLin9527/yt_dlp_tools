import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import yt_dlp


class VideoDownloaderApp:
  def __init__(self, master):
    self.master = master
    master.title("影片下載器")

    self.url_label = tk.Label(master, text="影片URL:")
    self.url_label.pack()

    self.url_entry = tk.Entry(master, width=50)
    self.url_entry.pack()

    self.download_button = tk.Button(master, text="下載影片",
                                     command=self.download_video)
    self.download_button.pack()

    self.message_text = ScrolledText(master, height=10, state='disabled')
    self.message_text.pack()

  def download_video(self):
    url = self.url_entry.get()
    if url:
      self.message_text.config(state='normal')
      self.message_text.insert('end', "開始下載影片...\n")
      self.message_text.config(state='disabled')

      threading.Thread(target=self._start_download, args=(url,)).start()
    else:
      messagebox.showerror("錯誤", "請輸入影片的URL")

  def _start_download(self, url):
    ydl_opts = {
      'format': 'best',
      'merge_output_format': 'mp4'
    }

    if 'list=' in url:
      ydl_opts.update({
        'outtmpl': '%(playlist)s/%(title)s.%(ext)s',
        'embed_thumbnail': True
      })
    else:
      ydl_opts.update({
        'outtmpl': '%(title)s.%(ext)s'
      })

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      try:
        ydl.download([url])
        self.message_text.config(state='normal')
        self.message_text.insert('end', "影片下載完成\n")
        self.message_text.config(state='disabled')
      except Exception as e:
        self.message_text.config(state='normal')
        self.message_text.insert('end', f"下載出錯: {str(e)}\n")
        self.message_text.config(state='disabled')


if __name__ == "__main__":
  root = tk.Tk()
  app = VideoDownloaderApp(root)
  root.mainloop()
