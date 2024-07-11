import os
import festim as F
from materials import tungsten, cu, cucrzr, trap_conglo, trap_w2

## To be able to run this script, you need to be in the Mainfolder
model = F.Simulation()
## Move to the Iter2D folder

original_directory = os.getcwd()

if __name__ == "__main__" or __name__ == "test.py":
    
    os.chdir("Festim_models/ITER2D")

model.mesh = F.MeshFromXDMF(
    volume_file="mesh_domains.xdmf",
    boundary_file="mesh_boundaries.xdmf",
)

id_top_surf = 9
id_coolant_surf = 10
id_left_surf = 11
id_bottom = 12

# materials
tungsten.id = 8  # volume W
cu.id = 7  # volume Cu
cucrzr.id = 6  # volume CuCrZr
model.materials = F.Materials([tungsten, cu, cucrzr])

model.traps = F.Traps([trap_conglo, trap_w2])


# temperature
model.T = F.HeatTransferProblem(transient=False)


# boundary conditions
heat_flux_top = F.FluxBC(surfaces=id_top_surf, value=10e6, field="T")
# bug in FESTIM v0.9
convective_heat_flux_coolant = F.ConvectiveFlux(
    h_coeff=7e04, T_ext=323, surfaces=id_coolant_surf
)

heat_transfer_bcs = [heat_flux_top, convective_heat_flux_coolant]

instantaneous_recombination_toroidal = F.DirichletBC(
    value=0, surfaces=id_left_surf, field=0
)
instantaneous_recombination_bottom = F.DirichletBC(value=0, surfaces=id_bottom, field=0)

recombination_flux_coolant = F.RecombinationFlux(
    Kr_0=2.9e-14, E_Kr=1.92, order=2, surfaces=id_coolant_surf
)
h_implantation_top = F.ImplantationDirichlet(
    surfaces=id_top_surf, phi=1.61e22, R_p=9.52e-10, D_0=tungsten.D_0, E_D=tungsten.E_D
)

h_transport_bcs = [
    h_implantation_top,
    recombination_flux_coolant,
    instantaneous_recombination_toroidal,
    instantaneous_recombination_bottom,
]


model.boundary_conditions = heat_transfer_bcs + h_transport_bcs

model.settings = F.Settings(
    absolute_tolerance=1e10,
    relative_tolerance=1e-10,
    maximum_iterations=15,
    traps_element_type="DG",
    chemical_pot=True,
    final_time=1e7,
    transient=True,
    # linear_solver="mumps",
)

model.dt = F.Stepsize(1, stepsize_change_ratio=1.1, dt_min=1e2)


derived_quantities = F.DerivedQuantities(
    [
        F.TotalVolume(field="retention", volume=tungsten.id),
        F.TotalVolume(field="retention", volume=cu.id),
        F.TotalVolume(field="retention", volume=cucrzr.id),
        F.TotalVolume(field="solute", volume=tungsten.id),
        F.TotalVolume(field="solute", volume=cu.id),
        F.TotalVolume(field="solute", volume=cucrzr.id),
        # F.SurfaceFlux(field="solute", surface=id_coolant_surf),
        # F.SurfaceFlux(field="solute", surface=id_left_surf),
        # F.SurfaceFlux(field="solute", surface=id_bottom),
    ],
)

model.exports = F.Exports(
    [
        derived_quantities,
        F.XDMFExport("T", filename="temperature.xdmf"),
        F.XDMFExport("solute", filename="mobile.xdmf"),
        F.XDMFExport("retention", filename="retention.xdmf"),
    ]
)

# Go back to the base repo directory and then to the result directory
os.chdir("../../graph_scripts_and_results/ITER2D")
model.initialise()
model.run()
os.chdir(original_directory)
