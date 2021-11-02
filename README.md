# Starscape

Starscape is a [Blender](http://www.blender.org) add-on for adding stars to the background of a scene.

![Moon-Earth](https://raw.githubusercontent.com/wiki/mrossini-ethz/starscape/images/moon-earth.png)

## Features
The add-on provides the following features:
- Procedural generation of stars
- Realistic brightness and colour distribution
- Realistic number of stars in the sky
- Stars are actual objects in the scene (no textures!)
- Star appearance is independent from render resolution and camera focal length (point sources)
- Appearance can be changed by hand after generation
- Compatible with all kinds of world backgrounds

## Blender Artist thread
[Link](https://blenderartists.org/t/starscape-add-on/1336930 "Link") to Blender Artist page

## Installation
1. Download the latest [release](https://github.com/mrossini-ethz/starscape/releases) and save it in a directory of your convenience.
2. Open Blender.
3. In th menu go to Edit -> Preferences -> Addons.
4. At the top of the window, chose *Install*.
5. Select the file downloaded zip file and press *Install Addon*.
6. Search for *Scene: Starscape* in the Addon list.
7. Activate the checkbox for the plugin.
8. If you want to keep the addon activated when blender restarts, open the menu (bottom left menu button) and choose *Save Preferences*.

## Usage

### Addon Panel
The controls for the addon can be found in the Properties panel under World > Starscape.

### Execution
Press 'Generate Starscape' in the panel. That's it! An object called 'Starscape' is created. It is anchored to the camera and thereby appears to remain fixed in the render even when moving the camera.

At the moment there are no options. This will change in the future.

## Planned features
The following features are planned for the future:
- Adjustable number of stars
- Change the random seed
- Adjustable star intensity
- Increase intensity range to fainter stars
- Add a milky way, i.e. a band of higher star density
- Twinkling stars in animations
- Create hemisphere only as an option
- Change the star shape

## Changelog

### Version 0.1
First official release.

## License
Camera Calibration with Perspective Views of Rectangles

Copyright (C) 2021  Marco Rossini

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
version 2 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

This Blender plugin is based on the research paper "Recovery of Intrinsic
and Extrinsic Camera Parameters Using Perspective Views of Rectangles" by
T. N. Tan, G. D. Sullivan and K. D. Baker, Department of Computer Science,
The University of Reading, Berkshire RG6 6AY, UK,
from the Proceedings of the British Machine Vision Conference, published by
the BMVA Press.
