# Starscape

Starscape is a [Blender](http://www.blender.org) add-on for adding stars to the background of a scene.

![Moon-Earth](https://raw.githubusercontent.com/wiki/mrossini-ethz/starscape/images/moon-earth.png)

## Features
The add-on provides the following features:
- Procedural generation of stars
- Realistic brightness and colour distribution
- Realistic number of stars in the sky (but adjustable)
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

### Options

#### Random Seed
The stars are randomly generated. In order to get reproducible results, the random number generator is initialised with a seed value. If the random result is not pleasing in some way (e.g. because there are a bunch of stars too close together by chance), try changing this value.

#### Star Density
The star density can be different depending where you are within a given galaxy. The density value of 1 is used here to represent the conditions found here near the earth. If you set the density to 2 you will see twice as many stars. Note that increasing this number is not realistic in our part of space. Also note that complexity of the scene increases with this number.

#### Star Intensity
You can change the intensity of the stars using this value. At the moment, the value 1 is arbitrary. Note that the interpretation of the intensity value may change in the future to more realistically render stars with a given film exposure.

#### Hemisphere
For scenes on a planet or moon the stars below the horizon are not necessary. This option reduces the amount of computing resources needed.

#### Lock To Camera
Attaches the starscape object to the camera such that the stars remain fixed with respect to the camera. This should always be activated because stars are usually very far away from an observer and their movement is negligible with respect to the motion of the observer. If you have a star that is very close (such as the sun), you should model it separately.

## Planned features
The following features are planned for the future:
- Increase intensity range to fainter stars
- Add a milky way, i.e. a band of higher star density
- Twinkling stars in animations
- Change the star shape

## Changelog

### Version 0.2
Added basic options:
- Random seed
- Star density
- Star intensity
- Hemisphere
- Camera lock

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
