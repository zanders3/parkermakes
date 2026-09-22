+++
title = "PlayWithYourPeas"
date = 2009-06-10
tags = ["C++", "DirectX"]
categories = ["Projects"]
thumbnail = "PlayWithYourPeas/screen1.png"
description = "PlayWithYourPeas was a game protoype design challenge posted by Daniel Cook on his Lost Garden blog."
+++

[PlayWithYourPeas](http://www.lostgarden.com/2008/02/play-with-your-peas-game-prototyping.html) was a game protoype design challenge posted by Daniel Cook on his [Lost Garden blog](http://www.lostgarden.com). He provided the design and art assets and all you had to do was implement it so I had a go! You can either [download the installer](PlayWithYourPeas/PlayWithYourPeasSetup.exe) (windows only) or take a look at the [source code](PlayWithYourPeas/NinjaPeasSource.zip).

![](PlayWithYourPeas/screen1.jpg)

The design is pretty awesome - you place peas who are convinced they are ninjas on a dinner plate assualt course of your own design. The ninja peas will climb to the top of your towers and jump. The longer they jump and the higher they fall (without squishing themselves) the bigger the score. Score the most points to win!

I implemented the design in C++ using the DirectX 9.0 and Win32 APIs for Window and Mouse Input as well as the [Box2D library](http://box2d.org/) to do physics collisions and response and the [irrKlang library](http://www.ambiera.com/irrklang/) to play the sound effects and music. The sounds effect were recorded and processed by myself using [Audacity](http://audacity.sourceforge.net/) and the music was from [incompetech](http://incompetech.com/) - a fantastic source of gameplay music.

![](PlayWithYourPeas/screen2.jpg)
![](PlayWithYourPeas/screen3.jpg)
![](PlayWithYourPeas/screen4.jpg)
