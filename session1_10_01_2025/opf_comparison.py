from matplotlib import pyplot as plt
import GridCalEngine as gce

# load a grid (.gridcal, .m (Matpower), .raw (PSS/e) .rawx (PSS/e), .epc (PowerWorld), .dgs (PowerFactory)
grid = gce.open_file("case89pegase.m")

# declare the snapshot opf
opf_options = gce.OptimalPowerFlowOptions(mip_solver=gce.MIPSolvers.HIGHS)
opf_driver = gce.OptimalPowerFlowDriver(grid=grid, options=opf_options)
opf_driver.run()
lin_opf_res = opf_driver.results


opf_options = gce.OptimalPowerFlowOptions(solver = gce.SolverType.NONLINEAR_OPF)
nlopf_driver = gce.OptimalPowerFlowDriver(grid=grid, options=opf_options)
nlopf_driver.run()
nl_opf_res = nlopf_driver.results

fig = plt.figure()
plt.ion()
plt.plot(lin_opf_res.Sf.real, label="Linear Pf")
plt.plot(nl_opf_res.Sf.real, label="NonLinear Pf")
plt.title("Linear and nonlinear OPF comparison")
plt.ylabel("MW")
plt.xlabel("Branch")
plt.legend()
plt.savefig("Opf comparison.png")
