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

density = PropsSI('D', 'T', dew_point+273.15, 'P', pressure, mixture)
viscosity = PropsSI('V', 'T', dew_point+273.15, 'P', pressure, mixture)



print(f"Dew point temperature: {dew_point:.2f} °C")
print(f"At {dew_point} °C: Density = {density:.2f} kg/m³, Viscosity = {viscosity:.5e} Pa.s")

# Air at dew point temperature
T_air = dew_point
density = PropsSI('D', 'T', dew_point+273.15, 'P', pressure, "air")
viscosity = PropsSI('V', 'T', dew_point+273.15, 'P', pressure, "air")
print(f"Air at {dew_point} °C: Density = {density:.2f} kg/m³, Viscosity = {viscosity:.5e} Pa.s")

T_HOT_I = 102.6
T_HOT_O = 49.8

T_COLD_I = 35

T_COLD_O = T_COLD_I + (T_HOT_I - T_HOT_O)

print (T_HOT_I, T_HOT_O, T_COLD_I, T_COLD_O)

EFF = (T_HOT_I - T_HOT_O) / (T_HOT_I - T_COLD_I)
print(EFF)