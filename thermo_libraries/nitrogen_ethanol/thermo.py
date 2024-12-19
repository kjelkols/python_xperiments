from thermo import *
#import thermo
#from thermo import Mixture, ChemicalConstantsPackage, UNIFAC

# Constants and package setup
constants = ChemicalConstantsPackage.from_IDs(['ethanol', 'nitrogen'])
mixture = Mixture(
    zs=[0.4, 0.6],  # Mole fractions
    T=110 + 273.15, # Initial temperature in Kelvin
    P=101325,       # Atmospheric pressure
    constants=constants,
    HeatCapacityGases=None,
    activity_model=UNIFAC
)

# Cooling process
for T in range(110, 69, -1):  # Temperature in Celsius
    mixture.T = T + 273.15
    try:
        dew_point = mixture.dew_point_at_T()
        print(f"At {T} °C: Dew point is {dew_point - 273.15:.2f} °C")
    except Exception as e:
        print(f"At {T} °C: {str(e)}")
