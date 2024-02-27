import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng với Scroll và Nút")

        # Tạo một Frame để chứa các thành phần và kích thước có thể scroll
        self.scroll_frame = ttk.Frame(root)
        self.scroll_frame.pack(expand=True, fill='both')

        # Tạo thanh cuộn
        self.scrollbar = ttk.Scrollbar(self.scroll_frame, orient='vertical')
        self.scrollbar.pack(side='right', fill='y')

        # Tạo vùng có thể scroll
        self.canvas = tk.Canvas(self.scroll_frame, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side='left', expand=True, fill='both')

        # Thiết lập thanh cuộn kết nối với vùng có thể scroll
        self.scrollbar.config(command=self.canvas.yview)

        # Tạo một Frame con để chứa nút và cột
        self.inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        # Tạo checkbox "Chọn tất cả" và nút "Bắt đầu tất cả"
        self.select_all_var = tk.IntVar(value=0)
        ttk.Checkbutton(self.inner_frame, text="Chọn tất cả", variable=self.select_all_var, command=self.toggle_select_all).grid(row=0, column=6, padx=5, pady=5, sticky='w')
        ttk.Button(self.inner_frame, text="Bắt đầu tất cả", command=self.start_all).grid(row=0, column=2, padx=5, pady=5, sticky='w')

        # Thêm nút "Chạy các luồng được chọn"
        ttk.Button(self.inner_frame, text="Chạy các luồng được chọn", command=self.run_selected_threads).grid(row=0, column=4, padx=5, pady=5, sticky='w')

        # Thêm nút "Dừng tất cả"
        ttk.Button(self.inner_frame, text="Dừng tất cả", command=self.stop_all).grid(row=0, column=3, padx=5, pady=5, sticky='w')

        # Thêm biến self.checkboxes để theo dõi tất cả các ô checkbox
        self.checkboxes = []

        for i in range(1, 11):  # Số dòng mẫu
            ttk.Label(self.inner_frame, text=f"Luồng {i}").grid(row=i, column=0, padx=5, pady=5, sticky='w')

            progress_bar = ttk.Progressbar(self.inner_frame, mode='indeterminate', length=300)
            button_start = ttk.Button(self.inner_frame, text="Bắt đầu", command=lambda i=i: self.start_single(i))
            button_stop = ttk.Button(self.inner_frame, text="Dừng")
            button_view = ttk.Button(self.inner_frame, text="Xem")

            progress_bar.grid(row=i, column=1, padx=5, pady=5, sticky='w')
            button_start.grid(row=i, column=2, padx=5, pady=5, sticky='w')
            button_stop.grid(row=i, column=3, padx=5, pady=5, sticky='w')
            button_view.grid(row=i, column=4, padx=5, pady=5, sticky='w')

            checkbox_var = tk.IntVar(value=0)
            checkbox = ttk.Checkbutton(self.inner_frame, variable=checkbox_var)
            checkbox.grid(row=i, column=6, padx=5, pady=5, sticky='w')  # Checkbox ở cuối cùng
            self.checkboxes.append(checkbox_var)

        # Bắt sự kiện khi kích thước nội dung bị thay đổi
        self.inner_frame.bind("<Configure>", self.on_frame_configure)

    def on_frame_configure(self, event):
        # Cập nhật kích thước của vùng có thể scroll khi nội dung thay đổi
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def start_all(self):
        print("Bắt đầu tất cả")

    def start_single(self, thread_id):
        print(f"Bắt đầu luồng {thread_id}")

    def toggle_select_all(self):
        value = self.select_all_var.get()
        for checkbox_var in self.checkboxes:
            checkbox_var.set(value)

    def run_selected_threads(self):
        selected_threads = [i for i, checkbox_var in enumerate(self.checkboxes, start=1) if checkbox_var.get() == 1]
        print(f"Chạy các luồng được chọn: {selected_threads}")

    def stop_all(self):
        print("Dừng tất cả")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
