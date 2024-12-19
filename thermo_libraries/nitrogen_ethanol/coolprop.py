import CoolProp.CoolProp as CP

# Define the mixture
fraction=0.1
fluid = "Ethanol[fraction]&Nitrogen[1-fraction]"  # Weight fractions converted to components


t = 110
p=101325

phase = CP.PhaseSI('T', t + 273.15, 'P', p, fluid)
print(f"At {t} °C: Phase is {phase}")

print ("Panic now");exit()

# Cool from 110 °C to 70 °C
for T in range(110, 69, -1):  # Temperature in Celsius
    try:
        pressure = 101325  # Atmospheric pressure in Pa
        phase = CP.PhaseSI('T', T + 273.15, 'P', pressure, fluid)
        print(f"At {T} °C: Phase is {phase}")
    except ValueError:
        print(f"At {T} °C: Error in phase calculation")

