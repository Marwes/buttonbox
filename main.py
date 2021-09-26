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
    # Extra
    1, 2,
    # Attack buttons
    3, 4, 5, 6, 7, 8,
    # Options
    9, 10,
    # Movement
    11, 12, 13, 14,
    # Unused
    15, 16
]

button_states = [False for x in gamepad_buttons]


def is_movement(gamepad_button_num):
    return 11 <= gamepad_button_num <= 14


while True:
    # Buttons are grounded when pressed (.value = False).
    for i, button in enumerate(buttons):
        gamepad_button_num = gamepad_buttons[i]
        if is_movement(gamepad_button_num):
            continue
        if button.value and button_states[i]:
            button_states[i] = False
            gamepad.release_buttons(gamepad_button_num)
        elif not button.value and not button_states[i]:
            button_states[i] = True
            gamepad.press_buttons(gamepad_button_num)

    LEFT = 13
    RIGHT = 11
    UP = 10
    DOWN = 12
    x = None
    y = None
    # SOCD cleaner
    # print(not buttons[LEFT].value, not buttons[RIGHT].value,
    #      not buttons[UP].value, not buttons[DOWN].value)
    if not buttons[LEFT].value:
        if not buttons[RIGHT].value:
            x = 0
        else:
            x = -127
    elif not buttons[RIGHT].value:
        x = 127
    else:
        x = 0

    if not buttons[UP].value:
        y = -127
    elif not buttons[DOWN].value:
        y = 127
    else:
        y = 0

    gamepad.move_joysticks(x, y)

    time.sleep(0.001)
