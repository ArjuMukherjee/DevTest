import os
import time
import threading

def delete_temp_file_after_time(file_path, delay=60):
    def delayed_delete():
        time.sleep(delay)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} deleted.")

    threading.Thread(target=delayed_delete).start()
