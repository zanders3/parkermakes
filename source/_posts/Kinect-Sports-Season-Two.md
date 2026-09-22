+++
title = "Kinect Sports: Season Two"
date = 2011-11-25
categories = ["Projects"]
tags = ["C++", "C#", "Actionscript", "Xbox 360"]
game_credit = true
thumbnail = "Kinect-Sports-Season-Two/logo.png"
description = "Kinect Sports Season Two was a Xbox 360 game developed by Rare and Big Park for the Kinect as a direct sequel to the BAFTA award winning Kinect Sports title."
+++

[Kinect Sports: Season Two](http://en.wikipedia.org/wiki/Kinect_Sports:_Season_Two) was a Xbox 360 game developed by [Rare](http://www.rare.co.uk/) and [Big Park](http://bigpark.com/) for the Kinect as a direct sequel to the BAFTA award winning [Kinect Sports](http://en.wikipedia.org/wiki/Kinect_Sports) title. I worked on the game at Rare as an intern software engineer between my second and third year of University.

![Kinect Sports: Season Two Logo](Kinect-Sports-Season-Two/logo.jpg)

I arrived at the studio during the final few weeks of Kinect Sports bug testing before release, so I was pulled in to assist with some of the servers that would support the final game when launched. After that I was put onto the pre production tools team helping to prepare Kinect Sports: Season Two for production. This involved fixing bugs and improving the art content, localisation and performance metrics reporting pipelines working mainly in C++ and C#.

![Golf](Kinect-Sports-Season-Two/screen1.jpg)

After this the game moved into production and I was moved onto the core engine team working in C++ where I wrote a new GPU and CPU profiler for the internal game engine. I was then put on the multiplayer team where I worked directly with Artists and Designers on the 'Challenge Play' gameplay mode. This mode glued all of the various game modes together into a new mode which allowed you to challenge your Xbox Live friends and local profiles on the same Xbox asynchronously.

![Challenge Gameplay Mode](Kinect-Sports-Season-Two/challengemode.jpg)

<div class="video-container"><iframe src="https://www.youtube.com/embed/rehYmXTp9yU" title="YouTube video" allowfullscreen></iframe></div>

Implementing this feature involved modifying the game code for each game to support async challenges and implementing the user interface using a combination of C++ and Actionscript since Scaleform was used for the UI. Each game mode was implemented differently and in some cases by a team working from a remote office so this presented a challenge at times. There was also an online server component that  delivered notifications of a challenge from an Xbox Live friend directly from the main menu screen.

![Tennis](Kinect-Sports-Season-Two/screen2.jpg)
