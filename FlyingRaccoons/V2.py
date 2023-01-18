from machine import TouchPad, Pin
import _thread as thread
import network 
import ntptime
import time


SCANNER = True
TIMEOUT_ON_SCAN = 10


def bottomButton(p2):
    print('Stop pressed!')
    p2.value(0)
    # Read file
    try:
        with open("wifiInfo.json", "r") as f:
            print(f.read())
            f.close()
    except MemoryError:
        f.close()
        print("Error reading file")


def topButton(p2):
    print('Start pressed!')
    wifiScan(p2)


def pinSetup():
    p2 = Pin(2, Pin.OUT)
    p2.value(0)
    print("LEDs set to off")

    leftSensor = TouchPad(Pin(14))
    rightSensor = TouchPad(Pin(4))
    print("Buttons set")
    return p2, leftSensor, rightSensor


def timeCheck():
  print("Setting time")
  try:
    ntptime.settime()
  except OSError:
    print("Time not set")

  rawRightMeow = time.localtime()
  if rawRightMeow[7] < 10:
    hour = "0{}".format(rawRightMeow[7])
  else:
    hour = rawRightMeow[7]

  if rawRightMeow[4] < 10:
    minute = "0{}".format(rawRightMeow[4])
  else:
    minute = rawRightMeow[4]

  if rawRightMeow[5] < 10:
    second = "0{}".format(rawRightMeow[5])
  else:
    second = rawRightMeow[5]

  if rawRightMeow[1] < 10:
    month = "0{}".format(rawRightMeow[1])
  else:
    month = rawRightMeow[1]

  if rawRightMeow[2] < 10:
    day = "0{}".format(rawRightMeow[2])
  else:
    day = rawRightMeow[2]

  year = rawRightMeow[0]

  rightMeow = "{}-{}-{}T{}:{}:{}".format(month, day, year, hour, minute, second)
  rightMeowStr = "{}/{}/{} {}:{}:{}".format(month, day, year, hour, minute, second)
  rightMeowDate = "{}/{}/{}".format(year, month, day)
  rightMeowTime = "{}:{}:{}".format(hour, minute, second)

  return rightMeow, rightMeowStr, rightMeowDate, rightMeowTime


def wifiScan(p2):
    while SCANNER:
        print("Scanning for WiFi networks...")

        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        _, rightMeowstr, _, rightMeowtime = timeCheck()

        # Turn on board LED on
        p2.value(1)        

        ping = wlan.scan()

        secLevels = ["Open", "WEP", "WPA-PSK", "WPA2-PSK", "WPA/WPA2-PSK", "AUTH_WPA2_ENTERPRISE", "AUTH_WPA3_PSK", "AUTH_WPA2_WPA3_PSK", "AUTH_MAX"]
        hiddenStatus = ["Visible", "Hidden"]

        info = {
            "//Example" : {        
                "//SSID": "",
                "//BSSID": "",
                "//Channel": "",
                "//RSSI": "",
                "//Security": "",
                "//Hidden": "",
                "//Time": ""
                }
            }

        for y in ping:
            print("Raw: {}".format(y))
            print("SSID: {}".format(y[0].decode()))
            bssid = "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(*y[1])
            print("BSSID: {}".format(bssid))
            
            print("Channel: {}".format(y[2]))
            print("RSSI: {}".format(y[3]))
            print("Security: {}".format(secLevels[int(y[4])]))
            print("Hidden?: {}".format(hiddenStatus[y[5]]))
            print("Time: {}".format(rightMeowstr))
            print("\n")
            key = "{}_{}".format(y[0].decode(), rightMeowtime)
            info[key] = {
                "SSID": y[0].decode(),
                "BSSID": bssid,
                "Channel": y[2],
                "RSSI": y[3],
                "Security": secLevels[int(y[4])],
                "Hidden": hiddenStatus[y[5]],
                "Time": rightMeowstr
            }

        # Write to file
        info = str(info).replace("'", '"')
        with open("wifiInfo.json", "a+") as f:
            f.write(str(info) + "\n")
            f.close()
        
        print("Waiting for {} seconds before rescanning".format(TIMEOUT_ON_SCAN))
        
        # Turn on board LED off
        p2.value(0)
        
        time.sleep(TIMEOUT_ON_SCAN)


def flash(p2, times):
    for x in range(times):
        p2.value(1)
        time.sleep(0.25)
        p2.value(0)
        time.sleep(0.25)


def main():
    print("Entering main")
    p2, left, right = pinSetup()

    init = True
    
    #flashing to start
    flash(p2, 3)

    while init:
        if left.read() < 200:
            print("Stop side pressed")
            flash(p2, 4)
            thread.start_new_thread(bottomButton, [p2])
            init = False
            global SCANNER
            SCANNER = False
            time.sleep(0.3)

        if right.read() < 200:
            print("Start side pressed")
            flash(p2, 2)
            print("P2 value: {}".format(p2.value()))
            thread.start_new_thread(topButton, [p2])
            time.sleep(0.3)
    
    # Timer is there to allow the scan to catch up
    time.sleep(5)
    print("Reseting to 0")
    flash(p2, 6)
    print("Exiting main")


if __name__ == "__main__":
    print("Starting program")
    main()
