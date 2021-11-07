# Blender Plugin: Starscape
# Copyright (C) 2021  Marco Rossini
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# This Blender plugin is based on the research paper "Recovery of Intrinsic
# and Extrinsic Camera Parameters Using Perspective Views of Rectangles" by
# T. N. Tan, G. D. Sullivan and K. D. Baker, Department of Computer Science,
# The University of Reading, Berkshire RG6 6AY, UK, Email: T.Tan@reading.ac.uk,
# from the Proceedings of the British Machine Vision Conference, published by
# the BMVA Press.

bl_info = {
    "name": "Starscape",
    "author": "Marco Rossini",
    "version": (0, 2, 0),
    "warning": "This is an unreleased development version.",
    "blender": (2, 90, 0),
    "location": "Properties > World Properties > Starscape",
    "description": "Creates a procedural starscape for use as a scene background",
    "wiki_url": "https://github.com/mrossini-ethz/starscape",
    "tracker_url": "https://github.com/mrossini-ethz/starscape/issues",
    "support": "COMMUNITY",
    "category": "Scene"
}

if "bpy" in locals():
    import importlib as imp
    imp.reload(starscape)
    imp.reload(operator)
    imp.reload(properties)
    imp.reload(panel)
else:
    from . import starscape
    from . import operator
    from . import properties
    from . import panel

import bpy

def register():
    bpy.utils.register_class(properties.StarscapeProperties)
    bpy.types.Scene.starscape_properties = bpy.props.PointerProperty(type=properties.StarscapeProperties)
    bpy.utils.register_class(operator.StarscapeOperator)
    bpy.utils.register_class(panel.StarscapePanel)


def unregister():
    bpy.utils.unregister_class(panel.StarscapePanel)
    bpy.utils.unregister_class(operator.StarscapeOperator)
    bpy.utils.unregister_class(properties.StarscapeProperties)

if __name__ == "__main__":
    register()
