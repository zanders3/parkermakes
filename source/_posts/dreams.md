+++
title = "Dreams"
date = 2023-09-10
tags = ["C", "C++", "Golang", "highlights"]
categories = ["Projects"]
thumbnail = "/2023/09/10/dreams/dreams.png"
description = "Dreams, a game about making games by Media Molecule"
+++

![Dreams Title Image](/2023/09/10/dreams/dreams.png)

[Dreams](https://en.wikipedia.org/wiki/Dreams_(video_game)) was a game making toolkit that I helped Media Molecule to build and support from 2017-2023. It won the 2021 [BAFTA Award for Technical Achievement](https://www.imdb.com/title/tt5309972/awards/) amongst other awards.

I joined the team as a tools programmer and grew to become fully responsible and accountable for the 'dreamiverse' which was the online service that allowed users to share their user generated content with the world. Growing myself from tools programmer, to principal tools programmer and then finally lead server programmer.

I was responsible for the architecture of the online service and I then built and led a team of server and devops programmers to develop and deploy the service.

The service had a lot of fun challenges since it combined features of:

- Social networks (likes, follows with notification 1 to many explosions)
- Deep genealogy graph connections (play next collaborative filtering)
- Custom search (page rank, similarity embeddings)
- Moderation systems
- Scalable user content storage systems
- User facing website - [indreams.me](https://indreams.me)

Which all led to some interesting challenges getting the thing to scale correctly. We built the whole thing on top of DynamoDB, S3, SQS, Kubernetes and redis using golang microservices with debug services verified via Oauth2. This service worked really well throughout development.

A whole bunch of other stuff happened during development to get the thing out the door. It was a huge challenge to actually ship this thing. Maybe one day I will actually write some of that stuff up properly.

I had a lot of fun through the development and during the post launch support working on my own 'games' within the game creation toolkit. Some of my [creations](https://indreams.me/zanders3/creations) got over 20k likes.

I'm going to list them below for posterity as well to explain the game creation journey I went through. It was really fun. I'm mostly listing them in order of 'best' not the order in which I actually made things.

# My Dreams Games

## Cake Factory and Cake Factory 2

![Cake Factory 2](/2023/09/10/dreams/cake_factory.jpg)

[Cake Factory](https://indreams.me/dream/mDhVUarUKLK) was a game inspired by Factorio, but fully implemented within the limitations of the dreams logic system. You build wheat and sugar farms, then that goes into a mill, then a cake mixer, then an oven and so on until you have delicious cake.

You are rewarded for making the delivery as quickly as possible.

## Mega Penguin Goes Rafting

I made a [whole series](https://indreams.me/scene/djdqZsJWYxR) of mega penguin games. My favourite is this [rafting one](https://indreams.me/scene/dfKqjTSpgJP) where mega penguin discovers a paddle and decide to see where the river leads.

![Mega Penguin staring at a paddle](/2023/09/10/dreams/mega_penguin_paddle_stare.jpg)
![Mega Penguin discovers that skipping swimming lessons for the gym can actually pay off!](/2023/09/10/dreams/mega_penguin_goes_rafting.jpg)

## City Simulator and City Simulator 2

The [first city simulator](https://indreams.me/dream/mhAbqmWxSFA) has been played by 40k people, I then followed this up with [a sequel](https://indreams.me/dream/mMPkxBPPPch) which had much improved graphics as I got better at using the art tools.

![City Simulator 2](/2023/09/10/dreams/city_simulator_2.jpg)

## The Blackfish

One of my favourite game designs that I keep 'accidentally' revisiting in various game jams since it's fun but really simple. [You control a pirate ship](https://indreams.me/dream/mmUhWzdbTyy) in first person on a dynamic ocean surface and use your cannons to sink the enemy ships before they sink you. 

Honestly inspired by Assassins Creed 4's ship gameplay which is awesome, which I think was itself originally inspired by Sid Meir's Pirates.

![The Blackfish](/2023/09/10/dreams/the_blackfish_pirate_game.jpg)

## Monster Truck Mountain

[This one](https://indreams.me/dream/mGgFRoxQuLz) was inspired by my love of the classic [Monster Truck Madness](https://en.wikipedia.org/wiki/Monster_Truck_Madness) game. I had a lot of fun building the suspension raycasting system on this one.

![Monster Truck Mountain](/2023/09/10/dreams/monster_truck_mountain_title.jpg)

## Taxi Drift

My love letter to [Crazy Taxi](https://en.wikipedia.org/wiki/Crazy_Taxi) in all but name.

![Taxi Drift Title](/2023/09/10/dreams/taxi_drift_taxi_game.jpg)
![Taxi Drift In Game](/2023/09/10/dreams/taxi_drift_in_game.jpg)

## Kingdom

A turn based strategy game set on the South East Coast in roughly 1200 AD. It may or may not be inspired by a particularly popular game about building civilisations. [Brighthelmstone](https://brightonmuseums.org.uk/discovery/history-stories/brighthelmstone-brighton-in-the-middle-ages/) ahoy!

![Kingdom Title](/2023/09/10/dreams/kingdom_civ_like.jpg)
![Kingdom Gameplay](/2023/09/10/dreams/kingdom_turn_screen.jpg)

## Flight Simulator

I was playing a lot of Microsoft Flight Simulator at the time, ok? [Dreams needed it's own one](https://indreams.me/dream/meRYRjbRtni), and nobody else had done it yet.

![Dreams Flight Simulator](/2023/09/10/dreams/dreams_flight_simulator.jpg)
![Sunset](/2023/09/10/dreams/flight_sim_sunset.jpg)

## River Raft

The first game I actually managed to create with the dreams tools. [You steer a river raft](https://indreams.me/dream/mEhepJNyark) down a river. It's pretty chill.

![River Raft](/2023/09/10/dreams/river_raft.jpg)

# Really Amazing Dreams Creations

I want to write some words about the best creations that I saw and played during my time playing dreams.

## Pig Detective

The [pig detective series](https://indreams.me/dream/mAckfpcDxDd) honestly deserves to be its own, separate game series. It is a fully voice acted point and click adventure game. I forgot I was playing dreams. A full game in its own right.

![Pig Detective: The Beast of Boffington](/2023/09/10/dreams/pig_detective.jpg)

## Trip's Voyage

This one was so [ridiculously polished](https://indreams.me/dream/mdtuorKHYjZ). Yes it's a complete ripoff of a certain plumbing based oddysey game but it is a fantastic homage.

![Trip's Voyage](/2023/09/10/dreams/trips_voyage.jpg)

There were a whole bunch of really [great creations I collected here](https://indreams.me/collection/cioqCdsovtR), but these two were the truly stand out creations in my book.

## Summary

Working on Dreams was an absolute blast. It was a fantastic project that I am proud to have contributed to. I hope my work has in some way inspired the next generation to learn and get excited about games and game development.
