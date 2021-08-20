import board
import usb_hid
import digitalio
import time
from gamepad import Gamepad

button_pins = (
    board.GP0,
    board.GP1,
    board.GP2,
    board.GP3,
    board.GP4,
    board.GP5,
    board.GP6,
    board.GP7,
    board.GP8,
    board.GP9,
    board.GP10,
    board.GP11,
    board.GP12,
    board.GP13,
    board.GP14,
    board.GP15,
)

buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]
for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP

gamepad = Gamepad(usb_hid.devices)

gamepad_buttons = [
    # Unused
    1, 2,
    # Movement
    3, 4, 5,
    # Jump
    6,
    # Options
    7, 8,
    # Attack buttons
    9, 10, 11, 12, 13, 14,
    # Extra
    15, 16
]

button_states = [False for x in gamepad_buttons]

while True:
    # Buttons are grounded when pressed (.value = False).
    for i, button in enumerate(buttons):
        gamepad_button_num = gamepad_buttons[i]
        if button.value and button_states[i]:
            button_states[i] = False
            gamepad.release_buttons(gamepad_button_num)
        elif not button.value and not button_states[i]:
            button_states[i] = True
            gamepad.press_buttons(gamepad_button_num)
    time.sleep(0.001)
