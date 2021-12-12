# refrigerator-grow-box
Software for a refrigerator grow box written in Python

RefrigeratorGUI.py is stated in "kiosk mode" on boot.
RefrigeratorController.py is also started on boot and controls everything independent of the GUI (GUI is not needed)

See Reddit post https://www.reddit.com/r/IndoorGarden/comments/rdy8vm/diy_automated_refrigerator_grow_box/

I am not a Python expert and definitely a tkinter novice.

The software is written for the following hardware:
Raspberry PI Zero 2
  /boot         - Here are all settings stored, filesystem is read/write.
  /             - Filesystem is read only to save the life of SD-card.
  /mnt/ramdisk  - Small ramdisk to save status and historydata. RTC 
  
DHT21           - DHT21 Digital Temperature & Humidity Sensor
                  If I were to redo the growbox today I would choose another sensor to avoid the kernel module.
                  None of the DHT22/DHT11 software (Python) worked with this sensor.
                  Anyway I bought the sensor here: https://www.electrodragon.com/product/am2301-dht21-digital-temperature-humidity-sensor/
                  
Relay board     - This I2C relayboard has a very good price. It has both relays and NPN transistors. Only downside is that it is hard to mount.
                  https://www.electrodragon.com/product/raspberry-pi-relay-shield/

SSR-relay       - Buy a SSR-relay WITH HEATSINK! The transistor on the relay board can pulse the SSR. Use the SSR-relay for heater.

RTC module      - Optional! If you don't have a network connection (no NTP sync) you have to use a RTC module to track time.
                  Buy a DS3231 RTC module on Banggood or Amazon.
             
Touch screen      You can buy a 7" touch screen here: https://www.banggood.com/7-Inch-Full-View-LCD-IPS-Touch-Screen-1024+600-800+480-HD-HDMI-Display-Monitor-for-Raspberry-Pi-p-1633584.html?cur_warehouse=CN&ID=514829&rmmds=search
                  A monitor and mouse will also work :)
