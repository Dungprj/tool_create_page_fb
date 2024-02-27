import tkinter as tk
from tkinter import ttk
from selenium import webdriver
import threading
import time
from screeninfo import get_monitors

class User:
    def __init__(self, window_size, window_position):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
        chrome_options.add_argument(f"--window-position={window_position[0]},{window_position[1]}")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.thread_running = False

    def login(self):
        self.driver.get("https://www.facebook.com/")
        cookies = [
            # Existing cookies...
        ]
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        self.driver.refresh()

    def resize_tab_and_content(self, tab_size):
        self.driver.set_window_size(tab_size[0], tab_size[1])
        self.driver.execute_script(f"document.body.style.zoom = {tab_size[1] / 200}")

    def close(self):
        self.driver.quit()

    def start_scenario(self, page):
        self.thread_running = True
        thread = threading.Thread(target=self.run_scenario, args=(page,))
        thread.start()

    def stop_scenario(self):
        self.thread_running = False

    def view_scenario(self):
        self.driver.maximize_window()

    def run_scenario(self, page):
        while self.thread_running:
            self.login()
            self.resize_tab_and_content((100, 600))
            page.create_facebook_page()
            time.sleep(5)
            print("Scenario is running in thread.")
            self.close()

class Page:
    def __init__(self, user):
        self.user = user

    def create_facebook_page(self):
        self.user.driver.get("https://www.facebook.com/pages/creation/?ref_type=launch_point")
        time.sleep(5)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng với Scroll và Nút")
        self.users = []
        self.pages = []

        # Thêm biến self.checkboxes để theo dõi tất cả các ô checkbox
        self.checkboxes = []

        # Thêm biến để theo dõi trạng thái của các luồng
        self.thread_states = []

        # Khởi tạo thanh cuộn và frame
        self.create_scroll_frame()

        for i in range(1, 11):
            ttk.Label(self.inner_frame, text=f"Luồng {i}").grid(row=i, column=0, padx=5, pady=5, sticky='w')

            progress_bar = ttk.Progressbar(self.inner_frame, mode='indeterminate', length=300)
            button_start = ttk.Button(self.inner_frame, text="Bắt đầu", command=lambda i=i: self.start_single(i))
            button_stop = ttk.Button(self.inner_frame, text="Dừng", command=lambda i=i: self.stop_single(i))
            button_view = ttk.Button(self.inner_frame, text="Xem", command=lambda i=i: self.view_single(i))

            progress_bar.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            button_start.grid(row=i, column=2, padx=5, pady=5, sticky='w')
            button_stop.grid(row=i, column=3, padx=5, pady=5, sticky='w')
            button_view.grid(row=i, column=4, padx=5, pady=5, sticky='w')

            checkbox_var = tk.IntVar(value=0)
            checkbox = ttk.Checkbutton(self.inner_frame, variable=checkbox_var)
            checkbox.grid(row=i, column=6, padx=5, pady=5, sticky='w')
            self.checkboxes.append(checkbox_var)

            # Khởi tạo trạng thái luồng cho mỗi luồng
            self.thread_states.append({'running': False, 'user': None, 'page': None})

        # Bắt sự kiện khi kích thước nội dung bị thay đổi
        self.inner_frame.bind("<Configure>", self.on_frame_configure)

        ttk.Button(self.inner_frame, text="Bắt đầu tất cả", command=self.start_all).grid(row=0, column=2, padx=5, pady=5, sticky='w')
        ttk.Button(self.inner_frame, text="Chạy các luồng được chọn", command=self.run_selected_threads).grid(row=0, column=4, padx=5, pady=5, sticky='w')
        ttk.Button(self.inner_frame, text="Dừng tất cả", command=self.stop_all).grid(row=0, column=3, padx=5, pady=5, sticky='w')

    def create_scroll_frame(self):
        self.scroll_frame = ttk.Frame(self.root)
        self.scroll_frame.pack(expand=True, fill='both')

        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient='vertical')
        self.scrollbar.pack(side='right', fill='y')

        self.canvas = tk.Canvas(self.scroll_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side='left', expand=True, fill='both')

        self.scrollbar.config(command=self.canvas.yview)

        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def start_all(self):
        for i, checkbox_var in enumerate(self.checkboxes, start=1):
            if checkbox_var.get() == 1:
                self.start_single(i)

    def start_single(self, thread_id):
        if not self.thread_states[thread_id - 1]['running']:
            user = User((100, 600), (0, 0))  # Điều chỉnh kích thước và vị trí cửa sổ theo ý muốn
            page = Page(user)
            self.thread_states[thread_id - 1]['user'] = user
            self.thread_states[thread_id - 1]['page'] = page
            user.start_scenario(page)
            self.thread_states[thread_id - 1]['running'] = True
            print(f"Bắt đầu luồng {thread_id}")

    def stop_single(self, thread_id):
        if self.thread_states[thread_id - 1]['running']:
            user = self.thread_states[thread_id - 1]['user']
            user.stop_scenario()
            self.thread_states[thread_id - 1]['running'] = False
            print(f"Dừng luồng {thread_id}")

    def view_single(self, thread_id):
        if self.thread_states[thread_id - 1]['running']:
            user = self.thread_states[thread_id - 1]['user']
            user.view_scenario()
            print(f"Xem luồng {thread_id}")
        else:
            print(f"Luồng {thread_id} không đang chạy")

    def run_selected_threads(self):
        for i, checkbox_var in enumerate(self.checkboxes, start=1):
            if checkbox_var.get() == 1:
                self.start_single(i)

    def stop_all(self):
        for i in range(1, 11):
            self.stop_single(i)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
