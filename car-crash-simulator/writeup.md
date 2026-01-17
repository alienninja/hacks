# How I Hacked a Mobile Racing Game (In 5 Minutes)

## TL;DR
I got tired of grinding for coins in a mobile car crash game, discovered the pricing config was stored in plain JSON on my phone, and wrote a Python script to give myself unlimited money. **It worked.**

## The Discovery

While playing around with a random mobile racing game on Android, I noticed it had the typical free-to-play grind: expensive cars, costly upgrades, and endless "watch an ad for 100 coins" prompts. Being curious (and impatient), I decided to poke around the game files.

### Finding the Gold Mine

Using `adb shell`, I navigated to the game's data directory:

```bash
/sdcard/Android/data/[game.package.name]/files/
```

Inside, I found a file called `ProductScheme.fxon`. The `.fxon` extension was unfamiliar, so I pulled it to my computer:

```bash
adb pull /sdcard/Android/data/[package]/files/ProductScheme.fxon
```

Opening it in a text editor revealed the shocking truth: **it was just a JSON file**. Not encrypted. Not obfuscated. Just plain, beautiful JSON containing every price in the game.

## The Structure

Here's what the pricing data looked like:

```json
{
  "Id": "vehicle_7",
  "InvoiceType": -1,
  "AllowedNumberOfPurchases": 1,
  "IsDefault": false,
  "RelatedInvoices": [{
    "InvoiceCurrency": 0,
    "InvoiceAmount": 12500,
    "Version": 0,
    "RelatedModifier": {"SaleAmount": 0}
  }]
}
```

Breaking it down:
- `InvoiceCurrency: 0` = coins (in-game currency)
- `InvoiceCurrency: 1` = gold (premium currency)
- `InvoiceAmount` = the price
- Quest rewards, daily bonuses, vehicles - **everything was here**

## The Exploit

I wrote a Python script to modify the values. Here's the approach:

### Original Values:
- Most expensive car: **12,500 coins**
- Premium car: **100 gold** (real money)
- Quest rewards: **500-1,500 coins**
- Daily reward: **100 coins**

### Modified Values:
- Most expensive car: **5,000 coins** (60% discount)
- Premium cars: **5,000 coins** (changed from gold to coins!)
- Quest rewards: **1,000-3,000 coins** (doubled)
- Daily rewards: **doubled across the board**

## The Python Script

```python
#!/usr/bin/env python3
import json

MODIFICATIONS = {
    # Quests - Double the rewards
    'distance_quest1': {'InvoiceAmount': 1000},
    'speed_quest2': {'InvoiceAmount': 2000},
    
    # Vehicles - Make them affordable
    'vehicle_7': {'InvoiceAmount': 5000},
    
    # Premium car - Convert from gold to coins!
    'car_super_1': {
        'InvoiceAmount': 5000,
        'InvoiceCurrency': 0  # 0=coins, 1=gold
    }
}

def modify_config(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    for item in data:
        if item['Id'] in MODIFICATIONS:
            for key, value in MODIFICATIONS[item['Id']].items():
                item['RelatedInvoices'][0][key] = value
    
    with open(output_file, 'w') as f:
        json.dump(data, f, separators=(',', ':'))

modify_config('ProductScheme.fxon', 'ProductScheme_modified.fxon')
```

[Download the full script →](modify_game_config.py)

## Does It Actually Work?

I pushed the modified file back to my phone:

```bash
adb push ProductScheme_modified.fxon /sdcard/Android/data/[package]/files/ProductScheme.fxon
```

Restarted the game and... **IT WORKED**. 

I could buy all the cars and upgrades with the modified prices. The premium car that would have cost real money? Now available for in-game coins. Every quest gave double rewards.

## Why Did This Work?

This is a textbook example of **client-side validation failure**. The game trusted the data on the device completely. There was:

- ❌ No server-side validation
- ❌ No encryption
- ❌ No integrity checking
- ❌ No checksum verification

The game simply read the JSON file and used whatever values it found.

## The Right Way To Do This

For game developers reading this, here's how to prevent this:

1. **Server-side validation** - Critical values (prices, currencies) should be validated on your servers
2. **Encryption** - At minimum, encrypt your config files
3. **Integrity checks** - Use checksums or signatures to detect tampering
4. **Obfuscation** - Make it harder (though not impossible) to find and modify data

For a single-player offline game like this, some might argue it doesn't matter - players can cheat themselves if they want. But for games with any online features, this would be catastrophic.

## Lessons Learned

1. **Never trust the client** - This applies to web apps, mobile games, everything
2. **Plain text configs are dangerous** - Even if you think users won't find them
3. **Android's app directories are accessible** - With adb or a file explorer, users can see everything
4. **Security through obscurity doesn't work** - A weird file extension (`.fxon`) didn't stop anyone

## Try It Yourself

**Important Disclaimers:**
- This is for **single-player games only**
- Don't use this on games with multiplayer or leaderboards
- This is educational - understand what you're doing and the implications
- I'm not responsible if you break your game or get banned from something

The script works on any game that stores config in plain JSON. Just:
1. Find the game's data directory
2. Look for JSON/config files
3. Modify carefully
4. Test and enjoy

## Conclusion

This was a fun 5-minute reverse engineering session that turned an endless grind into instant gratification. It's a great reminder that **security is hard** and **client-side data can never be trusted**.

The fact that a mobile game in 2026 stores critical pricing data in unencrypted JSON on the device is both hilarious and educational. 

---

**Questions? Want the full script?** Find me on [Twitter/X] or [GitHub].

*This post is for educational purposes. Don't be a jerk - only use this on single-player games where you're the only one affected.*
