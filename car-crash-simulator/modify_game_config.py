#!/usr/bin/env python3
"""
Game Configuration Modifier
Easily tweak game values by editing the MODIFICATIONS dictionary below
"""

import json
import sys
from pathlib import Path

# ============================================================================
# EDIT THESE VALUES TO MODIFY THE GAME
# ============================================================================

MODIFICATIONS = {
    # Quest Rewards - Double from original (was 10x, trying 2x now)
    'distance_quest1': {'InvoiceAmount': 1000},   # Original: 500
    'distance_quest2': {'InvoiceAmount': 2000},   # Original: 1000
    'distance_quest3': {'InvoiceAmount': 3000},   # Original: 1500
    'speed_quest1': {'InvoiceAmount': 1000},      # Original: 500
    'speed_quest2': {'InvoiceAmount': 2000},      # Original: 1000
    'speed_quest3': {'InvoiceAmount': 3000},      # Original: 1500
    
    # Daily Rewards - Double from original
    'daily_reward_day1': {'InvoiceAmount': 200},   # Original: 100
    'daily_reward_day2': {'InvoiceAmount': 400},   # Original: 200
    'daily_reward_day3': {'InvoiceAmount': 600},   # Original: 300
    'daily_reward_day4': {'InvoiceAmount': 800},   # Original: 400
    'daily_reward_day5': {'InvoiceAmount': 1000},  # Original: 500
    'daily_reward_day6': {'InvoiceAmount': 1600},  # Original: 800
    'daily_reward_day7': {'InvoiceAmount': 3000},  # Original: 1500
    
    # Vehicles - Cheaper pricing (5000 coins max instead of up to 12500)
    'vehicle_1': {'InvoiceAmount': 1000},    # Original: 1500
    'vehicle_2': {'InvoiceAmount': 1500},    # Original: 2500
    'vehicle_3': {'InvoiceAmount': 1500},    # Original: 2500
    'vehicle_6': {'InvoiceAmount': 3000},    # Original: 7500
    'vehicle_7': {'InvoiceAmount': 5000},    # Original: 12500
    'vehicle_8': {'InvoiceAmount': 5000, 'InvoiceCurrency': 0},  # Original: 250 gold
    
    # Super Car - Coins instead of gold
    'car_super_1': {'InvoiceAmount': 5000, 'InvoiceCurrency': 0},  # Original: 100 gold
    
    # Ad Reward - Increase from 100 to 500
    'coins_window_watch_reward': {'InvoiceAmount': 500},  # Original: 100
}

# ============================================================================
# DON'T EDIT BELOW THIS LINE (unless you know what you're doing)
# ============================================================================

def modify_config(input_file, output_file=None):
    """
    Modify the game configuration file
    
    Args:
        input_file: Path to input ProductScheme.fxon
        output_file: Path to output file (default: adds _modified suffix)
    """
    input_path = Path(input_file)
    
    if output_file is None:
        output_file = input_path.parent / f"{input_path.stem}_modified{input_path.suffix}"
    
    # Load JSON
    print(f"Loading {input_file}...")
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} items")
    
    # Apply modifications
    modified_count = 0
    for item in data:
        item_id = item['Id']
        if item_id in MODIFICATIONS:
            mods = MODIFICATIONS[item_id]
            
            # Show what we're changing
            old_values = {
                'InvoiceAmount': item['RelatedInvoices'][0]['InvoiceAmount'],
                'InvoiceCurrency': item['RelatedInvoices'][0]['InvoiceCurrency']
            }
            
            # Apply changes
            for key, value in mods.items():
                item['RelatedInvoices'][0][key] = value
            
            # Show the change
            print(f"  {item_id}:")
            if 'InvoiceCurrency' in mods:
                currency_name = "coins" if mods['InvoiceCurrency'] == 0 else "gold"
                old_currency_name = "coins" if old_values['InvoiceCurrency'] == 0 else "gold"
                print(f"    Currency: {old_currency_name} → {currency_name}")
            if 'InvoiceAmount' in mods:
                print(f"    Amount: {old_values['InvoiceAmount']} → {mods['InvoiceAmount']}")
            
            modified_count += 1
    
    # Save modified version
    print(f"\nModified {modified_count} items")
    print(f"Saving to {output_file}...")
    
    with open(output_file, 'w') as f:
        json.dump(data, f, separators=(',', ':'))
    
    print("Done!")
    return output_file

def verify_changes(file_path):
    """Verify that changes were applied correctly"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    print("\n" + "="*60)
    print("VERIFICATION - Current Values:")
    print("="*60)
    
    for item in data:
        if item['Id'] in MODIFICATIONS:
            currency = "coins" if item['RelatedInvoices'][0]['InvoiceCurrency'] == 0 else "gold"
            amount = item['RelatedInvoices'][0]['InvoiceAmount']
            print(f"{item['Id']:30} {amount:8} {currency}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python modify_game_config.py <input_file> [output_file]")
        print("Example: python modify_game_config.py ProductScheme.fxon")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    output_path = modify_config(input_file, output_file)
    verify_changes(output_path)
