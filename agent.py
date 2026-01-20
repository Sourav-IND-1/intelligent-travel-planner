print("🤖 Travel Planning Agent Started")

import adbutils
import time

adb = adbutils.AdbClient(host="127.0.0.1", port=5037)
devices = adb.device_list()

if not devices:
    print("❌ No Android device connected")
    exit()

device = devices[0]
print("📱 Connected:", device.serial)

# Wake phone
device.shell("input keyevent KEYCODE_WAKEUP")
device.shell("input keyevent KEYCODE_HOME")
time.sleep(1)

# -----------------------------
# OPEN MAPS (VISIBLE SEARCH)
# -----------------------------
device.shell(
    "monkey -p com.google.android.apps.maps "
    "-c android.intent.category.LAUNCHER 1"
)
time.sleep(4)

device.shell("input tap 540 200")
time.sleep(1)
device.shell('input text "Top places to visit in Goa"')
device.shell("input keyevent KEYCODE_ENTER")
time.sleep(5)

# -----------------------------
# OPEN BOOKING (VISIBLE SEARCH)
# -----------------------------
device.shell("input keyevent KEYCODE_HOME")
time.sleep(1)

device.shell(
    "monkey -p com.booking "
    "-c android.intent.category.LAUNCHER 1"
)
time.sleep(4)

device.shell("input tap 540 500")
time.sleep(1)
device.shell('input text "Goa"')
time.sleep(2)
device.shell("input tap 540 750")
time.sleep(5)

# -----------------------------
# CREATE GOOGLE KEEP NOTE (INTENT)
# -----------------------------
note_text = (
    "Travel Planning – Goa\n\n"
    "Top Places to Visit:\n"
    "https://www.google.com/maps/search/top+places+to+visit+in+goa\n\n"
    "Top Rated Hotels:\n"
    "https://www.booking.com/searchresults.html?"
    "ss=Goa&review_score=80&order=review_score_and_price\n\n"
    "Flights:\n"
    "https://www.google.com/flights?hl=en#flt=PAT.GOI;econ;sc:e"
)

device.shell(
    'am start -a android.intent.action.SEND '
    '-t text/plain '
    '-e android.intent.extra.TEXT "{}" '
    'com.google.android.keep'.format(note_text.replace('"', '\\"'))
)

print("📝 Google Keep note CREATED via system intent")
print("✅ Travel planning completed")
