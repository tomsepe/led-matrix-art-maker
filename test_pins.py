import board

# Print all available pin names
print("Available pin names:")
for name in dir(board):
    if not name.startswith('_'):  # Skip private attributes
        print(f"- {name}")

# Print any pins that might be related to I2C
print("\nPotential I2C pins:")
for name in dir(board):
    if 'I2C' in name or 'SDA' in name or 'SCL' in name:
        print(f"- {name}") 