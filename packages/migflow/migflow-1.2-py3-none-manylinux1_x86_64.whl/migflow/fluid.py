# MigFlow - Copyright (C) <2010-2020>
# <Universite catholique de Louvain (UCL), Belgium
#  Universite de Montpellier, France>
#
# List of the contributors to the development of MigFlow: see AUTHORS file.
# Description and complete License: see LICENSE file.
#
# This program (MigFlow) is free software:
# you can redistribute it and/or modify it under the terms of the GNU Lesser General
# Public License as published by the Free Software Foundation, either version
# 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program (see COPYING and COPYING.LESSER files).  If not,
# see <http://www.gnu.org/licenses/>.

"""Model for Immersed Granular Flow -- Fluid user interface

    Contact: jonathan.lambrechts@uclouvain.be
    Webpage: www.migflow.be

    MigFlow computes immersed granular flows using an unresolved FEM-DEM model.
    The continuous phase (mixture) is computed by solving averaged Navier-Stokes equations on unstructured meshes with the continuous finite element method.
"""

from ctypes import *
import numpy as np
import os
import sys
from . import VTK
from ._tools import gmsh,timeit
try :
    from .petsclsys import LinearSystem
except :
    print("PETSc4py not available, falling back to scipy linear system")
    from .scipylsys import LinearSystem

dir_path = os.path.dirname(os.path.realpath(__file__))
lib2 = np.ctypeslib.load_library("libmbfluid2",dir_path)
lib3 = np.ctypeslib.load_library("libmbfluid3",dir_path)

BNDCB = CFUNCTYPE(None,c_int,POINTER(c_double),POINTER(c_double))
class _Bnd :
    def __init__(self, b, dim) :
        self._b = b
        self._dim = dim
    def apply(self, n, xp, vp) :
        nv = len(self._b)
        x = np.frombuffer(cast(xp, POINTER(int(n)*self._dim*c_double)).contents).reshape([n,-1])
        v = np.frombuffer(cast(vp, POINTER(int(n)*nv*c_double)).contents).reshape([n,nv])
        for i in range(nv):
            if callable(self._b[i]) :
                v[:,i] = self._b[i](x)
            else :
                v[:,i] = self._b[i]

def _is_string(s) :
    if sys.version_info >= (3, 0):
        return isinstance(s, str)
    else :
        return isinstance(s, basestring)

def _np2c(a,dtype=float) :
    tmp = np.require(a,dtype,"C")
    r = c_void_p(tmp.ctypes.data)
    r.tmp = tmp
    return r

