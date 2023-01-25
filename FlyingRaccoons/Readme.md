### What is Flying Raccoons?

 - Flying racoons is a series of IoT devices that were developed to assist in hacking companies wifi networks. 
 - The general goal of all of these programs is to either assist or preform a phishing attack via a wifi hotspot (similar to an evil twin attack) and allow an attacker to gain the credentials to a wifi network.

### Why make Flying Raccoons?

 - Flying Raccoons is being developed due to how small and cheap IoT devices are. While a Wifi Pineapple can do more, deploying one is often more difficult due to size and the look of their antenna. Small devices like the ESP32 and ESP8266 do not have this issue as they are easily concealable. 
 - Another benefit to this is that they can also be put in small containers and dropped anywhere. My favorite method for delivery is via drone. This allows placement of these kinds of devices to be even harder to find along with being more discreet. If equipped with a magnet, you can even retrieve the device without having to be able to physically reach the area.

### How is this different from a wifi pineapple or other wifi testing device?

 - The main difference is that these programs are designed to be used on an ESP32 or ESP8266 devices using Micropython. The reason for this is so that you can cheaply deploy a device and not fear about what happens if it gets damaged. 
 - Another reason is due to it's weight. Since the ESP devices are so small, you can place them in a light container and then drop them off by hand or with a drone. This option allows for better placement of the device without as high of a likelihood of it being discovered.

### What are the different versions?
 - V1 (Released) is designed to be used by hand as a recon tool. This version allows a user to walk around and click 1 of 2 buttons. 
   - The "top" button will scan the near by SSID's from wifi access points and record the data along with time every time the button is clicked. 
     - For convince, there are 2 LEDs on the device. One to signal ready for scanning and the other to signal a scan is in progress
   - The "bottom" button is to stop the scanning and to turn off the LEDs as they can potentially be very bright.
  - V2 (Released) is similar to V1 except that it is optimized to be used on a drone. The main differences are
    - Scanning is done automatically versus manually (every 10 seconds AFTER a scan is complete)
    - ~~No LEDs are attached since the scanning is done automatically~~
      - Signaling via LED is done from the on board LED vs attaching LEDs on a board
    - The top button starts the scanning with a 30 second delay instead of instantly
      - The automatic scanning starts and continues after the first initial scan.
      - ~~The bottom button works the same.~~
        - The buttons have been removed in exchange for touching the pins. 
        - Left side is now the bottom button and right side is now the top. 
   - V3 (In development) is the ideal first end goal. The device would be able to do the following:
     - Be loaded with a target SSID to impersonate
     - Check to make sure that the SSID is in range and it has a decent connection to it (-70 dBm or lower ideally. After -80, it will wait a set number of seconds and wait until it has a greater signal)
     - If the above is set, it will then set up an evil twin with an open network
     - At this point, it will deploy a captive portal with a phishing page to gather passwords for the WiFi.
     - Every attempt to log in via the portal will try to authenticate to the Wifi. 
       - If the device is able to connect, it will notify the end user that the password was correct and then give the next page (Different pages per designed scenario). 
       - If the password is incorrect, it will notify the end user that the password was incorrect and to try again.
     - Once it is able to connect to the wifi, the device will test to see if it was given a non-APIPA address.
       - If it sees an APIPA address, the device will change MAC addresses to see if it can get an address by impersonating different devices (A printer, Cisco router, etc...)
         -  If it is unable to get an IP address, the device will shut off and start beaconing every 10 minutes for a duration of 30 seconds to assist in retrieval.
       - If it does not see an APIPA address, it will attempt to connect to the C2 server defined in the code. 
       - At this point, the C2 server will have instructions on what it should do next.
         - Options are either beacon that it is complete with it's assessment or download new code to upgrade and continue an attack with Micropython.


### Goals for the future

In the future (Version 4 and beyond) I will probably attempt to make the device do a range of attacks:
 - Bluetooth attacks with an ESP32
 - SDR based attacks
 - Deauth attacks (both targetted and against all targets)
 - RFID based attacks
