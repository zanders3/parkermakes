+++
title = "GB Emulator"
date = 2017-08-03
tags = ["C++"]
categories = ["Projects"]
thumbnail = "/2017/08/03/GBemulator/tetris.png"
description = "A gameboy hardware emulator that uses GLWT and imgui for rendering."
+++

![My emulator playing Tetris in Demo Mode](/2017/08/03/GBemulator/tetris.png)

I've been messing about with emulators! The GB hardware is [very](http://marc.rawer.de/Gameboy/Docs/GBCPUman.pdf) [well](http://gameboy.mongenel.com/dmg/opcodes.html) [documented](http://imrannazar.com/Gameboy-Z80-Opcode-Map) with [lots of interesting](https://cturt.github.io/cinoop.html) [blog posts](http://imrannazar.com/GameBoy-Emulation-in-JavaScript) on the topic so I've decided to have a go at writing a gameboy hardware emulator myself.

The current status of the project is that I've implemented most of the CPU opcodes, GPU emulation and memory bank controller emulation required to get tetris up and running. I also wrote a GPU debugger, memory inspector and disassembler using [imgui](https://github.com/ocornut/imgui) that can be used to find emulator bugs. I'm also using my own [GLWT](https://github.com/zanders3/glwt2) library to create a window and make an OpenGL context.

So there is just about enough there for you to get through the menus, watch the demo mode and play a game of tetris! There are some crazy bugs though - I've not implemented the hardware used for random number generation so you only get square blocks falling from the top of the screen making for a less than entertaining game of tetris. In addition the sprite rendering has an off by one error somewhere (a faulty instruction somewhere?) meaning the blocks are shifted down by 1. Audio is also not implemented yet.

![Debugging Tetris](/2017/08/03/GBemulator/debugger.jpg)

I'm currently focused on writing some cpu unit tests for the whole thing to find and fix those faulty instructions, but it is a huge task and is taking me a while. Overall it's been a pretty fun project to hack around with so far.

I've thrown the whole source code of the thing up on github - take a look! https://github.com/zanders3/gb
