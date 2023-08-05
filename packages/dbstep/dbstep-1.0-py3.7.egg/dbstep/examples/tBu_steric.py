from pymol.cgo import *
from pymol import cmd


cylinder = [
   CYLINDER, 0., 0., 0.000, -2.850, -0.000, 0.000, 0.100, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0,
   CYLINDER, 0., 0., 0.000, -2.600, 1.950, 0.000, 0.100, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0,
   CYLINDER, 0., 0., 0., 0., 0., 3.750, 0.1, 1.0, 1.0, 1.0, 0., 0.0, 1.0,
]
cmd.load_cgo(cylinder, "axes")

cmd.load("/Users/guilianluchini/Desktop/CSU/Research/Sterics/DBSTEP/dbstep/examples/tBu_transform.xyz")
cmd.show_as("spheres", "tBu_transform")
cmd.set("sphere_transparency", 0.5)
cmd.set("orthoscopic", "on")
