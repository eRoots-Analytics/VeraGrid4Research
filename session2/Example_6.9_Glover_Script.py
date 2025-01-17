import GridCalEngine.api as gce

grid = gce.MultiCircuit()

# Buses
b1 = gce.Bus(name="Bus 1",
             Vnom=15,
             is_slack=True)
grid.add_bus(b1)

b2 = gce.Bus(name="Bus 2",
             Vnom=345)
grid.add_bus(b2)

b3 = gce.Bus(name="Bus 3",
             Vnom=15)
grid.add_bus(b3)

b4 = gce.Bus(name="Bus 4",
             Vnom=345)
grid.add_bus(b4)

b5 = gce.Bus(name="Bus 5",
             Vnom=345)
grid.add_bus(b5)

# Generators
g1 = gce.Generator(name='g1',
                   vset=1.0,
                   Snom=400)
grid.add_generator(b1, g1)

g2 = gce.Generator(name='g2',
                   vset=1.05,
                   Snom=800,
                   Qmin=4000,
                   Qmax=-2800)
grid.add_generator(b3, g2)

# Lines
grid.add_line(gce.Line(name="l1",
                       bus_from=b4,
                       bus_to=b2,
                       rate=1200,
                       r=0.009,
                       x=0.1,
                       b=1.72,
                       length=321.8688))

grid.add_line(gce.Line(name="l2",
                       bus_from=b5,
                       bus_to=b2,
                       rate=1200,
                       r=0.0045,
                       x=0.05,
                       b=0.88,
                       length=321.8688 / 2))

grid.add_line(gce.Line(name="l3",
                       bus_from=b5,
                       bus_to=b4,
                       rate=1200,
                       r=0.00225,
                       x=0.025,
                       b=0.44,
                       length=321.8688 / 4))

# Transformador
t1 = gce.Transformer2W(name="t1",
                       bus_from=b1,
                       bus_to=b5,
                       HV=345,
                       LV=15,
                       r=0.00150,
                       x=0.02,
                       g=0,
                       b=0,
                       nominal_power=400)
grid.add_transformer2w(t1)

t2 = gce.Transformer2W(
    name="t2",
    bus_from=b3,
    bus_to=b4,
    HV=345,
    LV=15,
    r=0.00075,
    x=0.01,
    g=0,
    b=0,
    nominal_power=800,
)
grid.add_transformer2w(t2)

# Loads
grid.add_load(b3, gce.Load("ld1", P=80, Q=40))

grid.add_load(b2, gce.Load("ld2", P=800, Q=280))

# PowerFlow
results = gce.power_flow(grid)

print(grid.name)
print('Converged:', results.converged, 'error:', results.error)
print(results.converged)
print(results.get_branch_df())
print(results.get_bus_df())
print(results.get_report_dataframe())

# gce.save_file(grid=grid, filename="ejemplo_glover_6_9.gridcal")

nc = gce.compile_numerical_circuit_at(circuit=grid, t_idx=None)

adm = nc.get_admittance_matrices()
Sbus = nc.get_power_injections()  # MW +j MVAr
Sbus_pu = nc.get_current_injections_pu()

print("Ybus:", adm.Ybus.todense())
print("Sbus:", Sbus)

print()
