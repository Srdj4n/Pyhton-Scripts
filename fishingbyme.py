import sounddevice as sd
import numpy as np
import keyboard
import time
import threading

# Event to signal that sound was detected
sound_event = threading.Event()

# Function to detect sound events
def detect_sound(indata, frames, time, status):
    # Calculate the root mean square (RMS) amplitude
    rms = np.sqrt(np.mean(indata**2))
    # Set a threshold for sound detection
    threshold = 0.02  # Adjust this value as needed
    if rms > threshold:
        # Sound detected, set the event
        sound_event.set()

# Function to run the script
def run_script():
    # Press '2' key
    print("Pressing '2'...")
    keyboard.press('2')
    time.sleep(0.1)  # Adjust this value as needed
    keyboard.release('2')
    # Wait for 3 seconds before listening for sound events
    print("Waiting for 3 seconds before listening for sound...")
    time.sleep(3)
    # Reset the event for the next iteration
    sound_event.clear()
    # Query supported sample rates for the input device
    device_info = sd.query_devices(31, 'input')
    supported_samplerates = device_info['default_samplerate']
    # Choose a sample rate from the supported list
    if isinstance(supported_samplerates, float):
        samplerate = supported_samplerates
    else:
        samplerate = 44100
    print(f"Using sample rate: {samplerate}")
    # Start listening for sound events
    with sd.InputStream(device=31, callback=detect_sound, channels=1, samplerate=samplerate):
        print("Listening for sound events...")
        # Wait for sound to be played or for 3 seconds
        if sound_event.wait(timeout=20):
            # Sound detected, press '1' key
            print("Sound detected. Pressing '1'...")
            time.sleep(0.5)
            keyboard.press('1')
            time.sleep(0.1)  # Adjust this value as needed
            keyboard.release('1')
        else:
            print("No sound detected within 3 seconds.")

# Run the script
print("Script started.")
while True:
    run_script()
    # Wait before repeating the process
    time.sleep(3.5)
