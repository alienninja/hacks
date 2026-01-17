# Car Crash Simulator - Quick Start Guide

## What Can You Do?

1. **Modify Prices** - Change vehicle costs, upgrade prices, and rewards
2. **Reset Dailies** - Instantly reset daily rewards and quests

## Setup (One-time)

### Install ADB

**Windows:**
1. Download [Platform Tools](https://developer.android.com/tools/releases/platform-tools)
2. Extract to `C:\platform-tools\`
3. Add to PATH or run from that directory

**Mac:**
```bash
brew install android-platform-tools
```

**Linux:**
```bash
sudo apt install adb  # Ubuntu/Debian
sudo pacman -S android-tools  # Arch
```

### Enable USB Debugging on Android

1. Go to Settings → About Phone
2. Tap "Build Number" 7 times (enables Developer Options)
3. Go to Settings → Developer Options
4. Enable "USB Debugging"
5. Connect phone via USB
6. Accept the debugging prompt on your phone

### Verify Connection

```bash
adb devices
```

Should show:
```
List of devices attached
ABC123DEF456    device
```

## Method 1: Price Modifier (Python)

### Pull the Config File

```bash
adb pull /sdcard/Android/data/com.SIDGIN.CarCrashSimulator/files/ProductScheme.fxon
```

### Modify Values

Edit `modify_game_config.py` and change values in the `MODIFICATIONS` dictionary:

```python
MODIFICATIONS = {
    'vehicle_7': {'InvoiceAmount': 5000},    # Change this number
    'distance_quest1': {'InvoiceAmount': 10000},  # Or this
}
```

### Run the Script

```bash
python3 modify_game_config.py ProductScheme.fxon
```

### Push Back to Device

```bash
adb push ProductScheme_modified.fxon /sdcard/Android/data/com.SIDGIN.CarCrashSimulator/files/ProductScheme.fxon
```

### Restart the Game

Force stop and relaunch the game. Your changes are live!

## Method 2: Daily Reset (Bash)

**Much simpler** - just run:

```bash
chmod +x reset_dailies.sh
./reset_dailies.sh
```

This will:
1. Stop the game
2. Reset your daily rewards (can claim all 7 days)
3. Reset your daily quests (ready to complete again)
4. Relaunch the game

Run this anytime you want to claim dailies again!

## Troubleshooting

### "adb: command not found"
- ADB is not installed or not in PATH
- Solution: Install ADB (see Setup above)

### "no devices/emulators found"
- Phone not connected or USB debugging disabled
- Solution: Connect phone, enable USB debugging, accept prompt

### "Permission denied"
- On Linux, you might need udev rules
- Solution: `sudo usermod -aG plugdev $USER` and reconnect

### Game doesn't show changes
- File might not have copied correctly
- Solution: Pull the file again and verify it was modified

### Script says "scheme_container not found"
- Game hasn't been run yet
- Solution: Launch the game at least once, then try again

## Tips

- **Back up first!** Always keep a copy of the original file
- **Start small** - Try modest changes first (2x instead of 10x)
- **Test incrementally** - Change one thing, test, then change more
- **Game updates** - Updates may reset your modifications

## What Works

✅ Vehicle prices
✅ Upgrade costs  
✅ Quest rewards
✅ Daily rewards
✅ Premium currency conversion
✅ Ad rewards
✅ Daily reset (unlimited times)

## What Doesn't Work

❌ Player level or XP (not in this file)
❌ Unlocking locked content (different system)
❌ Online leaderboards (none exist in this game)

## Example Modifications

### Beginner (Safe)
```python
'vehicle_7': {'InvoiceAmount': 10000},  # 20% off
'distance_quest1': {'InvoiceAmount': 750},  # 50% more
```

### Moderate
```python
'vehicle_7': {'InvoiceAmount': 5000},   # 60% off
'distance_quest1': {'InvoiceAmount': 1000},  # 2x rewards
'car_super_1': {'InvoiceAmount': 5000, 'InvoiceCurrency': 0},  # Premium to coins
```

### Aggressive (Everything cheap)
```python
'vehicle_7': {'InvoiceAmount': 100},    # Almost free
'distance_quest1': {'InvoiceAmount': 10000},  # 20x rewards
```

## Need Help?

- Check the [full write-up](index.html) for more details
- File an issue on GitHub
- Make sure you're using the latest version of the scripts

---

Have fun and remember: **single-player only!**
