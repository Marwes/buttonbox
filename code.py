import keypad
import board
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard, find_device
from adafruit_hid.keycode import Keycode

key_pins = (
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

keys = keypad.Keys(key_pins, value_when_pressed=False, pull=True)


class BitmapKeyboard(Keyboard):
    def __init__(self, devices):
        device = find_device(devices, usage_page=0x1, usage=0x6)

        try:
            device.send_report(b'\0' * 16)
        except ValueError:
            print("found keyboard, but it did not accept a 16-byte report. check that boot.py is installed properly")

        self._keyboard_device = device

        # report[0] modifiers
        # report[1:16] regular key presses bitmask
        self.report = bytearray(16)

        self.report_modifier = memoryview(self.report)[0:1]
        self.report_bitmap = memoryview(self.report)[1:]

    def _add_keycode_to_report(self, keycode):
        modifier = Keycode.modifier_bit(keycode)
        if modifier:
            # Set bit for this modifier.
            self.report_modifier[0] |= modifier
        else:
            self.report_bitmap[keycode >> 3] |= 1 << (keycode & 0x7)

    def _remove_keycode_from_report(self, keycode):
        modifier = Keycode.modifier_bit(keycode)
        if modifier:
            # Set bit for this modifier.
            self.report_modifier[0] &= ~modifier
        else:
            self.report_bitmap[keycode >> 3] &= ~(1 << (keycode & 0x7))

    def release_all(self):
        for i in range(len(self.report)):
            self.report[i] = 0
        self._keyboard_device.send_report(self.report)


kbd = BitmapKeyboard(usb_hid.devices)

keymap = [
    # Unused
    Keycode.P, Keycode.M,
    # Movement
    Keycode.A, Keycode.S, Keycode.D,
    # Jump
    Keycode.W,
    # Options
    Keycode.SPACE, Keycode.ENTER,
    # Attack buttons
    Keycode.J, Keycode.U, Keycode.Q, Keycode.I, Keycode.L, Keycode.O,
    # Extra
    Keycode.ESCAPE, Keycode.TAB,
]
keymap.reverse()

# keymap = [
#     Keycode.TAB, Keycode.ESCAPE,
#     Keycode.ENTER, Keycode.SPACE,
#     Keycode.Q,
#     Keycode.M, Keycode.P,
#     Keycode.L, Keycode.O, Keycode.I, Keycode.U, Keycode.J,
#     Keycode.D, Keycode.S, Keycode.A, Keycode.W,
# ]

while True:
    ev = keys.events.get()
    if ev is not None:
        if ev.key_number >= len(keymap):
            print("Key", ev.key_number, "is not mapped")
            continue
        key = keymap[ev.key_number]
        if ev.pressed:
            kbd.press(key)
        else:
            kbd.release(key)
