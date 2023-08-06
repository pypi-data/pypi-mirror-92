## ThinkIndicator

Has automatic fan control of your ThinkPad made your knees flame and bodily fluids boil?

Maybe you're fine with your laptop running hot but you want to quickly switch it to full fan speed, get to bed with it and get no burns?

Look no further!

This little indicator (taskbar widget) will let you change the fan speed with just a scroll over it.

### Requirements

* Python>3.6
* Linux with acpi_thinkpad module (if you don't know what it is, you have it)
* pygobject
* libappindicator
* Root access (if you know how to bypass that, let me know)
* Obviously, an IBM/Lenovo ThinkPad

#### Enabling fan control

Check if you have `/proc/acpi/ibm/fan` file in your system. If not, try loading acpi_thinkpad module with command `modprobe acpi_thinkpad`.

The next step is enabling manual control over the fans. Create file `/etc/modprobe.d/50-thinkfan.conf` with content `options thinkpad_acpi fan_control=1`.

Reboot and you're all set.

#### pygobject

An appropriate package is called python3-gobject in SUSE and Fedora, python3-gi in Debian and Ubuntu, python-gobject in Arch btw.

#### libappindicator

An appropriate package is called libappindicator3-1 in most distros, libappindicator-gtk3 in Arch.

### Usage

Run start.sh. You should see a number or letter signifying the current fan status in your taskbar. Click on it to change the mode. If you are in a manual mode (signified by a number) then you can scroll on the indicator to change the speed level.

If shit hits the fan (haha) let me know via the Issues tab.

## Disclaimer

THIS SOFTWARE IS DISTRIBUTED UNDER NO RESPONSIBILITY ACCEPTED FOR THE RESULTS OF ITS USAGE, INCLUDING BUT NOT LIMITED TO FRYING YOUR LAPTOP, TESTICLES OR OVARIES.
