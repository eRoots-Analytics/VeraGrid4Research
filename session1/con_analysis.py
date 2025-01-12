import GridCalEngine as gce
import numpy as np
import pandas as pd
from GridCalEngine.Simulations.PowerFlow.power_flow_worker import multi_island_pf_nc

# load a grid (.gridcal, .m (Matpower), .raw (PSS/e) .rawx (PSS/e), .epc (PowerWorld), .dgs (PowerFactory)
grid = gce.open_file("case89pegase.m")

# we compile the grid into a numerical circuit for a particular time point (in this case, the snapshot)
nc = gce.compile_numerical_circuit_at(circuit=grid, t_idx=None)

# define the power flow options
opt = gce.PowerFlowOptions(solver_type=gce.SolverType.DC)

# run a powerr flow over the numerical circuit: This is a custom operation,
# since we want more fine control over the process
res_base = multi_island_pf_nc(nc, options=opt)

# gather the number of branches (lines, dc-lines, transformers, windings, series, impedances, switches)
m = nc.passive_branch_data.nelm

# declare the result matrices
con_flows = np.zeros((m, m))
lodf = np.zeros((m, m))

# loop over the number of branches
for k in range(m):

    # collect the state of a branch
    prev_state = nc.passive_branch_data.active[k]

    # failing the branch; Note we're directly modifying the numerical circuit instead of the MultiCircuit
    # this renders a much faster execution, since we're skipping the compilation step
    nc.passive_branch_data.active[k] = 0

    # Run the power flow on the modified numerical circuit
    res = multi_island_pf_nc(nc, options=opt)

    # Record the flows in MW
    con_flows[k, :] = res.Sf.real

    # Compute the Line-outage-distribution-factors (LODF)
    lodf[k, :] = (res_base.Sf.real - res.Sf.real) / (res_base.Sf.real + 1e-20)

    # recover the branch to the previous state
    nc.passive_branch_data.active[k] = prev_state

# Save the flows to CSV using pandas
df1 = pd.DataFrame(
    data=con_flows,
    index=nc.passive_branch_data.names,
    columns=nc.passive_branch_data.names
)
df1.to_csv("Contingencies.csv")

# Save the LODF to csv using pandas
df2 = pd.DataFrame(
    data=lodf,
    index=nc.passive_branch_data.names,
    columns=nc.passive_branch_data.names
)
df2.to_csv("LODF.csv")
