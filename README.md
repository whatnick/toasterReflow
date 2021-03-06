# toasterReflow
#### Copyright (c) 2013 - Alexander Hiam - <hiamalexander@gmail.com>

This is the start of a reflow oven control program, intended for use with
converted toaster ovens. It currently runs on the BeagleBone using 
[PyBBIO](https://github.com/alexanderhiam/PyBBIO) and [Adafruit GPIO](https://github.com/adafruit/Adafruit_Python_GPIO), but will eventually 
support more platforms. It uses a [Flask](http://flask.pocoo.org/)
based web interface, with realtime temperature data plotted using 
[Flot](http://www.flotcharts.org/).

BeagleBone based reflow oven write up including enhancements such as multiple heating elements,
self calibration of duty cycles and buzzer can be found on [Seeedstudio Recipe](http://www.seeedstudio.com/recipe/1096-beagleflow-beaglebone-green-reflow-oven.html).

Not everything is working quite right yet, and anything is bound to change;
use at your own risk!


    toasterReflow is licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
