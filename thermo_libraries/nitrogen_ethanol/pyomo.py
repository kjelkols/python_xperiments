from pyomo.environ import ConcreteModel, SolverFactory
from idaes.core import FlowsheetBlock
from idaes.generic_models.properties.activity_coeff_models.BTX_activity_coeff_VLE import configuration, BTXParameterBlock
from idaes.generic_models.unit_models import Flash

# Create a Pyomo model
model = ConcreteModel()
model.fs = FlowsheetBlock(dynamic=False)
model.fs.properties = BTXParameterBlock(default=configuration)

# Add flash unit
model.fs.flash = Flash(default={"property_package": model.fs.properties})

# Set conditions
model.fs.flash.inlet.temperature.fix(110 + 273.15)
model.fs.flash.inlet.pressure.fix(101325)
model.fs.flash.inlet.flow_mol.fix(1)
model.fs.flash.inlet.mole_frac_comp["benzene"].fix(0.4)
model.fs.flash.inlet.mole_frac_comp["toluene"].fix(0.6)

# Solve for different temperatures
solver = SolverFactory("ipopt")
for T in range(110, 69, -1):
    model.fs.flash.inlet.temperature.fix(T + 273.15)
    results = solver.solve(model)
    if results.solver.termination_condition == "optimal":
        vapor_frac = model.fs.flash.vap_outlet.flow_mol.value
        print(f"At {T} °C: Vapor fraction is {vapor_frac:.4f}")
    else:
        print(f"At {T} °C: No solution")
