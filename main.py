def on_button_pressed_a():
    global IsOverride, LedLightStatus
    IsOverride = not (IsOverride)
    if IsOverride:
        LedLightStatus = True
        pins.digital_write_pin(DigitalPin.P0, 1)
        basic.show_icon(IconNames.SQUARE)
    elif LedLightStatus:
        pins.digital_write_pin(DigitalPin.P0, 1)
        basic.show_icon(IconNames.SQUARE)
    else:
        pins.digital_write_pin(DigitalPin.P0, 0)
        basic.show_leds("""
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            """)
    datalogger.log(datalogger.create_cv("Event", 0),
        datalogger.create_cv("Value", IsOverride),
        datalogger.create_cv("Light", input.light_level()),
        datalogger.create_cv("Cycles", LightOnCount))
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    global LightOnThreshold, LedLightStatus
    LightOnThreshold = input.light_level()
    basic.show_string("C")
    basic.show_number(LightOnThreshold)
    basic.pause(500)
    if input.light_level() < LightOnThreshold:
        LedLightStatus = True
        pins.digital_write_pin(DigitalPin.P0, 1)
        basic.show_icon(IconNames.SQUARE)
    else:
        LedLightStatus = False
        pins.digital_write_pin(DigitalPin.P0, 0)
        basic.show_leds("""
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            """)
    datalogger.log(datalogger.create_cv("Event", "Calibration"),
        datalogger.create_cv("Value", LightOnThreshold),
        datalogger.create_cv("Light", LightOnThreshold),
        datalogger.create_cv("Cycles", LightOnCount))
input.on_button_pressed(Button.B, on_button_pressed_b)

# On shake gesture, shows (P) for power, shows the light on count, pauses for 700ms to avoid bugs, and shows either the sun or moon, depending if the led light status variable or the is override variable true

def on_gesture_shake():
    basic.show_string("P")
    basic.show_number(LightOnCount)
    basic.pause(700)
    if LedLightStatus or IsOverride:
        basic.show_icon(IconNames.SQUARE)
    else:
        basic.show_leds("""
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            """)
input.on_gesture(Gesture.SHAKE, on_gesture_shake)

# Sets the value at which the light will turn on at (from 0-255) then sets the data logging columns
loop_counter = 0
current = 0
LightOnCount = 0
LedLightStatus = False
IsOverride = False
LightOnThreshold = 0
LightOnThreshold = 110
datalogger.set_column_titles("Event", "Light", "Light")

def on_forever():
    global current, LedLightStatus, LightOnCount, loop_counter
    current = input.light_level()
    if not (IsOverride):
        if current < LightOnThreshold and not (LedLightStatus):
            LedLightStatus = True
            LightOnCount += 1
            datalogger.log(datalogger.create_cv("Event", "AutoOn"),
                datalogger.create_cv("Value", 1),
                datalogger.create_cv("Light", current),
                datalogger.create_cv("Cycles", LightOnCount))
        elif current > LightOnThreshold + 10 and LedLightStatus:
            LedLightStatus = False
            datalogger.log(datalogger.create_cv("Event", "AutoOff"),
                datalogger.create_cv("Value", 0),
                datalogger.create_cv("Light", current),
                datalogger.create_cv("Cycles", LightOnCount))
    if LedLightStatus or IsOverride:
        pins.digital_write_pin(DigitalPin.P0, 1)
        basic.show_icon(IconNames.SQUARE)
    else:
        pins.digital_write_pin(DigitalPin.P0, 0)
        basic.show_leds("""
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            """)
    loop_counter += 1
    if loop_counter >= 5:
        datalogger.log(datalogger.create_cv("Event", "Ambient"),
            datalogger.create_cv("Value", current),
            datalogger.create_cv("Light", current),
            datalogger.create_cv("Cycles", LightOnCount))
        loop_counter = 0
    basic.pause(150)
basic.forever(on_forever)
