from selenium import webdriver
import threading
import time
from screeninfo import get_monitors

class User:
    def __init__(self, window_size, window_position):
        # Create a Selenium WebDriver instance with a specific window size and position
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
        chrome_options.add_argument(f"--window-position={window_position[0]},{window_position[1]}")
        self.driver = webdriver.Chrome(options=chrome_options)

    def login(self):
        # Open Facebook
        self.driver.get("https://www.facebook.com/")

        # Set cookies
        cookies = [
            # Existing cookies...
        ]

        for cookie in cookies:
            self.driver.add_cookie(cookie)

        # Refresh the page to apply the cookies
        self.driver.refresh()

    def resize_tab_and_content(self, tab_size):
        # Resize the entire browser window (including content)
        self.driver.set_window_size(tab_size[0], tab_size[1])
        
        # Resize the content within the tab
        self.driver.execute_script(f"document.body.style.zoom = {tab_size[1] / 200}")

    def close(self):
        # Close the browser window
        self.driver.quit()

class Page:
    def __init__(self, user):
        self.user = user

    def create_facebook_page(self):
        # Navigate to the desired page
        self.user.driver.get("https://www.facebook.com/pages/creation/?ref_type=launch_point")

        # Wait for some time to see the result (you can replace this with additional actions)
        time.sleep(5)

def run_scenario(user, page):
    user.login()
    user.resize_tab_and_content((50, 200))  # Set the desired size for the tab and content
    page.create_facebook_page()
    # Additional actions as needed
    user.close()

def main():
    monitors = get_monitors()

    if not monitors:
        raise ValueError("No monitors found.")

    monitor = monitors[0]  # Assuming the first monitor, you can adjust it as needed

    screen_width = monitor.width
    screen_height = monitor.height

    rows = 0  # Number of rows
    columns = 3  # Number of tabs per row

    threads = []

    for i in range(10):  # Creating 10 threads for the demonstration
        col = i % columns
        if col == 0:
            rows += 1
        window_position = (col * screen_width // columns, (rows - 1) * screen_height // rows)
        user = User((50, 200), window_position)
        page = Page(user)
        thread = threading.Thread(target=run_scenario, args=(user, page))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
