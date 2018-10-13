from pynput import keyboard

def on_press(key):
    if key == keyboard.Key.esc:
        listener.stop()
    else:
        print(ord(getattr(key, 'char', '0')))

controller = keyboard.Controller()
with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()