+++
title = "Building dogsbod: A quadruped robot"
date = 2026-03-13
tags = ["3D printing", "rp2040", "robotics", "highlights"]
categories = ["Writing"]
thumbnail = "dogsbod/dogsbod.png"
description = "I built a robot dog. This took me on a big adventure across whole new domains: mechanical engineering, 3D printing, robotics, PCB design and electronics."
+++

![Dogsbod v2](dogsbod/dogsbod.png)

## Goal: Build a small, cheap and stupid quadruped robot dog

How hard could it be?

As it turns out, it is suprisingly difficult! The process ended up with me learning CAD, mechanical engineering, 3D printing, PCB design, PCB manufacturing and electrical engineering. 

Though in the end I did manage to get it walking:

![Dogsbod v1 Walk and Turn Test](dogsbod/dogsbod_walknturn.mp4)

I am still learning even now, there is still a lot to further improve and I have a new found appreciation and respect for those building and pursuing electronics, manufacturing and robotics as a result.

Come and join me on an adventure as we learn what it takes to build the simplest, cheapest robot dog I can come up with.

## Initial Plan

In January I was [inspired](https://www.instructables.com/GoodBoy-3D-Printed-Arduino-Robot-Dog/) by a [bunch of](https://www.instructables.com/ESP32-Small-Robot-Dog/) [projects online](https://www.instructables.com/DogBot-V2-Make-Your-Own-Quadruped-Robot-From-Scrat/) and [various](https://www.youtube.com/watch?v=VhUvoV5XyRg) [youtube](https://www.youtube.com/watch?v=iXmrPoqd8gs) videos explaining the process of creating a robot dog, and this got me excited enough to want to give it a try myself.

At the time of starting this project I didn't have a 3D printer and I hadn't used CAD software before, though I know how to use Blender really well.

The idea was to try and build a robot using the cheapest servos I could find, mostly for power and budget reasons, and then try to fit the robot's movement within those limits. I wanted to be able to run the robot from 4xAA batteries because I didn't want to jump straight to high power electronics.

I started out with this very simple BOM:

- [Miuzei 9g Metal Gear Micro Servo Motors](https://www.amazon.co.uk/gp/product/B0DGD55Q71?smid=ADX1E4W4DEI4I&th=1) x8
  - 1.8kg/cm torque @ 4.8V
  - 13.5g mass
- [Waveshare Pico Servo Driver](https://www.waveshare.com/wiki/Pico-Servo-Driver)
- [4x NiMH AA batteries](https://www.amazon.co.uk/AmazonBasics-Capacity-Pre-Charged-Rechargeable-Batteries-Black)
- [4x AA battery holder](https://thepihut.com/products/4-x-aa-battery-holder-with-on-off-switch)
- [Pack of M3 Nuts + Bolts](https://www.amazon.co.uk/dp/B0DC4688ZT)
- [Raspberry Pi Pico W](https://thepihut.com/products/raspberry-pi-pico-w)
- 3D printer filament

I also came up with an initial mass budget of ~20g per leg.
```
1.8kg/cm torque

Pico + Servo Driver = 34g
Servos = 13.5g x 8 = 108g
NiMH x 4 = 30g x 4 = 120g
Battery holder 25g (assumed) = 25g

==> 287g without any plastic

assume 50% torque available because bad quality. 900g/cm.
900g/cm * 4 legs = 3600g/cm
3600g/cm / 10cm distance along each leg = 360g budget - 287g = 73g

19.4g per leg
```

I did some really rough power calculations.

```
Battery pack: 4× AA NiMH in series

    Nominal voltage: 4⋅1.2=4.8 V
    Typical capacity: about 2000–2500 mAh for decent AAs
    In series, voltage adds, capacity stays the same → call it a 2–2.5 Ah, 4.8 V pack

Servos: 8× SG90

    Rated operating voltage: about 3.5–6 V
    Stall current is 700 mA
    8 servos could theoretically hit 5–6 A if they all slam into stall at once
```

I found the 5-6A result quite worrying, but hoped that if they didn't all stall at the same time it would be ok? I pay for this mistake later on, but I do get further than I expected!

## CAD Design

I then set about designing the robot in CAD. I initially tried to learn Freecad, but bounced off the software. They keep updating it and I keep bouncing off it, but it does seem like freecad development has really progressed this year. I think Freecad will win in the end, it currently feels like Blender just before the 2.8 UI overhaul.

So in the end I chose to learn solidworks instead.

Solidworks at its core is great and powerful CAD software. However the '3D experience platform' is obnoxious, and asks you to login every single time you open it. 

Luckily you can still save locally and check that stuff into Git, and again the core CAD software itself is really good.

After a week or so learning Solidworks I came up with this design:

![Dogsbod v1 CAD Design](dogsbod/dogsbod_cad.png)

This allowed me to calculate the final mass budget:
```
Each leg is 24.19g x4 = 96.76g
Body is = 36.8g
Battery box is = 22.37g
=> 155.93g
Pico + Servo Driver = 34g
Servos = 13.5g x 8 = 108g
NiMH x 4 = 30g x 4 = 120g
=> 417.9g

360g budget => 15% over budget.
```

I was 5g over my intended mass budget, though given I had reduced the torque by 50% to arrive at that original budget I decided this was good enough to proceed. So if I naively assume the servos will deliver their actual torque specs then I'm only at 58% of the mass budget.

## Electronics and Initial Firmware

On the electronics side, I set myself an initial goal of getting the waveshare servo board up and running, driving a single servo. 

I wired up another Pico I had lying around to act as a [Pico Debugger Probe](https://www.raspberrypi.com/documentation/microcontrollers/debug-probe.html) which makes flashing the firmware significantly less annoying: you can set things up in VS code to the point where mashing F5 compiles, flashes and then attaches the debugger. So you can have full debugging access, which I'm very used to/spoiled with from my game console development experience. Debuggers are a very powerful tool to have available, and are worth fighting for to gain that low level understanding of what's going on.

For that reason it's also really worth spending the time to setup UART so you can print what is going on inside the chip as well. Wiring UART correctly is a complete nightmare, and I always seem to get it the wrong way round. I don't think I'm the only one!

My first attempt to get the waveshare board to move a servo didn't work, and in the process of figuring out why I accidentally shorted the 5V output and GND together with my multimeter probes. There was a terrifying moment where I saw an arc between the pins and then power to the whole board was lost, which I think was the efuse within my PC's USB ports. Luckily I didn't fry my PC's USB ports or even worse the whole PC itself but I **did** fry the buck converter on the waveshare board.

This was confirmed after a bit of (much more careful!) multimeter probing around the buck converter pins when connected to 5V.

In the end the problem turned out to be that I'd forgotten to turn on the 'SERVO POWER' switch on the waveshare board! ARGH. In my defence the schematic of my r1 waveshare board I'd bought many years ago had been updated to a new revision with better layout + power options so I don't actually have the schematic of the board I have.

As a result I learned that it's a great idea to check in the datasheets for the components you're working with into Git. Please do this instead of assuming your favourite component will be archived for you forever!

The firmware required to drive a servo really is simple. You [wobble the data pin](https://en.wikipedia.org/wiki/Pulse-width_modulation) the servo is connected at the rate that that the servo chip wants you to wobble the pin at. For the Miuzei servos I'm using they want a pulse width modulation (PWM) working pulse width of 500-2500 usec.
```c
#include "hardware/pwm.h"

static void set_servo_angle(int pin, int angle) {
    if (angle <= 0) angle = 0;
    if (angle >= 180) angle = 180;
    if (pin <= 0) pin = 0;
    if (pin >= NUM_SERVOS) pin = NUM_SERVOS - 1;
    pin += SERVO_MIN_PIN;
    uint32_t pulse_us = 500 + (angle * (2500 - 500)) / 180;
    uint32_t slice = pwm_gpio_to_slice_num(pin);
    uint32_t channel = pwm_gpio_to_channel(pin);
    pwm_set_chan_level(slice, channel, pulse_us);
}
```

With this I was able to get a bunch of servos moving about.

## IK Solvers and Five Bar Linkages



## Picking a 3D Printer

It was at this point that I decided to invest in a 3D printer. I went for a [Bambu Lab P1S](https://uk.store.bambulab.com/products/p1s). Honestly it's a great 3D printer. I've not had to do any maintenance on it to date, the Bambu Handy app works great, the slicer software works brilliantly. The print failures that I have had have mostly been user error or my down to my often damp garage - thanks english weather! My goal was to have a tool not to do 3D printing as a hobby, and it is perfect for this.

I know there are concerns about the steps Bambu Labs have taken more recently to lock down the ecosystem etc but my CAD designs are not important/secret enough for me to really worry about this. I do turn the machine off at the wall when I'm not using it. It's great that there is a local developer mode that I *could* turn on if I want to actually take control, but convenience and *its a tool just should 'just work'* wins for me for now.

