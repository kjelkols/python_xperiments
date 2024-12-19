from CoolProp.CoolProp import PropsSI

# Molecular weights (g/mol)
M_ethanol = 46.07
M_nitrogen = 28.013

# Weight fractions
w_ethanol = 0.4
w_nitrogen = 0.6

# Calculate mole fractions
n_ethanol = w_ethanol / M_ethanol
n_nitrogen = w_nitrogen / M_nitrogen
total_moles = n_ethanol + n_nitrogen

x_ethanol = n_ethanol / total_moles
x_nitrogen = n_nitrogen / total_moles

print(f"Mole fraction of ethanol: {x_ethanol:.4f}")
print(f"Mole fraction of nitrogen: {x_nitrogen:.4f}")

# Mixture definition for CoolProp (mole fractions)
mixture = f"Ethanol[{x_ethanol:.4f}]&Nitrogen[{x_nitrogen:.4f}]"

# Find dew point temperature
pressure = 101325  # Atmospheric pressure in Pa
dew_point = PropsSI('T', 'Q', 1, 'P', pressure, mixture) - 273.15  # Convert to Celsius
print(f"Dew point temperature: {dew_point:.2f} °C")
