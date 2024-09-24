import psutil
import time
from datetime import datetime
import logging
import getpass
import os

open_time = None

# Setup logging
logging.basicConfig(filename='vscode_usage_and_process.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(message)s',
                    filemode='w')
logger = logging.getLogger(__name__)

# Get the current user's username
current_user = getpass.getuser()

# Function to get VSCode process
def get_vscode_process():
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        try:
            # VSCode process name is typically 'Code' or 'code'
            if 'code helper' == proc.info['name'].lower():
                # Check the full executable path for additional accuracy
                # exe_path = proc.info.get('exe', '')
                # if exe_path and 'code' in os.path.basename(exe_path).lower():
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return None

# Function to track when an application opens
# def track_application_open():
#     vscode_process = None
#     # global open_time
 
    
#     try:
#         while True:
#             current_vscode_process = get_vscode_process()
#             # print(current_vscode_process)
            
#             if current_vscode_process:
#                 if not vscode_process:
#                     # VSCode just opened
#                     open_time = datetime.now()
#                     logger.info(f"VSCode opened at {open_time}")
#                     vscode_process = current_vscode_process
            
#             time.sleep(1)  # Check every second for better responsiveness
#     except KeyboardInterrupt:
#         logger.info("Tracking open applications stopped.")

# Function to track when an application closes
def track_application_close():
    vscode_process = None
    current_vscode_process = None
    global open_time
    
    
    try:
        while True:
            current_vscode_process = get_vscode_process()
            print(current_vscode_process)
            print(vscode_process)
            if current_vscode_process:
                if not vscode_process:
                    # New VSCode process detected, start timing
                    vscode_process = current_vscode_process
                    open_time = datetime.now() 
                    logger.info(f"VSCode opened at {open_time}") # Reset open time when a new process is found
            else:
                # VSCode just closed
                print('aaaa')
                close_time = datetime.now()
                if not open_time:
                    print("wtf did you do")
                    continue
                usage_time = close_time - open_time
                print(usage_time)
                logger.info(f"VSCode closed at {close_time}, Total time open: {usage_time}")
                vscode_process = None  # Reset the process tracker
        
            time.sleep(1)  # Check every second for better responsiveness
    except KeyboardInterrupt:
        logger.info("Tracking closed applications stopped.")

if __name__ == "__main__":
    # Uncomment the function you want to run
    # track_application_open()
    track_application_close()
