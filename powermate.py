#!/usr/bin/env python3
import evdev
from evdev import ecodes, UInput
import sys
import time

VENDOR_ID = 0x077d
PRODUCT_ID = 0x0410
DEBOUNCE_TIME = 0.2

# X11 key codes for volume control
KEY_VOLUMEDOWN = 114  # XF86AudioLowerVolume
KEY_VOLUMEUP = 115    # XF86AudioRaiseVolume
KEY_MUTE = 113        # XF86AudioMute

class PowerMateController:
    def __init__(self):
        self.device = self.find_powermate()
        if not self.device:
            raise Exception("PowerMate device not found")
            
        print(f"\nStarting PowerMate control on {self.device.name} at {self.device.path}")
        self.last_click_time = 0
        
        # Create virtual input device for media keys
        capabilities = {
            evdev.ecodes.EV_KEY: [
                KEY_VOLUMEDOWN,
                KEY_VOLUMEUP,
                KEY_MUTE
            ]
        }
        self.uinput = UInput(capabilities, name="PowerMate Media Controls")

    def find_powermate(self):
        """Find the PowerMate device among input devices."""
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            try:
                if (device.info.vendor == VENDOR_ID and 
                    device.info.product == PRODUCT_ID):
                    return device
            except:
                continue
        return None

    def simulate_key_press(self, key_code):
        """Simulate a media key press and release."""
        # Press key
        self.uinput.write(ecodes.EV_KEY, key_code, 1)
        self.uinput.syn()
        time.sleep(0.1)  # Small delay between press and release
        # Release key
        self.uinput.write(ecodes.EV_KEY, key_code, 0)
        self.uinput.syn()
    
    def adjust_volume(self, direction):
        """Adjust volume by simulating media key press."""
        if direction > 0:
            self.simulate_key_press(KEY_VOLUMEUP)
            print("Volume up")
        else:
            self.simulate_key_press(KEY_VOLUMEDOWN)
            print("Volume down")
    
    def toggle_mute(self):
        """Toggle mute by simulating mute key press."""
        self.simulate_key_press(KEY_MUTE)
        print("Mute toggled")

    def handle_events(self):
        """Main event loop for handling PowerMate input."""
        print("\nControls:")
        print("- Rotate clockwise: Volume up")
        print("- Rotate counter-clockwise: Volume down")
        print("- Click: Toggle mute")
        print("\nListening for events... (Press Ctrl+C to exit)\n")
        
        try:
            for event in self.device.read_loop():
                if event.type == ecodes.EV_REL:  # Rotation events
                    self.adjust_volume(event.value)
                elif event.type == ecodes.EV_KEY and event.value == 1:  # Button press
                    current_time = time.time()
                    if current_time - self.last_click_time > DEBOUNCE_TIME:
                        self.toggle_mute()
                        self.last_click_time = current_time
                    
        except KeyboardInterrupt:
            print("\nExiting PowerMate controller")
        except Exception as e:
            print(f"Error in event loop: {e}", file=sys.stderr)
            raise
        finally:
            self.uinput.close()

def main():
    try:
        controller = PowerMateController()
        controller.handle_events()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()