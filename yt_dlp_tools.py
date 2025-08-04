import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import threading
import yt_dlp
import os
import webbrowser
from datetime import datetime

class VideoDownloaderApp:
    def __init__(self, master):
        self.master = master
        master.title("影片下載器")

        # URL 輸入
        self.url_label = tk.Label(master, text="影片/音樂 URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        # 按鈕
        self.download_video_button = tk.Button(master, text="下載影片", command=lambda: self.start_download("video"))
        self.download_video_button.pack()

        self.download_audio_button = tk.Button(master, text="下載音樂", command=lambda: self.start_download("audio"))
        self.download_audio_button.pack()

        # 訊息顯示區
        self.message_text = ScrolledText(master, height=10, state='disabled')
        self.message_text.pack()

    def start_download(self, download_type):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("錯誤", "請輸入有效的 URL")
            return

        self.log_message("開始下載...")
        threading.Thread(target=self._download, args=(url, download_type)).start()

    def _download(self, url, download_type):
        options = self.get_download_options(download_type)

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(url, download=True)
                file_name = ydl.prepare_filename(info)
                self.log_message(f"下載完成: {file_name}")

                # 提示開啟目錄
                self.master.after(0, lambda: self.prompt_open_directory(os.path.dirname(file_name)))
        except Exception as e:
            self.log_message(f"下載出錯: {str(e)}")

    def get_download_options(self, download_type):
        if download_type == "video":
            return {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': '%(title)s.%(ext)s',
            }
        elif download_type == "audio":
            return {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': '%(title)s.%(ext)s',
            }

    def log_message(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.master.after(0, lambda: self._prepend_message(formatted_message))

    def _prepend_message(self, message):
        self.message_text.config(state='normal')
        current_content = self.message_text.get('1.0', 'end').strip()
        new_content = f"{message}\n{current_content}"
        self.message_text.delete('1.0', 'end')
        self.message_text.insert('1.0', new_content)
        self.message_text.config(state='disabled')

    def prompt_open_directory(self, directory):
        if messagebox.askyesno("下載完成", "是否開啟下載目錄?"):
            webbrowser.open(directory)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()
