from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, sh1107, ws0010
from PIL import ImageFont

import subprocess

serial = i2c(port=1, address=0x3C)
device = sh1106(serial,rotate=2)


while True:
    name = 'RaspiOS'

    cmd = "hostname -I | cut -d\' \' -f1 | head --bytes -1"
    ip = subprocess.check_output(cmd, shell = True )

    cmd = "top -bn1 | grep load | awk '{printf \"%.2fLA\", $(NF-2)}'"
    cpu = subprocess.check_output(cmd, shell = True )

    cmd = "free -m | awk 'NR==2{printf \"%.2f%%\", $3*100/$2 }'"    
    mem = subprocess.check_output(cmd, shell = True )
    
    cmd = "df -h | awk '$NF==\"/\"{printf \"HDD: %d/%dGB %s\", $3,$2,$5}'"
    cmd = "df -h | awk '$NF==\"/\"{printf \"%d/%dGB\", $3,$2}'"
    disk = subprocess.check_output(cmd, shell = True )
    
    cmd = "vcgencmd measure_temp | cut -d '=' -f 2 | head --bytes -1"
    temp = subprocess.check_output(cmd, shell = True )

    with canvas(device) as draw:
        draw.text((0, 0), name, fill="white")
        draw.text((0, 10), ip, fill="white")
        draw.text((0, 20), cpu, fill="white")
        draw.text((60, 20), mem, fill="white")
        draw.text((0, 20), disk, fill="white")
        draw.text((60, 20), temp, fill="white")
