input.onButtonPressed(Button.A, function () {
    IsOverrideTrue = !(IsOverrideTrue)
    if (IsOverrideTrue) {
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
input.onButtonPressed(Button.B, function () {
    LightOnThreshold = input.lightLevel()
    basic.showString("T")
    basic.showNumber(LightOnThreshold)
    basic.pause(1000)
    basic.showLeds(`
        # . # . #
        . # # # .
        # # # # #
        . # # # .
        # . # . #
        `)
})
input.onGesture(Gesture.Shake, function () {
    basic.showString("C")
    basic.showNumber(LightOnCount)
    basic.pause(1000)
    if (LedLightStatus) {
        basic.showIcon(IconNames.Square)
        basic.showLeds(`
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            `)
    } else {
    	
    }
})
let LedLightStatus = false
let LightOnCount = 0
let IsOverrideTrue = false
let LightOnThreshold = 0
LightOnThreshold = 80
basic.forever(function () {
    if (!(IsOverrideTrue)) {
        if (input.lightLevel() < LightOnThreshold && !(LedLightStatus)) {
            LedLightStatus = true
            LightOnCount += 1
        } else if (input.lightLevel() > LightOnThreshold + 10 && LedLightStatus) {
            LedLightStatus = false
        }
        if (LedLightStatus || IsOverrideTrue) {
            basic.showIcon(IconNames.Square)
            pins.digitalWritePin(DigitalPin.P0, 1)
        } else {
            pins.digitalWritePin(DigitalPin.P0, 0)
            basic.showLeds(`
                # . # . #
                . # # # .
                # # # # #
                . # # # .
                # . # . #
                `)
        }
        basic.pause(100)
    }
})
