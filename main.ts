input.onButtonPressed(Button.A, function () {
    IsOverride = !(IsOverride)
    if (IsOverride) {
        LedLightStatus = true
        basic.showIcon(IconNames.Square)
    } else if (LedLightStatus) {
        basic.showIcon(IconNames.Square)
    } else {
        basic.showLeds(`
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            `)
    }
    datalogger.log(
    datalogger.createCV("Event", 0),
    datalogger.createCV("Value", IsOverride),
    datalogger.createCV("Light", input.lightLevel()),
    datalogger.createCV("Cycles", LightOnCount)
    )
})
input.onButtonPressed(Button.B, function () {
    LightOnThreshold = input.lightLevel()
    basic.showString("C")
    basic.showNumber(LightOnThreshold)
    basic.pause(500)
    if (input.lightLevel() < LightOnThreshold) {
        LedLightStatus = true
        basic.showIcon(IconNames.Square)
    } else {
        basic.showLeds(`
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            `)
        LedLightStatus = false
    }
    datalogger.log(
    datalogger.createCV("Event", 0),
    datalogger.createCV("Value", LightOnThreshold),
    datalogger.createCV("Light", LightOnThreshold),
    datalogger.createCV("Cycles", LightOnCount)
    )
})
// On shake gesture, shows (P) for power, shows the light on count, pauses for 700ms to avoid bugs, and shows either the sun or moon, depending if the led light status variable or the is override variable true
input.onGesture(Gesture.Shake, function () {
    basic.showString("P")
    basic.showNumber(LightOnCount)
    basic.pause(700)
    if (LedLightStatus || IsOverride) {
        basic.showIcon(IconNames.Square)
    } else {
        basic.showLeds(`
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            `)
    }
})
// Sets the value at which the light will turn on at (from 0-255) then sets the data logging columns
let loop_counter = 0
let current = 0
let LightOnCount = 0
let LedLightStatus = false
let IsOverride = false
let LightOnThreshold = 0
LightOnThreshold = 110
datalogger.setColumnTitles(
"Event",
"Light",
"Light"
)
basic.forever(function () {
    current = input.lightLevel()
    if (!(IsOverride)) {
        if (current < LightOnThreshold && !(LedLightStatus)) {
            LedLightStatus = true
            LightOnCount += 1
            datalogger.log(
            datalogger.createCV("Event", "AutoOn"),
            datalogger.createCV("Value", 1),
            datalogger.createCV("Light", current),
            datalogger.createCV("Cycles", LightOnCount)
            )
        } else if (current > LightOnThreshold + 10 && LedLightStatus) {
            LedLightStatus = false
            datalogger.log(
            datalogger.createCV("Event", "AutoOff"),
            datalogger.createCV("Value", 0),
            datalogger.createCV("Light", current),
            datalogger.createCV("Cycles", LightOnCount)
            )
        }
    }
    if (LedLightStatus || IsOverride) {
        basic.showIcon(IconNames.Square)
    } else {
        basic.showLeds(`
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            `)
    }
    loop_counter += 1
    if (loop_counter >= 5) {
        datalogger.log(
        datalogger.createCV("Event", "Ambient"),
        datalogger.createCV("Value", current),
        datalogger.createCV("Light", current),
        datalogger.createCV("Cycles", LightOnCount)
        )
        loop_counter = 0
    }
    basic.pause(150)
})
