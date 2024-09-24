import psutil
import time
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(filename='vscode_usage.log',
                    level=logging.DEBUG, 
                    format='%(asctime)s - %(message)s',
                    filemode='w') 
logger = logging.getLogger(__name__)

# Function to get VSCode process
def get_vscode_process():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'code' in proc.info['name'].lower():  # VSCode's executable is 'Code' or 'code'
            return proc
    return None

def track_vscode_open_close():
    vscode_process = None
    open_time = None
    
    try:
        while True:
            current_vscode_process = get_vscode_process()
            
            if current_vscode_process:
                if not vscode_process:
                    # VSCode just opened
                    open_time = datetime.now()
                    logger.info(f"VSCode opened at {open_time}")
                    vscode_process = current_vscode_process
            else:
                if vscode_process:
                    # VSCode just closed
                    close_time = datetime.now()
                    usage_time = close_time - open_time
                    logger.info(f"VSCode closed at {close_time}, Total time open: {usage_time}")
                    vscode_process = None
            time.sleep(1)  # Check every second for better responsiveness
    except KeyboardInterrupt:
        logger.info("Tracking stopped.")

if __name__ == "__main__":
    track_vscode_open_close()