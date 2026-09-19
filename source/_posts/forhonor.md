+++
title = "For Honor"
date = 2018-04-19
tags = ["C++","networking","lockstep"]
categories = ["Projects"]
thumbnail = "/2018/04/19/forhonor/forhonor.png"
description = "An 8v8 realtime multiplayer fighting game"
game_credit = true
+++

![For Honor Title](/2018/04/19/forhonor/forhonor.png)

I worked on For Honor as a Senior Gameplay Programmer whilst working at Studio Gobo. I built the core training mode logic that trains players on parry, block and attack timings. This is dynamic and is done by analysing the character behavior trees dynamically during gameplay.

This feature continues to train for honor players to this day!

From a technical perspective For Honor is a very interesting game. It uses deterministic lockstep with rollback as the networking model which is pretty unique for a 3rd person 3D multiplayer game, though admittedly this is a well known technique for 2D multiplayer fighting games.

One of my proudest gaming achievements during this project was defeating the gameplay director at their own game during a playtest on site at Ubisoft Montreal. Unfortunately this enjoyment later backfired because the character I used was then slightly nerfed a couple of months later!
