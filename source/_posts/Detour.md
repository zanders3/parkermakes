+++
title = "Detour"
date = 2011-05-11
tags = ["C#", "XNA", "HLSL"]
categories = ["Projects"]
game_credit = true
thumbnail = "Detour/screen1.png"
description = "Detour was an indie game developed in XNA and released on Steam in October 2011."
+++

Detour was an indie game developed in [XNA](http://en.wikipedia.org/wiki/Microsoft_XNA) and released on [Steam](http://store.steampowered.com/app/92100/) in October 2011. It was made by [Sandswept Studios](http://www.sandswept.net/), a small team at the time mostly based in Utah - not counting myself of course who worked remotely! I worked on Detour part time during my first and second year at University.

![Trucks leaving the map in glorious victory](Detour/screen1.jpg)

The game involves you delivering trucks from your factory to the other side of the map by building roads. You must deliver the trucks before your competitors do, so to get a monopoly on the truck delivery market you sabotage your opponents roads with nails, dynamite and bombs. It is often described as a chess game with bombs. There is also a infinite runner mode where you need to keep your truck on the map as it scrolls down the screen. It sure was a weird game design.

![Expanding over the river](Detour/screen2.jpg)

I was completely responsible for the graphics and wrote all of the content pipelines, shaders and special effects from scratch. I also helped out with some of the in game UI. The shaders were written in HLSL and the graphics pipeline used the DirectX 9.0 SDK provided by XNA.

![Nighttime truck chaos](Detour/screen3.jpg)

The renderer batched draw calls into buckets and used static mesh instancing to draw the tiles quickly. It had support for multiple geometry passes and the final game had some sweet effects implemented such as realtime reflections on the water, realtime soft shadows, local lighting, model recolouring, smoke particles, grass billboards, lasers, shield distortion, fog of war desaturation, bloom, tone mapping and a fullscreen explosion blur. I learned a lot about graphics programming in the process.

![Crossing another river](Detour/screen4.jpg)

Looking back I wish I had known more of the tricks to speed things up such as combining meshes dynamically to reduce the total number of draw calls and state switches. I did know some of the tricks such as doing a Z-buffer pre-pass to allow hidden fragments to be discarded. All in all it was a fun project to work on.

<div class="video-container"><iframe src="https://www.youtube.com/embed/AAcREayEcv0" title="YouTube video" allowfullscreen></iframe></div>
