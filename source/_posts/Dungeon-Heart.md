+++
title = "Dungeon Heart"
date = 2013-01-27
tags = ["Unity", "C#"]
categories = ["Projects"]
thumbnail = "Dungeon-Heart/screen1.png"
description = "Dungeon Heart was a game made in 48 hours with Alex Trowers and Leanne Bayley as part of the 2013 Global Game Jam game jamming competition."
+++

Dungeon Heart was a game made in 48 hours with [Alex Trowers](http://alextrowers.blogspot.co.uk/) and [Leanne Bayley](http://huhjustablog.blogspot.co.uk/) as part of the 2013 [Global Game Jam](http://globalgamejam.org/) game jamming competition. We even managed to get a good 7 hours sleep and got the game we planned to make finished on time!

Since we used Unity you can [play the full game here](/dungeonheart)!

![The Title Screen](Dungeon-Heart/screen2.png)

The theme was 'Heartbeats' so naturally as big fans (and for some of us ex-employees) of Bullfrog we made a Dungeon Keeper clone, since Dungeon Keeper has a heart in the middle. The game was built with the Unity Game Engine using C#. I find Unity one of the easiest game engines to use, and it is the perfect tool for prototyping and game jamming.

At first we decided how to best split up the work. It was decided that I would focus on the code, Leanne on the Art and Trowers would handle the game design and jump into the other two disciplines where needed. 

Day 1
-----

To start with I focused on getting a basic tile based map engine going, and we made a decision to go 3D. Leanne started cranking out some monsters whilst Trowers searched for sound effects and started throwing some particle effects together. Each level used a really simple text file to define each level layout, with each different character in the text file representing a tile in the map in the level. This allowed us to create a whole bunch of levels really quickly.

So I got that all up and running and then started to focus on the biggest, scariest task - AI Pathfinding! Whilst I knew about the A* pathfinding algorithm and how it worked, I had never attempted to write one from scratch during a game jam before. Luckily thanks to [this fantastic explanation](http://www.policyalmanac.org/games/aStarTutorial.htm) and some fixing of a few off by one errors I managed to get a basic pathfinding system working.

![Attack and Defence of your Dungeon Heart](Dungeon-Heart/screen1.jpg)

I then spent the next few hours setting up a basic AI system. None of the characters in the game were controlled directly and instead needed to decide for themselves where they needed to go. This was done using [Dijkstra's algorithm](Dijkstra's_algorithm), a variant of A* to find the nearest target. For good characters their targets involved other creatures as a first priority, followed by the Dungeon Heart itself. For the evil creatures they simply targeted the nearest (in map steps) good creature.

The AI system also had a really simple animation system that made the characters jump and move between tiles to the time of the Dungeon's Heartbeat.

![We <3 Dragons Team Logo](Dungeon-Heart/screen3.png)

There were 6 character types implemented in the game - 3 good and 3 evil. Naturally the good guys are sneaking into your dungeon and trying to smash up your Dungeon Heart whilst the evil player needs to defend the Dungeon by setting trapdoors (a last minute inclusion, but one of the best bits) and clicking on spawn points at the correct time. If you clicked the spawn point on the beat of the heartbeat three times in row then you would spawn the most powerful creature, two times for the second most powerful and once for the least. Mess up your timing and nothing would happen! The balancing and implementation of the spawn timing system was done by Trowers whilst I was sorting out the pathfinding and character AI system.

By the end of the first night we were in a pretty good position - we had a basic pathfinding system with good creatures pathfinding to the Dungeon Heart but not doing any damage.

Day 2
-----

So with the solid start from the previous day things were looking pretty good the following morning! The final day was spent implementing the final gameplay design making the two different sides attack each other by introducing an attack system and hit points to each character. I also set up the victory and loss conditions, making the Dungeon Heart beat faster when you are about to lose, creating lots of tension in the final moments.

![Outnumbered by Knights](Dungeon-Heart/screen4.png)

The rest of the day was spent getting multiple levels with multiple waves of enemies working and fixing lots of bugs that had popped up over time. Trowers also got the sound effects plugged in and threw some quick designs for multiple levels together as well as the coding for the spawn pads. Leanne had by this point finished all of the art so was making papercraft of the characters in the game.

The final few hours were spent manically bug fixing, as a few hours before the end a load of really strange bugs reared their heads giving us an exciting dash for the finish! At the final deadline naturally the Global Game Jam servers got overloaded but we were allowed to put our entries on a Dropbox instead which we were assured would count.

![A Good Defence!](Dungeon-Heart/screen5.png)

A few hours later we had the judging, done by the very scientific method of whooping and arm waving, and we were positioned in second place. We were all quite happy with that as the competition was fierce! 

In summary the global game jam was great fun and opened my eyes to how much fun a game jam can be! It is a nice change of pace from what sometimes feels like the snails pace of normal game development during your day job, since in your job the software you write has to actually work and not have some really nasty bugs lurking in there! ;)
