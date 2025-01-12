import GridCalEngine as gce
import numpy as np
import pandas as pd
from GridCalEngine.Simulations.PowerFlow.power_flow_worker import multi_island_pf_nc

# load a grid (.gridcal, .m (Matpower), .raw (PSS/e) .rawx (PSS/e), .epc (PowerWorld), .dgs (PowerFactory)
grid = gce.open_file("case89pegase.m")

nc = gce.compile_numerical_circuit_at(circuit=grid, t_idx=None)

opt = gce.PowerFlowOptions(solver_type=gce.SolverType.DC)
res_base = multi_island_pf_nc(nc, options=opt)

m = nc.passive_branch_data.nelm
con_flows = np.zeros((m, m))

for k in range(m):

    prev_state = nc.passive_branch_data.active[k]

    # failing the branch
    nc.passive_branch_data.active[k] = 0

    res = multi_island_pf_nc(nc, options=opt)
    con_flows[k, :] = res.Sf.real

    # recovering the branch
    nc.passive_branch_data.active[k] = prev_state

df = pd.DataFrame(
    data=con_flows,
    index=nc.passive_branch_data.names,
    columns=nc.passive_branch_data.names
)
df.to_csv("Contingencies.csv")