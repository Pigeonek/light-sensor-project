def on_button_pressed_a():
    global IsOverrideTrue
    IsOverrideTrue = not (IsOverrideTrue)
    if IsOverrideTrue:
        basic.show_icon(IconNames.SQUARE)
    else:
        basic.show_leds("""
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            """)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    global LightOnThreshold
    LightOnThreshold = input.light_level()
    basic.show_string("T")
    basic.show_number(LightOnThreshold)
    basic.pause(1000)
    basic.show_leds("""
        # . # . #
        . # # # .
        # # # # #
        . # # # .
        # . # . #
        """)
input.on_button_pressed(Button.B, on_button_pressed_b)

def on_gesture_shake():
    basic.show_string("C")
    basic.show_number(LightOnCount)
    basic.pause(1000)
    if LedLightStatus:
        basic.show_icon(IconNames.SQUARE)
        basic.show_leds("""
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            """)
    else:
        pass
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

LedLightStatus = False
LightOnCount = 0
IsOverrideTrue = False
LightOnThreshold = 0
LightOnThreshold = 80

def on_forever():
    global LedLightStatus, LightOnCount
    if not (IsOverrideTrue):
        if input.light_level() < LightOnThreshold and not (LedLightStatus):
            LedLightStatus = True
            LightOnCount += 1
        elif input.light_level() > LightOnThreshold + 10 and LedLightStatus:
            LedLightStatus = False
        if LedLightStatus or IsOverrideTrue:
            basic.show_icon(IconNames.SQUARE)
            pins.digital_write_pin(DigitalPin.P0, 1)
        else:
            pins.digital_write_pin(DigitalPin.P0, 0)
            basic.show_leds("""
                # . # . #
                . # # # .
                # # # # #
                . # # # .
                # . # . #
                """)
        basic.pause(100)
basic.forever(on_forever)
