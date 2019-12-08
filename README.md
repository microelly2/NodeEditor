# FreeCAD Node Editor
A visual node editor for FreeCAD based on [PyFlow](https://wonderworks-software.github.io/PyFlow).

![v0.0.3 screenshot](https://user-images.githubusercontent.com/4140247/60964703-fd265580-a2e1-11e9-906b-7dd91a754785.png)

## Status
Under heavy development (Alpha)

## About
[FreeCAD](https://www.freecadweb.org) is an open source 3D CAD/CAM solution with a Python API.  
[PyFlow](https://wonderworks-software.github.io/PyFlow) is a visual scripting framework built in Python.  
When integrated, the result is a visual Node Editor.

## Screencasts

#### v0.22

  - facedraw with pyflow ([clip](https://youtu.be/7FInafkuuEI))
  - crooked stairs with treads ([clip](https://youtu.be/zy8wqJsP9VI))
  - mapping geom2d to surface ([clip](https://youtu.be/8PUBl8KmUx0))
  - alpha shape ([clip](https://youtu.be/PbRHFuk1ojk))

<details>
  <summary><b>Expand this section to see more screencasts</b></summary>

### Important Note
To view the latest PyFlow/NodeEditor development screencasts go to either @microelly2's:  

* website: http://freecadbuch.de/doku.php?id=pyflow
* YouTube PyFlow [playlist](https://www.youtube.com/watch?v=RO3m7oK3AN8&list=PLIxaznuCUATKBEV6bkRLySstKxbGxrmlr)

Here are some highlight selections:

#### v0.0.6

  - generator for vector array, grids and bspline surfaces ([clip](https://youtu.be/fCelpH6e7Xc))
  - from  vectors to vectorlist to vectorarray to surface ([clip](https://youtu.be/H2B6_yldrj8))
  - from vectors to vectorlist to polygon ([clip](https://youtu.be/w5iJYJGBAQE))
  - polygon with input pins for vectors ([clip](https://youtu.be/g5ZAEO5CPWQ))

#### first steps

  - v0.0.4 ([clip](https://youtu.be/XaBEMbWZxAM))
  - v0.0.3 ([clip](https://youtu.be/9B2AxDQQDeg))
  - v0.0.1 ([clip](https://youtu.be/39VoYv0OTNU))

</details>

## Requirements

The FreeCAD NodeEditor current master branch works on the FreeCAD [AppImage](https://www.freecadweb.org/wiki/AppImage) v0.19.18403 or greater.  
Specifically:  

    OS: Ubuntu 14.04.6 LTS (Unity/ubuntu)
    Word size of OS: 64-bit
    Word size of FreeCAD: 64-bit
    Version: 0.19.18403 (Git) AppImage
    Build type: Release
    Branch: master
    Hash: 0717b4fc23ef1db70964c3977d25e2fe46a739d1
    Python version: 3.7.3
    Qt version: 5.12.5
    Coin version: 4.0.0a
    OCC version: 7.3.0
    Locale: German/Germany (de_DE)

### Other Dependencies

* @microelly2's fork of PyFlow: https://github.com/microelly2/PyFlow  
  * The original PyFlow repo is at https://github.com/wonderworks-software/PyFlow
* [Qt.py](https://github.com/mottosso/Qt.py) a 'minimal Python 2 & 3 shim around all Qt bindings - PySide, PySide2, PyQt4 and PyQt5'
* The FreeCAD NodeEditor from this repository: https://github.com/microelly2/NodeEditor

### Important Notes
* Python2 in not longer supported.  
* FreeCAD NodeEditor is compatible with the original PyFlow@wonderworks-software without extra modifications (though we recommend using [@microelly2's fork](https://github.com/microelly2/PyFlow) nonetheless)

## Install

Install the following packages into the local Module directory ~/.FreeCAD/Mod

  - PyFlow from https://github.com/microelly2/PyFlow
  - Qt.py from https://github.com/mottosso/Qt.py  
  - NodeEditor from https://github.com/microelly2/NodeEditor


## Usage
Addon is still heavily developed and is shown here as a proof-of-concept for the time being.  

## Documentation
Documentation will start here http://freecadbuch.de/doku.php?id=pyflow

## Feedback
For feedback, questions, discussions, improvements etc... on this Addon, please use the [dedicated FreeCAD forum thread](https://forum.freecadweb.org/viewtopic.php?f=8&t=36299).

## Author
[@microelly2](https://github.com/microelly2)  

## License
MIT License
