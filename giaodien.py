import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng với Scroll và Nút")

        self.scroll_frame = ttk.Frame(root)
        self.scroll_frame.pack(expand=True, fill='both')

        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient='vertical')
        self.scrollbar.pack(side='right', fill='y')

        self.canvas = tk.Canvas(self.scroll_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side='left', expand=True, fill='both')

        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        self.select_all_var = tk.IntVar(value=0)
        self.start_button = ttk.Button(self.inner_frame, text="Bắt đầu tất cả", command=self.start_all)
        ttk.Checkbutton(self.inner_frame, text="Chọn tất cả", variable=self.select_all_var, command=self.toggle_select_all).grid(row=0, column=5, padx=5, pady=5, sticky='w')
        self.start_button.grid(row=0, column=2, padx=5, pady=5, sticky='w')

        ttk.Button(self.inner_frame, text="Chạy các luồng được chọn", command=self.run_selected_threads).grid(row=0, column=6, padx=5, pady=5, sticky='w')
        ttk.Button(self.inner_frame, text="Dừng tất cả", command=self.stop_all).grid(row=0, column=7, padx=5, pady=5, sticky='w')

        self.checkboxes = []
        self.status_text = tk.Text(self.root, wrap=tk.WORD, height=10, width=50)
        self.status_text.pack(fill='both', expand=True)

        self.progress_style = ttk.Style()
        self.progress_style.configure("Status.TProgressbar", troughcolor="white", background="white")
        self.progress_style.configure("Running.TProgressbar", troughcolor="green", background="green")

        self.progress_style.layout("Status.TProgressbar",
                                   [('Horizontal.Progressbar.trough',
                                     {'children': [('Horizontal.Progressbar.pbar',
                                                    {'side': 'left', 'sticky': 'ns'})],
                                      'sticky': 'nswe'})])

        self.progress_style.layout("Running.TProgressbar",
                                   [('Horizontal.Running.Progressbar.trough',
                                     {'children': [('Horizontal.Running.Progressbar.pbar',
                                                    {'side': 'left', 'sticky': 'ns'})],
                                      'sticky': 'nswe'})])

        self.thread_states = {}
        self.running_threads = set()

        for i in range(1, 11):
            ttk.Label(self.inner_frame, text=f"Luồng {i}").grid(row=i, column=0, padx=5, pady=5, sticky='w')

            progress_bar = ttk.Progressbar(self.inner_frame, mode='determinate', length=100, maximum=100, style="Status.TProgressbar")
            button_start = ttk.Button(self.inner_frame, text="Bắt đầu", command=lambda i=i, pb=progress_bar: self.start_or_continue_single(i, pb))
            button_stop = ttk.Button(self.inner_frame, text="Dừng", command=lambda i=i: self.stop_single(i), state="disabled")  # Nút dừng ở chế độ disable mặc định
            button_view = ttk.Button(self.inner_frame, text="Xem", command=lambda i=i: self.view_single(i), state="disabled")  # Nút xem ở chế độ disable mặc định

            progress_bar.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            button_start.grid(row=i, column=2, padx=5, pady=5, sticky='w')
            button_stop.grid(row=i, column=3, padx=5, pady=5, sticky='w')
            button_view.grid(row=i, column=4, padx=5, pady=5, sticky='w')

            checkbox_var = tk.IntVar(value=0)
            checkbox = ttk.Checkbutton(self.inner_frame, variable=checkbox_var)
            checkbox.grid(row=i, column=5, padx=5, pady=5, sticky='w')
            self.checkboxes.append(checkbox_var)
            self.thread_states[i] = "stopped"

        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.app_state = "stopped"

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def start_or_continue_single(self, thread_id, progress_bar):
        if self.thread_states[thread_id] == "stopped":
            self.start_single(thread_id, progress_bar)
        else:
            self.continue_single(thread_id)

    def start_all(self):
        if self.app_state == "stopped":
            self.show_status("Bắt đầu tất cả", "green")
            self.start_button.configure(text="Đang chạy", state="disabled", command=self.continue_all)
            self.app_state = "running"
            self.running_threads = set(range(1, 11))
            self.update_ui()

    def continue_all(self):
        self.show_status("Tiếp tục", "green")
        self.app_state = "running"
        self.update_ui()

    def start_single(self, thread_id, progress_bar):
        self.show_status(f"Bắt đầu luồng {thread_id}", "green")
        progress_bar.step(100)
        self.thread_states[thread_id] = "running"
        self.running_threads.add(thread_id)
        self.update_ui()

    def continue_single(self, thread_id):
        self.show_status(f"Tiếp tục luồng {thread_id}", "green")
        self.thread_states[thread_id] = "running"
        self.running_threads.add(thread_id)
        self.update_ui()

    def stop_all(self):
        self.show_status("Dừng tất cả", "orange")
        self.start_button.configure(text="Bắt đầu tất cả", state="normal", command=self.start_all)
        self.app_state = "stopped"
        self.running_threads.clear()
        self.update_ui()

    def stop_single(self, thread_id):
        self.show_status(f"Dừng luồng {thread_id}", "orange")
        self.thread_states[thread_id] = "stopped"
        self.running_threads.discard(thread_id)
        self.update_ui()

    def toggle_select_all(self):
        value = self.select_all_var.get()
        for checkbox_var in self.checkboxes:
            checkbox_var.set(value)

    def run_selected_threads(self):
        selected_threads = [i for i, checkbox_var in enumerate(self.checkboxes, start=1) if checkbox_var.get() == 1]
        self.show_status(f"Chạy các luồng được chọn: {selected_threads}", "green")
        self.running_threads.update(selected_threads)
        self.update_ui()

    def view_single(self, thread_id):
        if thread_id in self.running_threads:
            self.show_status(f"Đang xem luồng {thread_id}", "blue")
        else:
            self.show_status(f"Luồng {thread_id} chưa chạy, không thể xem ngay lúc này.", "red")

    def show_status(self, message, color):
        self.status_text.configure(state='normal')
        self.status_text.insert(tk.END, message + "\n", f"{color}_tag")
        self.status_text.tag_configure(f"{color}_tag", foreground=color)
        self.status_text.configure(state='disabled')
        self.status_text.see(tk.END)

    def update_ui(self):
        for thread_id in range(1, 11):
            progress_bar = self.inner_frame.grid_slaves(row=thread_id, column=1)[0]
            button_start = self.inner_frame.grid_slaves(row=thread_id, column=2)[0]
            button_stop = self.inner_frame.grid_slaves(row=thread_id, column=3)[0]
            button_view = self.inner_frame.grid_slaves(row=thread_id, column=4)[0]

            if thread_id in self.running_threads:
                progress_bar.configure(style="Running.TProgressbar")
                button_start.configure(text="Đang chạy", command=lambda i=thread_id, pb=progress_bar: self.continue_single(i), state="disabled")
                button_stop.configure(state="normal")  # Khi luồng đang chạy, mở khóa nút dừng
                button_view.configure(state="normal")  # Khi luồng đang chạy, mở khóa nút xem
            else:
                progress_bar.configure(style="Status.TProgressbar")
                button_start.configure(text="Bắt đầu", command=lambda i=thread_id, pb=progress_bar: self.start_or_continue_single(i, pb), state="normal")
                button_stop.configure(state="disabled")  # Khi luồng chưa chạy, khoá nút dừng
                button_view.configure(state="disabled")  # Khi luồng chưa chạy, khoá nút xem


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)

    style = ttk.Style(root)
    style.configure("Running.TButton", foreground="white", background="green")

    root.mainloop()
