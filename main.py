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
    # Movement UP, DOWN, RIGHT, LEFT
    11, 12, 13, 14,
    # Unused
    15, 16
]

button_states = [False for x in gamepad_buttons]


def is_movement(gamepad_button_num):
    return 11 <= gamepad_button_num <= 14


def handle_button(i, button_down):
    gamepad_button_num = gamepad_buttons[i]

    if not button_down and button_states[i]:
        button_states[i] = False
        gamepad.release_buttons(gamepad_button_num)
    elif button_down and not button_states[i]:
        button_states[i] = True
        gamepad.press_buttons(gamepad_button_num)


USE_DPAD = True

while True:
    # Buttons are grounded when pressed (.value = False).
    for i, button in enumerate(buttons):
        gamepad_button_num = gamepad_buttons[i]

        if is_movement(gamepad_button_num):
            continue

        handle_button(i, not button.value)

    LEFT = 13
    RIGHT = 11
    UP = 10
    DOWN = 12
    x = None
    y = None
    # SOCD cleaner
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

    if USE_DPAD:
        if x > 0:
            handle_button(RIGHT, True)
            handle_button(LEFT, False)
        elif x < 0:
            handle_button(RIGHT, False)
            handle_button(LEFT, True)
        else:
            handle_button(RIGHT, False)
            handle_button(LEFT, False)

        if y > 0:
            handle_button(DOWN, True)
            handle_button(UP, False)
        elif y < 0:
            handle_button(DOWN, False)
            handle_button(UP, True)
        else:
            handle_button(DOWN, False)
            handle_button(UP, False)
    else:
        gamepad.move_joysticks(x, y)

    time.sleep(0.001)
