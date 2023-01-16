import machine
import network 
import time
# import urequests as requests
import ntptime


def main():

    p0 = machine.Pin(0, machine.Pin.OUT)
    p0.value(0)
    p2 = machine.Pin(2, machine.Pin.OUT)
    p2.value(0)

    init = True
    button1 = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
    button2 = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
    while init:
        if not button1.value():
            print('Bottom Button pressed!')
            init = False
            print("I am stopping now...")
            p2.value(0)
            p0.value(0)

            # Read file
            try:
                with open("wifiInfo.json", "r") as f:
                    print(f.read())
                    f.close()
            except MemoryError:
                f.close()
                print("Error reading file")

        elif not button2.value():
            print('Top Button pressed!')
            p0.value(1)
            p2.value(0)
            wifiScan()
            time.sleep(0.5)
            p0.value(0)
            p2.value(1)

def timeCheck():
  print("Setting time")
  try:
    ntptime.settime()
  except OSError:
    print("Time not set")

  rawRightMeow = time.localtime()
  count = 0
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


def wifiScan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    _, rightMeowstr, _, rightMeowtime = timeCheck()
    ping = wlan.scan()

    secLevels = ["Open", "WEP", "WPA-PSK", "WPA2-PSK", "WPA/WPA2-PSK"]
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
        # print("Raw: {}".format(y))
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
    with open("wifiInfo.json", "a+") as f:
        f.write(str(info) + "\n")
        f.close()
    
        
if __name__ == "__main__":
    print("Starting program")
    main()
