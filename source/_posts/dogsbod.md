+++
title = "Building dogsbod: A quadruped robot"
date = 2026-03-13
tags = ["3D printing", "rp2040", "robotics", "highlights"]
categories = ["Writing"]
thumbnail = "dogsbod/dogsbod.png"
description = "I built a robot dog. This took me on a big adventure across whole new domains: mechanical engineering, 3D printing, robotics, PCB design and electronics."
+++

![Dogsbod v2](dogsbod/dogsbod.png)

Goal: Build a small, cheap and stupid quadruped robot dog. How hard could it be?

---

As it turns out, suprisingly difficult! Come and join me on an adventure as we learn what it takes to build the simplest robot dog possible. The process ended up with me learning CAD, mechanical engineering, 3D printing, PCB design and power electronics. 

I am still learning even now and have a new found appreciation for electronics, manufacturing and robotics as a result.

## Initial Plan

In January I was [inspired](https://www.instructables.com/GoodBoy-3D-Printed-Arduino-Robot-Dog/) by a [bunch of](https://www.instructables.com/ESP32-Small-Robot-Dog/) [projects online](https://www.instructables.com/DogBot-V2-Make-Your-Own-Quadruped-Robot-From-Scrat/) and [various](https://www.youtube.com/watch?v=VhUvoV5XyRg) [youtube](https://www.youtube.com/watch?v=iXmrPoqd8gs) videos explaining the process of creating a robot dog, and this got me excited enough to want to give it a try myself.

At the time of starting this project I didn't have a 3D printer and I hadn't used CAD software before, though I had spent a lot of time in Blender.

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

I also did some really rough power calculations, but from a position of relative ignorance!

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

I found the 5-6A result quite worrying, but hoped that if they didn't all stall at the same time it would be ok? I pay for this mistake later on, but I get further than you think! :D

## CAD Design

I then set about designing the robot in CAD. I initially tried to learn Freecad, but bounced off the software. I keep bouncing off it, but it does seem like freecad development has really progressed this year. I think Freecad will win in the end, it really feels like Blender before the 2.8 UI overhaul.

So in the end I picked solidworks instead. 

Solidworks at its core is great and powerful CAD software. However the '3D experience platform' is obnoxious, and asks you to login every single time you open it. 

I've also found solidworks is happy to crash quite regularly, and in one scenario I was completely unable to open it for a week because of a Microsoft Edge DLL. It would crash every time '3D experience' tried to prompt you to save your CAD files into their platform. Which given how crashy it is, doesn't provide much confidence.

Luckily you can still save locally and check that stuff into Git, and again the core CAD software itself is really good.

After a week or so learning Solidworks I came up with this design:

![Dogsbod v1 CAD Design](dogsbod/dogsbod_cad.png)

This allowed me to calculate the final mass budget:



