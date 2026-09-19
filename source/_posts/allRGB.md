+++
title = "allRGB Rainbow Fractal"
date = 2014-03-15
tags = ["C++"]
categories = ["Projects"]
thumbnail = "/2014/03/15/allRGB/rainbowfractal.png"
description = "The challenge was simple; create an image containing all 16777216 RGB colours in a single image with not one colour missing or duplicated!"
+++

The challenge was simple: create an image containing all 16777216 RGB colours in a single image with not one colour missing or duplicated!

![Rainbow Fractal](/2014/03/15/allRGB/rainbowfractal.jpg)

At the time there weren't many mandelbrot fractal examples so I decided to try and find a way to create an all RGB image of the mandelbrot set. The resulting image is a 4096x4096 48.1Mb in PNG format. A compressed thumbnail is below; go to allRGB.com if you [want to see the full image](http://allrgb.com/rainbow-fractal).

The code I wrote to create the image is [available here](https://gist.github.com/zanders3/9a690443bc4b22340e00). It works by first calculating a color mapping representing every RGB color, which is then sorted by Hue.

Next we generate a grayscale mandelbrot image whilst generating a histogram of the range of values in this grayscale image. The histogram is then converted into a cumulative histogram which gives us an offset into the color map. This in effect means we have a bucket of colours to choose from for each grayscale value representing the mandelbrot image.

We can now generate the image at this point by looping through the grayscale mandelbrot image, looking up which histogram bucket the gray pixel is in, use up one of those RGB colours in the bucket and use that colour in the final image.

This simple algorithm does have a drawback of producing weird shapes due to the hue sorting so we randomise the colours contained within each histogram bucket to produce a more pleasing image when viewed from a distance!

I hope that all made sense! It certainly was a fun challenge to do; I can highly recommend giving this challenge a go!
