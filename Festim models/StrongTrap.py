import festim as F
import numpy as np
import scipy.constants as const
import matplotlib.pyplot as plt
import os
my_model = F.Simulation()
N_A_const=const.N_A
my_model.mesh = F.MeshFromVertices(
    vertices=np.linspace(0, 1E-3, num=1001)
)
my_model.materials = F.Material(id=1, D_0=1.9e-7, E_D=0.2)
my_model.T = F.Temperature(value=1000)
P_up = 1E5 # Pa

my_model.boundary_conditions = [
    F.DirichletBC(surfaces=1, value=0.0088*N_A_const,field=0),
    F.DirichletBC(surfaces=2, value=0, field=0)
]
rho_n=6.338E28
trap = F.Trap(
            k_0=1.58E7/N_A_const,
            E_k=0.2,
            p_0=1e13,
            E_p=2.5,
            density=1E-3*rho_n,
            materials=my_model.materials.materials[0]
        )

my_model.traps = [trap]
my_model.settings = F.Settings(
    absolute_tolerance=1e10,
    relative_tolerance=1e-10,
    final_time=1E6  # s
    )
my_model.dt = F.Stepsize(initial_value=1E-2,
    dt_min=1E-3,
    stepsize_change_ratio=1.1,
    )
derived_quantities = F.DerivedQuantities([F.HydrogenFlux(surface=2)])


my_model.exports = [derived_quantities]

my_model.initialise()

my_model.run()

times = derived_quantities.t
computed_flux = derived_quantities.filter(surfaces=2).data

plt.plot(times, np.abs(computed_flux)/2, alpha=0.2, label="computed")
plt.ylim(bottom=0)
plt.xlabel("Time (s)")
plt.ylabel("Downstream flux (H2/m2/s)")
plt.ylim([1E-6,1E17])
plt.xlim([3E5,3.4E5])
if __name__ == '__main__':
    os.chdir('graph_scripts_and_results/Strong_Trap')

    plt.savefig('Strong_flux_festim.png')
    np.savetxt('Strong_flux_festim.txt',np.column_stack([times,np.abs(computed_flux)/2]))##Change flux from H to H2