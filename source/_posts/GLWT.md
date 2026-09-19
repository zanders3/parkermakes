+++
title = "GLWT"
date = 2016-07-10
tags = ["C", "C++", "Objective-C"]
categories = ["Projects"]
thumbnail = "/2016/07/10/GLWT/glwt.png"
description = "The OpenGL window toolkit is a single file C++ library that creates an OpenGL context on Windows/OSX"
+++

Inspired by the [fantastic stb libraries](https://github.com/nothings/stb) by Sean Barrett I got tired of spending hours messing about trying to get an OpenGL context up and running. Libraries such as [SDL](https://www.libsdl.org/) can manage this for you very well but feel overkill when you're starting out.

So I've decided to write my own window and platform abstraction library which will grow over time as I develop my other personal projects. The whole thing is pretty bare bones at the moment so I wouldn't recommend you actually use it right now. Take a look!

https://github.com/zanders3/glwt2

## Usage

This main.c will get you started:

    #include "glwt.h"
    
    void glwt_setup()
    {
    }
    
    void glwt_draw(float time)
    {
        glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
    }
    
    int main(int argc, char *argv[])
    {
        return glwt_init("Hello, GLWT!", 800, 600, false);
    }

## Compiling

Simply create a new empty XCode/Visual Studio project and add glwt.(cpp/mm) and glwt.h to the project.

On Mac you will need to go to the 'Build Phases' XCode project settings tab and add the Cocoa.framework and OpenGL.framework for the project to link. Also ensure the glwt.mm file is an mm file *not* a cpp file.

## Input
Pressed keys are stored in the global ```bool glwt_keydown[255];``` structure as ascii keycodes. e.g. ```glwt_keydown['a']```. This will work for a-z and 0-9 keys. There are additional keys defined in the Keys enum at the top of the header file. This currently only works on windows - I'll be adding Mac support later!

