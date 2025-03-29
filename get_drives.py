import os
import platform

def get_available_drives():
    """
    Returns a list of available drives on the system.
    Works across Windows, macOS, and Linux.
    """
    system = platform.system()
    
    if system == 'Windows':
        # For Windows
        import string
        from ctypes import windll
        
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        
        # Check each drive letter
        for letter in string.ascii_uppercase:
            # Check if the bit corresponding to this drive is set
            if bitmask & 1:
                drives.append(f"{letter}:\\")
            bitmask >>= 1
            
        return drives
        
    elif system == 'Darwin':  # macOS
        # For macOS, typically mounted volumes are in /Volumes
        return [os.path.join('/Volumes', item) for item in os.listdir('/Volumes')]
        
    else:  # Linux and other Unix-like systems
        # For Linux, check /mnt and /media directories
        drives = []
        
        # Check common mount points
        for mount_point in ['/mnt', '/media']:
            if os.path.exists(mount_point):
                drives.extend([os.path.join(mount_point, item) for item in os.listdir(mount_point)])
                
        # You might also want to parse /proc/mounts or use subprocess to call 'df'
        return drives

# Example usage
if __name__ == "__main__":
    drives = get_available_drives()
    print("Available drives:")
    for drive in drives:
        print(f" - {drive}")