#!/bin/bash

# Car Crash Simulator - Daily Rewards & Quests Reset
# No root required - ADB access only
# Resets daily rewards and quests so you can claim them immediately

PACKAGE_NAME="com.SIDGIN.CarCrashSimulator"
BASE_PATH="/sdcard/Android/data/$PACKAGE_NAME/files"

echo "==================================================="
echo "Car Crash Simulator - Daily Reset Tool"
echo "==================================================="
echo ""

# Check if ADB is available
if ! command -v adb &> /dev/null; then
    echo "❌ Error: ADB is not installed or not in PATH"
    echo "Install ADB first: https://developer.android.com/tools/adb"
    exit 1
fi

# Check if device is connected
if ! adb devices | grep -q "device$"; then
    echo "❌ Error: No Android device connected"
    echo "Connect your device with USB debugging enabled"
    exit 1
fi

echo "✓ ADB found and device connected"
echo ""

echo "Stopping $PACKAGE_NAME..."
adb shell am force-stop $PACKAGE_NAME

# Find the dynamic scheme_container directory
CONTAINER_DIR=$(adb shell "ls -d $BASE_PATH/scheme_container_*" 2>/dev/null | tr -d '\r')

if [ -z "$CONTAINER_DIR" ]; then
    echo "❌ Error: Could not find scheme_container directory in $BASE_PATH"
    echo "Make sure the game has been run at least once"
    exit 1
fi

echo "✓ Found container at: $CONTAINER_DIR"
echo ""

# Data to write - compute dates dynamically
# REWARD_DATA needs 1 year in the past
REWARD_DATE=$(date -d "-1 year" -u +"%Y-%m-%dT%H:%M:%S.%N%:z" | sed 's/\([0-9]\{7\}\)[0-9]*\(.*\)/\1\2/')
# QUESTS_DATA needs a date one year and one day in the future
QUESTS_DATE=$(date -d "tomorrow +1 year" -u +"%Y-%m-%dT%H:%M:%S.%N+00:00" | sed 's/\([0-9]\{6\}\)[0-9]*\(.*\)/\1\2/')

REWARD_DATA="[{\"Id\":-1,\"LastClaimedIndex\":5,\"LastDayClaimed\":\"$REWARD_DATE\"}]"
QUESTS_DATA="[{\"Id\":-1,\"DailyQuestsData\":[{\"QuestType\":0,\"ClaimedIndexes\":\"\",\"CurrentProgress\":100.0},{\"QuestType\":1,\"ClaimedIndexes\":\"\",\"CurrentProgress\":100.0}],\"LastResetTime\":\"$QUESTS_DATE\"}]"

echo "Resetting daily rewards..."
adb shell "echo '$REWARD_DATA' > $CONTAINER_DIR/DailyRewardScheme.fxon"

echo "Resetting daily quests..."
adb shell "echo '$QUESTS_DATA' > $CONTAINER_DIR/DailyQuestsScheme.fxon"

echo ""
echo "✓ Reset complete!"
echo ""
echo "Launching $PACKAGE_NAME..."
adb shell monkey -p $PACKAGE_NAME -c android.intent.category.LAUNCHER 1

echo ""
echo "==================================================="
echo "Done! Your daily rewards and quests are ready to claim"
echo "==================================================="
