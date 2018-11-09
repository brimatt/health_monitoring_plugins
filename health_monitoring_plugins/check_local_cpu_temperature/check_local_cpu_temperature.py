#!/usr/bin/python
# check_local_cpu_temperature.py - Check the local CPU temperature without the usage of "lm-sensors"

# Copyright (C) 2018 rsmuc rsmuc@mailbox.org
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with check_jenkins_api.py.  If not, see <http://www.gnu.org/licenses/>.

# Import PluginHelper and some utility constants from the Plugins module
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], os.pardir))
from pynag.Plugins import PluginHelper, ok, critical, unknown, warning

# Create an instance of PluginHelper()
helper = PluginHelper()
helper.parser.add_option('-C', help="check the component (temp1, Core 0, Core 1, Core x)", dest="component")

helper.parse_arguments()

# get the options
component = helper.options.component


# The default return value should be always OK
helper.status(ok)

def read_temperature(sensors_filefile):
    try:
        with open(sensors_file) as f:
            content = f.readlines()

        content = [x.strip() for x in content] 
        temperature = float(content[0])/1000

        return temperature

    except:
        helper.exit(summary="not able to read data" , exit_code=unknown, perfdata='')

if __name__ == "__main__":    

    if component == "temp1":        
        # read the data
        sensors_file = "/sys/class/thermal/thermal_zone0/temp"        
        temperature = read_temperature(sensors_file)
        
        # Show the summary and add the metric and afterwards check the metric
        helper.add_summary("CPU temperature: %s C" % temperature)
        helper.add_metric(label='temp',value=temperature)

    
    elif "Core" in component:
        core = int(component.split(" ")[1])
        sensors_file = ("/sys/devices/platform/coretemp.0/hwmon/hwmon1/temp%s_input" % (core+2))
        temperature = read_temperature(sensors_file)
        
        # Show the summary and add the metric and afterwards check the metric
        helper.add_summary("Core %s temperature: %s C" % (core, temperature))
        helper.add_metric(label='temp',value=temperature)
        
    helper.check_all_metrics()

helper.exit()