def _load_msh(mesh_file_name, lib, dim) :
        """
        mesh_file_name -- Name of the mesh.msh file containing information about the domain
        """
        etype = 2 if dim == 2 else 4
        betype = 1 if dim == 2 else 2
        gmsh.model.add("tmp")
        gmsh.open(mesh_file_name)
        gmsh.model.mesh.renumberNodes()
        _, x, _ = gmsh.model.mesh.getNodes()
        x = x.reshape([-1,3])
        _, el = gmsh.model.mesh.getElementsByType(etype)
        el = (el-1).reshape([-1,dim+1])
        bnd = []
        btag = []
        bname = []
        periodic_nodes = []
        for edim, etag  in gmsh.model.getEntities() :
            ptag, cnodes, pnodes, _ = gmsh.model.mesh.getPeriodicNodes(edim, etag)
            if ptag == etag or len(cnodes) == 0: continue
            periodic_nodes.extend(zip(cnodes,pnodes))
        for ip,(pdim, ptag)  in enumerate(gmsh.model.getPhysicalGroups(dim-1)) :
            bname.append(gmsh.model.getPhysicalName(pdim,ptag))
            for etag in gmsh.model.getEntitiesForPhysicalGroup(pdim, ptag):
                for eltype, _, elnodes in zip(*gmsh.model.mesh.getElements(pdim,etag)):
                    if eltype != betype: 
                        continue
                    bnd.append(elnodes-1)
                    btag.append(np.full((elnodes.shape[0]//dim), ip))
        periodic_nodes = np.array(periodic_nodes,dtype=np.int32).reshape([-1,2])-1
        bnd = np.hstack(bnd).reshape([-1,dim])
        btag = np.hstack(btag)
        cbname = (c_char_p*len(bname))(*(i.encode() for i in bname))

        # remove nodes and boundaries not connected to elements
        keepnodes = np.full(x.shape[0], False, np.bool)
        keepnodes[el] = True
        newidx = np.cumsum(keepnodes)-1
        el = newidx[el]
        x = x[keepnodes,:]
        periodic_nodes = newidx[periodic_nodes]
        keepbnd = np.full(bnd.shape[0], True, np.bool)
        for i in range(dim) :
            keepbnd = np.logical_and(keepbnd, keepnodes[bnd[:,i]])
        bnd = newidx[bnd][keepbnd,:]
        btag = btag[keepbnd]
        is_parent = np.full([x.shape[0]],True,np.bool)
        is_parent[periodic_nodes[:,0]] = False
        periodic_parent = np.cumsum(is_parent)-1
        periodic_parent[periodic_nodes[:,0]] = periodic_parent[periodic_nodes[:,1]]
        lib.mesh_new_from_elements.restype = c_void_p
        return c_void_p(lib.mesh_new_from_elements(
                c_int(x.shape[0]),_np2c(x,np.float64),
                c_int(el.shape[0]),_np2c(el,np.int32),
                c_int(bnd.shape[0]),_np2c(bnd,np.int32),
                _np2c(btag,np.int32),c_int(len(cbname)),cbname,
                _np2c(periodic_parent,np.int32)))

class FluidProblem :
    """Creates the numerical representation of the fluid."""

    def __init__(self, dim, g, mu, rho, sigma=0, coeff_stab=0.01, volume_drag=0., quadratic_drag=0., petsc_solver_type="", drag_in_stab=1, drag_coefficient_factor=1, ip_factor=1, temporal=True, advection=True):
        """Builds the fluid structure.

        Keyword arguments:
        dim -- Dimension of the problem
        g -- Gravity vector
        viscosity -- List of fluid phases viscosities (this should be a vector whom dimension specify if there is one or two fluid)
        density -- List of fluid phases densities (this should be a vector whom dimension specify if there is one or two fluid)
        sigma -- Surface tension (only when there are two fluids)
        coeff_stab -- Optional argument used as coefficient for extra diffusivity added to stabilise the advection of concentration (only for two fluid problem) 
        petsc_solver_type -- Optional argument to specify solver option (only when petsc is used)
        drag_in_stab -- States if the drag force is in the stabilisation term
        drag_coefficient_factor -- Factor multiplicating the drag coefficient
        temporal -- Enables d/dt (i.e. False = steady)
        advection -- Enables advective terms (i.e. False = Stokes, True = Navier-Stokes)


        Raises:
        ValueError -- If the dimension differs from 2 or 3
        NameError -- If C builder cannot be found
        """
        self.solver_options = petsc_solver_type
        self.strong_cb_ref = []
        self.weak_cb_ref = []
        self.sys = None
        if dim == 2 :
            self._lib = lib2
        elif dim == 3 :
            self._lib = lib3
        else :
            raise ValueError("dim should be 2 or 3.")
        self._lib.fluid_problem_new.restype = c_void_p
        n_fluids = np.require(rho,"float","C").reshape([-1]).shape[0]
        self._n_fluids = n_fluids
        self._dim = dim
        self._fp = c_void_p(self._lib.fluid_problem_new(_np2c(g), n_fluids, _np2c(mu), _np2c(rho), c_double(sigma), c_double(coeff_stab), c_double(volume_drag), c_double(quadratic_drag), c_int(drag_in_stab),c_double(drag_coefficient_factor),c_double(ip_factor),c_int(temporal), c_int(advection)))
        if self._fp == None :
            raise NameError("Cannot create fluid problem.")

    def __del__(self):
        """Deletes the fluid structure."""
        if(self._fp is not None) :
            self._lib.fluid_problem_free(self._fp)

    def load_msh(self, mesh_file_name) :
        """Sets the domain geometry for the fluid computation.

        Keyword argument:
        mesh_file_name -- Name of the mesh.msh file containing information about the domain
        """
        mesh = _load_msh(mesh_file_name, self._lib, self.dimension())
        self._lib.fluid_problem_set_mesh(self._fp, mesh)
        self.sys = None
        gmsh.model.remove()

    def set_wall_boundary(self, tag, pressure=None, velocity=None, compute_viscous_term=1) :
        """Sets the weak boundaries (=normal fluxes) for the fluid problem.

        Keyword arguments:
        tag -- Physical tag (or list of tags), set in the mesh.geo file, of the wall boundaries
        pressure -- The pressure value if imposed (callback or number)
        velocity -- The velocity value if imposed (callback or number)
        """
        if not _is_string(tag) :
            for t in tag :
                self.set_wall_boundary(t,pressure)
            return
        pid = -1
        vid = -1
        cb_or_value = None
        if pressure is not None:
            cb_or_value = [pressure]
            pid = 0
        if velocity is not None:
            cb_or_value = velocity
            vid = 0
        if pressure is not None and velocity is not None:
            cb_or_value = velocity+[pressure]
            vid = 0
            pid = self._dim
        bndcb = BNDCB(_Bnd(cb_or_value,self._dim).apply)
        self.weak_cb_ref.append(bndcb)
        self._lib.fluid_problem_set_weak_boundary(self._fp,tag.encode(), c_int(0), bndcb, c_int(vid), c_int(pid), c_int(-1), c_int(-1), c_int(int(compute_viscous_term)))

    def set_symmetry_boundary(self, tag, pressure=None):
        """Sets the symmetry boundaries (=normal fluxes) for the fluid problem.

        Keyword arguments:
        tag -- Physical tag (or list of tags), set in the mesh.geo file, of the symmetry boundaries
        pressure -- The pressure value if imposed (callback or number)
        velocity -- The velocity value if imposed (callback or number)
        """
        if not _is_string(tag):
            for t in tag:
                self.set_symmetry_boundary(t,pressure)
            return
        pid = -1
        vid = -1
        cb_or_value = None
        if pressure is not None:
            cb_or_value = [pressure]
            pid = 0
        bndcb = BNDCB(_Bnd(cb_or_value, self._dim).apply)
        self.weak_cb_ref.append(bndcb)
        self._lib.fluid_problem_set_weak_boundary(self._fp, tag.encode(), c_int(0), bndcb, c_int(vid), c_int(pid), c_int(-1), c_int(-1), c_int(-1))

    def set_open_boundary(self, tag, velocity=None, pressure=None, porosity=1, concentration=1, compute_viscous_term=1):
        """Sets the weak boundaries (=normal fluxes) for the fluid problem.

        Keyword arguments:
        tag -- Physical tag (set in the mesh.geo file) of the boundary on which the flux type is added
        velocity -- The velocity value if imposed (callback or number)
        pressure -- The pressure value if imposed (callback or number)
        porosity -- Porosity value outside the boudary
        concentration -- Concentration outside the boundary

        Raises:
        NameError -- If the specified porosity outside the boundary is too small
        NameError -- If velocity and pressure are not specified or if they are both specified at the open boundary. It should be one or the other
        NameError -- If the dimension of the velocity vector is not equal to the physical dimension of the problem
        """
        if porosity < 1e-3 :
            raise NameError("Inflow porosity too small!")
        if (velocity is None and pressure is None) or (velocity is not None and pressure is not None)  :
            raise NameError("Pressure or Velocity (but not both) should be specified at open boundaries")
        if (velocity is not None and len(velocity) != self._dim)  :
            raise NameError("len(velocity) != dimension at open boundaries")
        if velocity is not None :
            cb_or_value = velocity+[porosity]
            vid = 0
            cid = self._dim
            pid = -1
            n = self._dim+1
        else :
            cb_or_value = [pressure]+[porosity]
            pid = 0
            cid = 1
            vid = -1
            n = 2
        if self._n_fluids == 2 :
            cb_or_value += [concentration]
            aid = n
        else :
            aid = -1

        bndcb = BNDCB(_Bnd(cb_or_value, self._dim).apply)
        self.weak_cb_ref.append(bndcb)
        self._lib.fluid_problem_set_weak_boundary(self._fp, tag.encode(),c_int(1),bndcb,c_int(vid),c_int(pid),c_int(cid),c_int(aid),c_int(int(compute_viscous_term)))

    def set_strong_boundary(self, tag, field,callback_or_value, row=None) :
        """Sets the strong boundaries (=constrains) for the fluid problem.

        Keyword arguments:
        tag -- Physical tag (set in the mesh.geo file) of the boundary on which the constraint is added
        field -- Constrained field O: x-velocity; 1: y-velocity; 2: pressure
        callback_or_value -- Value assigned to the specified field on the specified boundary
        row -- Optional argument specifying the row on which the constrain has to be applied (if None the constrain is normally applied on the row field)
        """
        if row is None :
            row = field
        bndcb = BNDCB(_Bnd([callback_or_value], self._dim).apply)
        self.strong_cb_ref.append(bndcb)
        self._lib.fluid_problem_set_strong_boundary(self._fp, tag.encode(), c_int(field), c_int(row), bndcb)

    def adapt_mesh(self, lcmax, lcmin, n_el, old_n_particles, old_particle_position, old_particle_volume, cmax=1, cmin=1) :
        """Adapts the mesh.

        Keyword arguments:
        lcmax -- Maximum mesh radius
        lcmin -- Minimum mesh radius
        n_el -- Number of element wanted
        old_n_particles -- Number of particles at the previous time step
        old_particle_position -- Position of the particles at the previous time step
        old_particle_volume -- Volume of the particles at the previous time step
        cmax -- Optional argument to weigh maximum gradient used in the adaptation formula
        cmin -- Optional argument to weigh minimum gradient used in the adaptation formula
        """
        self._lib.fluid_problem_adapt_gen_mesh(self._fp, c_double(lcmax), c_double(lcmin), c_double(n_el), c_double(cmax), c_double(cmin))
        mesh = _load_msh("adapt/mesh.msh", self._lib, self.dimension())
        self._lib.fluid_problem_adapt_mesh(self._fp, mesh, c_double(lcmax), c_double(lcmin), c_double(n_el), c_double(cmax), c_double(cmin), c_int(old_n_particles), _np2c(old_particle_position), _np2c(old_particle_volume))
        self.sys = None

    def _mesh_boundaries(self) :
        n = self._lib.fluid_problem_mesh_n_boundaries(self._fp)
        bnds = {}
        for i in range(n) :
            bsize = c_int()
            bname = c_char_p()
            self._lib.fluid_problem_mesh_boundary_info(self._fp, c_int(i),byref(bname),byref(bsize))
            nodes = np.ndarray([bsize.value,self._dim],np.int32)
            self._lib.fluid_problem_mesh_boundary_interface_nodes(self._fp,c_int(i),c_void_p(nodes.ctypes.data))
            bnds[bname.value] = nodes
        return bnds

    def write_vtk(self, output_dir, it ,t, stab=False):
        """Writes output file for post-visualization.
        Keyword arguments:
        output_dir -- Output directory
        it -- Computation iteration
        t -- Computation time
        stab -- If True exports the stabilisation parametres in the output files
        """
        v = self.solution()[:,:self._dim]
        da = self.concentration_dg_grad()
        cell_data = []
        if self._dim == 2 :
            v = np.insert(v,self._dim,0,axis=1)
            da = np.insert(da,self._dim,0,axis=1)
        data = [
            ("pressure",self.solution()[:,[self._dim]]),
            ("velocity",v),
            ("porosity",self.porosity()),
            ("old_porosity",self.old_porosity()),
            ("grad",da),
            ("parent_node_id", self.parent_nodes())
            ]
        if self._n_fluids == 2 :
            cell_data.append(("curvature",self.curvature()))
            cell_data.append(("concentration",self.concentration_dg()))
            cell_data.append(("stab",self._get_matrix("stab_param",self.n_elements(),1)))
        field_data = [(b"Boundary %s"%(name), nodes) for name,nodes in self._mesh_boundaries().items()]
        connectivity = self.elements()
        types = np.repeat([5 if self._dim == 2 else 10],connectivity.shape[0])
        offsets = np.cumsum(np.repeat([self._dim+1],connectivity.shape[0])).astype(np.int32)
        VTK.write(output_dir+"/fluid",it,t,(types,connectivity,offsets),self.coordinates(),data,field_data,cell_data)

    def export_vtk(self, output_dir, t, it, stab=False) :
        print("Careful this function is deprecated... \n\tUse write_vtk instead !")
        self.write_vtk(output_dir, it, t, stab)

    def read_vtk(self, dirname, i):
        """Reads output file to reload computation.

        Keyword arguments:
        filename -- Name of the file to read
        """
        filename = dirname + "/fluid_%05d.vtu"%i
        x,cells,data,cdata,fdata = VTK.read(filename)
        mesh_boundaries = {name[9:]:nodes for name,nodes in fdata.items() if name.startswith("Boundary ")}
        cbnd_names = (c_char_p*len(mesh_boundaries))(*(i.encode() for i in mesh_boundaries.keys()))
        el = cells["connectivity"].reshape([-1,self._dim+1])
        nbnd = len(mesh_boundaries)
        bnds = np.vstack(list(mesh_boundaries.values()))
        bnd_tags = np.repeat(list(range(nbnd)),list([v.shape[0] for v in mesh_boundaries.values()]))
        bnd_tags = np.require(bnd_tags,np.int32,"C")
        self._lib.mesh_new_from_elements.restype = c_void_p
        _mesh = c_void_p(self._lib.mesh_new_from_elements(
                c_int(x.shape[0]),_np2c(x,np.float64),
                c_int(el.shape[0]),_np2c(el,np.int32),
                c_int(bnds.shape[0]),_np2c(bnds,np.int32),
                _np2c(bnd_tags,np.int32),c_int(len(cbnd_names)),cbnd_names,
                _np2c(data["parent_node_id"],np.int32) if "parent_node_id"  in data else None))
        self._lib.fluid_problem_set_mesh(self._fp, _mesh)
        sol = self.solution()
        sol[:,:self._dim] = data["velocity"][:,:self._dim]
        sol[:,[self._dim]] = data["pressure"]
        if self._n_fluids == 2 :
            self.concentration_dg()[:] = cdata["concentration"]
        self.porosity()[:] = data["porosity"]
        self.old_porosity()[:] = data["old_porosity"]
        self.sys = None


    def import_vtk(self, filename) :
        print("Careful this function is deprecated... \n\tUse read_vtk instead !")
        x,cells,data,cdata,fdata = VTK.read(filename)
        mesh_boundaries = {name[9:]:nodes for name,nodes in fdata.items() if name.startswith("Boundary ")}
        cbnd_names = (c_char_p*len(mesh_boundaries))(*(i.encode() for i in mesh_boundaries.keys()))
        el = cells["connectivity"].reshape([-1,self._dim+1])
        nbnd = len(mesh_boundaries)
        bnds = np.vstack(list(mesh_boundaries.values()))
        bnd_tags = np.repeat(list(range(nbnd)),list([v.shape[0] for v in mesh_boundaries.values()]))
        bnd_tags = np.require(bnd_tags,np.int32,"C")
        self._lib.mesh_new_from_elements.restype = c_void_p
        _mesh = c_void_p(self._lib.mesh_new_from_elements(
                c_int(x.shape[0]),_np2c(x,np.float64),
                c_int(el.shape[0]),_np2c(el,np.int32),
                c_int(bnds.shape[0]),_np2c(bnds,np.int32),
                _np2c(bnd_tags,np.int32),c_int(len(cbnd_names)),cbnd_names,
                _np2c(data["parent_node_id"],np.int32) if "parent_node_id"  in data else None))
        self._lib.fluid_problem_set_mesh(self._fp, _mesh)
        sol = self.solution()
        sol[:,:self._dim] = data["velocity"][:,:self._dim]
        sol[:,[self._dim]] = data["pressure"]
        if self._n_fluids == 2 :
            self.concentration_dg()[:] = cdata["concentration"]
        self.porosity()[:] = data["porosity"]
        self.old_porosity()[:] = data["old_porosity"]
        self.sys = None
        
    def compute_node_force(self, dt) :
        """Computes the forces to apply on each grain resulting from the fluid motion.

        Keyword arguments:
        dt -- Computation time step
        """
        forces = np.ndarray([self.n_particles,self._dim],"d",order="C")
        self._lib.fluid_problem_compute_node_particle_force(self._fp, c_double(dt), c_void_p(forces.ctypes.data))
        return forces

    def compute_node_torque(self, dt) :
        """Computes the angular drags to apply on each grain resulting from the fluid motion.
        Only in 2D
        Keyword arguments:
        dt -- Computation time step
        """
        torques = np.ndarray([self.n_particles,1],"d",order="C")

        self._lib.fluid_problem_compute_node_particle_torque(self._fp, c_double(dt), c_void_p(torques.ctypes.data))
        return torques

    def implicit_euler(self, dt, check_residual_norm=-1, reduced_gravity=0, stab_param=0.) :
        """Solves the fluid equations.

        Keyword arguments:
        dt -- Computation time step
        check_residual_norm -- If > 0, checks the residual norm after the system resolution
        reduced_graviy -- If True simulations are run with a reduced gravity (not to use in two fluids simulations)
        stab_param -- If zero pspg/supg/lsic stabilisation is computed otherwise the value is used as a coefficient for a pressure laplacian stabilisation term
        """
        self._lib.fluid_problem_set_reduced_gravity(self._fp,c_int(reduced_gravity))
        self._lib.fluid_problem_set_stab_param(self._fp,c_double(stab_param))
        self._lib.fluid_problem_apply_boundary_conditions(self._fp)
        solution_old = self.solution().copy()
        self._lib.fluid_problem_reset_boundary_force(self._fp)
        self._lib.fluid_problem_compute_stab_parameters(self._fp,c_double(dt))

        periodic_map = self._get_matrix("periodic_mapping", self.n_nodes(), 1, c_int).flatten()
        if self.sys is None :
            self.sys = LinearSystem(periodic_map[self.elements()],self.n_fields(),self.solver_options)
        sys = self.sys
        rhs = np.zeros(sys.globalsize)
        localv = np.ndarray([sys.localsize*self.n_elements()])
        localm = np.ndarray([sys.localsize**2*self.n_elements()])
        self._lib.fluid_problem_assemble_system(self._fp,_np2c(rhs),_np2c(solution_old),c_double(dt),_np2c(localv),_np2c(localm))
        sys.local_to_global(localv,localm,rhs)
        if check_residual_norm > 0 :
            norm0 = np.linalg.norm(rhs)
        self.solution()[:] -= sys.solve(rhs).reshape([-1,self.n_fields()])[periodic_map]
        if check_residual_norm > 0 :
            sys.zero_matrix()
            rhs[:] = 0
            self._lib.fluid_problem_assemble_system(self._fp,_np2c(rhs),_np2c(solution_old),c_double(dt),_np2c(localv),_np2c(localm))
            sys.local_to_global(localv,localm,rhs)
            norm = np.linalg.norm(rhs)
            print("norm",norm)
            if norm > check_residual_norm :
                raise ValueError("wrong derivative or linear system precision")
        self._lib.fluid_problem_node_force_volume(self._fp,_np2c(solution_old),c_double(dt),None,None)

    def compute_cfl(self):
        """Computes the CFL number divided by the time step

        """
        nv = np.linalg.norm(self.solution()[:,:self._dim],axis=1)
        nvmax = np.max(nv[self.elements()],axis=1,keepdims=True)
        h = self._get_matrix("element_size",self.n_elements(),1)
        cfl = nvmax / (0.1*h)
        return np.max(cfl)

    def advance_concentration(self,dt):
        """Solves the advection equation for the concentration using the current velocity field.

        Keyword arguments:
        dt -- Computation time step
        """
        if self._n_fluids == 2 :
            cfl = self.compute_cfl()
            nsub = int(cfl*dt+1)
            if (nsub != 1) :
                print("sub-iterating advection for cfl : %i sub-iterations"%nsub)
            for i in range(nsub) :
                self._lib.fluid_problem_advance_concentration(self._fp,c_double(dt/nsub))

    def set_particles(self, mass, volume, position, velocity, contact):
        """Set location of the grains in the mesh and compute the porosity in each cell.

        Keyword arguments:
        mass -- List of particles mass
        volume -- List of particles volume
        position -- List of particles centre positions 
        velocity -- List of particles velocity
        contact -- List of particles contact resultant forces
        """
        self.n_particles = mass.shape[0]
        self._lib.fluid_problem_set_particles(self._fp,c_int(mass.shape[0]),_np2c(mass),_np2c(volume),_np2c(position),_np2c(velocity),_np2c(contact))

    def move_particles(self, position, velocity, contact):
        """Set location of the grains in the mesh and compute the porosity in each cell.

        Keyword arguments:
        position -- List of particles centre positions 
        velocity -- List of particles velocity
        contact -- List of particles contact resultant forces
        """
        self._lib.fluid_problem_move_particles(self._fp,c_int(velocity.shape[0]),_np2c(position),_np2c(velocity),_np2c(contact))

    def _get_matrix(self, f_name, nrow, ncol,typec=c_double) :
        f = getattr(self._lib,"fluid_problem_"+f_name)
        f.restype = POINTER(typec)
        return np.ctypeslib.as_array(f(self._fp),shape=(nrow,ncol))

    def solution(self) :
        """Gives access to the fluid field value at the mesh nodes."""
        return self._get_matrix("solution", self.n_nodes(), self.n_fields())

    def velocity(self) :
        """Gives access to the fluid velocity value at the mesh nodes."""
        return self.solution()[:,:-1]
        
    def mesh_velocity(self) :
        """Give access to the mesh velocity value at the mesh nodes."""
        return self._get_matrix("mesh_velocity", self.n_nodes(), self._dim)

    def pressure(self) :
        """Gives access to the fluid field value at the mesh nodes."""
        return self.solution()[:,[-1]]

    def boundary_force(self) :
        """Give access to force exerted by the fluid on the boundaries."""
        return self._get_matrix("boundary_force", self._lib.fluid_problem_mesh_n_boundaries(self._fp), self._dim)

    def coordinates(self) :
        """Gives access to the coordinate of the mesh nodes."""
        return self._get_matrix("coordinates",self.n_nodes(), 3)

    def parent_nodes(self):
        """Gives access to the parent nodes of each node."""
        return self._get_matrix("periodic_mapping", self.n_nodes(),1, typec=c_int32)

    def n_fluids(self) :
        """Returns the number of fluids."""
        return self._n_fluids

    def elements(self):
        """Gives read-only access to the elements of the mesh."""
        return self._get_matrix("elements", self.n_elements(), self._dim+1,c_int)

    def n_elements(self):
        """Returns the number of mesh nodes."""
        self._lib.fluid_problem_n_elements.restype = c_int
        return self._lib.fluid_problem_n_elements(self._fp)

    def n_fields(self):
        """Returns the number of fluid fields."""
        self._lib.fluid_problem_n_fields.restype = c_int
        return self._lib.fluid_problem_n_fields(self._fp)

    def n_nodes(self):
        """Returns the number of mesh nodes."""
        self._lib.fluid_problem_n_nodes.restype = c_int
        return self._lib.fluid_problem_n_nodes(self._fp)

    def porosity(self):
        """Returns the porosity at nodes"""
        return self._get_matrix("porosity", self.n_nodes(), 1)

    def set_concentration_cg(self,concentration):
        """Sets the concentration at nodes"""
        concentration = concentration.reshape((self.n_nodes(),1))
        self._lib.fluid_problem_set_concentration_cg(self._fp,_np2c(concentration))

    def concentration_dg(self):
        """Returns the concentration at discontinuous nodes"""
        return self._get_matrix("concentration_dg", self.n_elements(), self._dim+1)

    def concentration_dg_grad(self):
        """Returns the concentration at discontinuous nodes"""
        return self._get_matrix("concentration_dg_grad", self.n_nodes(), self._dim)

    def curvature(self):
        """Returns the porosity at previous time step"""
        return self._get_matrix("curvature", self.n_elements(), 1)

    def old_porosity(self):
        """Returns the porosity at previous time step"""
        return self._get_matrix("old_porosity", self.n_nodes(), 1)

    def volume_flux(self, bnd_tag):
        """Computes the integral of the (outgoing) normal velocity through boundary with tag bnd_tag"""
        self._lib.fluid_problem_volume_flux.restype = c_double
        return self._lib.fluid_problem_volume_flux(self._fp,bnd_tag.encode())

    def particle_element_id(self) :
        """Returns the id of the mesh cell in which particles are located."""
        f = getattr(self._lib,"fluid_problem_particle_element_id")
        f.restype = c_void_p
        fs = getattr(self._lib,"fluid_problem_n_particles")
        fs.restype = c_int
        ptr = f(self._fp)
        size = fs(self._fp)
        buf = (size*c_int).from_address(ptr)
        return np.ctypeslib.as_array(buf)

    def particle_uvw(self) :
        """Returns the coordinates of the particles inside their element"""
        return self._get_matrix("particle_uvw",self.n_particles,self._dim)

    def particle_position(self) :
        """Gives access to stored paricles position."""
        return self._get_matrix("particle_position", self.n_particles, self._dim)

    def particle_velocity(self) :
        """Gives access to the stored particle velocity."""
        return self._get_matrix("particle_velocity", self.n_particles, self._dim)

    def particle_volume(self) :
        """Gives access to the fluid field value at the mesh nodes."""
        return self._get_matrix("particle_volume", self.n_particles, 1)

    def bulk_force(self) :
        """Gives access to the volume force at fluid nodes."""
        return self._get_matrix("bulk_force", self.n_nodes(), self._dim)

    def node_volume(self) :
        """Returns the volume associated with each node"""
        return self._get_matrix("node_volume",self.n_nodes(),1)

    def _n_physicals(self):
        f = self._lib.fluid_problem_private_n_physical
        f.restype = c_int
        return f(self._fp)

    def _physical(self,ibnd):
        f = self._lib.fluid_problem_private_physical
        phys_dim = c_int()
        phys_id = c_int()
        phys_n_nodes = c_int()
        phys_nodes = POINTER(c_int)()
        phys_name = c_char_p()
        phys_n_boundaries = c_int()
        phys_boundaries = POINTER(c_int)()
        f(self._fp,c_int(ibnd),byref(phys_name),byref(phys_dim),byref(phys_id),byref(phys_n_nodes),byref(phys_nodes),byref(phys_n_boundaries),byref(phys_boundaries))
        nodes = np.ctypeslib.as_array(phys_nodes,shape=(phys_n_nodes.value,)) if phys_nodes else np.ndarray([0],np.int32)
        bnd = np.ctypeslib.as_array(phys_boundaries,shape=(phys_n_boundaries.value,2)) if phys_boundaries else np.ndarray([2,0],np.int32)
        return phys_name.value,phys_dim.value,phys_id.value,nodes,bnd

    def dimension(self) :
        return self._dim

