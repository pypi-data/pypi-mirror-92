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

"""Model for Immersed Granular Flow -- Particles user interface

    Contact: jonathan.lambrechts@uclouvain.be
    Webpage: www.migflow.be

    MigFlow computes immersed granular flows using an unresolved FEM-DEM model.
    The discrete phase is computed batey updating iteratively the particle velocities until a set of velocities respecting the non-interpenetration contact law for the next time step is found
"""

from __future__ import division
from . import VTK
import shutil
import os
import sys
from ctypes import *
from ._tools import gmsh


import numpy as np
assert(np.lib.NumpyVersion(np.__version__) >= "1.17.0")

dir_path = os.path.dirname(os.path.realpath(__file__))
lib2 = np.ctypeslib.load_library("libscontact2",dir_path)
lib2fwr = np.ctypeslib.load_library("libscontact2fwr",dir_path)
lib3 = np.ctypeslib.load_library("libscontact3",dir_path)
lib3fwr = np.ctypeslib.load_library("libscontact3fwr",dir_path)

is_64bits = sys.maxsize > 2**32

def _np2c(a,dtype=np.float64) :
    tmp = np.require(a,dtype,"C")
    r = c_void_p(tmp.ctypes.data)
    r.tmp = tmp
    return r

class ParticleProblem :
    """Creates the numerical structure containing all the physical particles that appear in the problem"""

    def _get_array(self, fName, dtype) :
        f = getattr(self._lib,"particleProblem"+fName)
        f.restype = c_void_p
        ptr = f(self._p)
        if ptr is None :
            return np.ndarray((0),dtype)
        size = cast(ptr-(8 if is_64bits else 4), POINTER(c_size_t)).contents.value//dtype.itemsize
        buf = (size*np.ctypeslib.as_ctypes_type(dtype)).from_address(ptr)
        return np.ctypeslib.as_array(buf)

    def _get_matrix(self, fName, ncol) :
        f = getattr(self._lib,"particleProblem"+fName)
        f.restype = c_void_p
        ptr = f(self._p)
        if ptr is None :
            return np.ndarray((0,ncol))
        size = cast(ptr-(8 if is_64bits else 4), POINTER(c_size_t)).contents.value//8
        buf = (size*c_double).from_address(ptr)
        return np.ctypeslib.as_array(buf).reshape([-1,ncol])

    def _get_idx(self, fName) :
        f = getattr(self._lib,"particleProblem"+fName)
        f.restype = c_void_p
        ptr = f(self._p)
        if ptr is None :
            return np.ndarray((0,),dtype=np.int32)
        size = cast(ptr-(8 if is_64bits else 4), POINTER(c_size_t)).contents.value//4
        buf = (size*c_int).from_address(ptr)
        return np.ctypeslib.as_array(buf)

    def __init__(self, dim, friction_enabled=False, rotation_enabled=True) :
        """Builds the particles problem structure.

        Keyword arguments:
        dim -- Dimension of the problem

        Raises:
        ValueError -- If dimension differs from 2 or 3
        NameError -- If C builder cannot be found
        """
        self._dim = dim
        self._friction_enabled = friction_enabled
        if not friction_enabled :
            rotation_enabled = False;
        self._rotation_enabled = rotation_enabled
        if dim == 2 :
            self._lib = lib2 if rotation_enabled else lib2fwr
            self._coord_type = c_double*2
        elif dim == 3 :
            self._lib = lib3 if rotation_enabled else lib3fwr
            self._coord_type = c_double*3
        else :
            raise ValueError("Dimension should be 2 or 3.")
        self._lib.particleProblemNew.restype = c_void_p
        self._p = c_void_p(self._lib.particleProblemNew())
        if self._p == None :
            raise NameError("Cannot create particle problem.")

        bndtype =[('material',np.int32),('tag',np.int32)]
        self._disktype = np.dtype(bndtype+[('x',np.float64,dim),('v',np.float64,dim),('r',np.float64)])
        self._segmenttype = np.dtype(bndtype+[('p',np.float64,(2,dim)),('v',np.float64,(dim))])
        self._triangletype = np.dtype(bndtype+[('p',np.float64,(3,dim)),('v',np.float64,(dim))])
        self._periodicEntitytype = np.dtype([('etag', np.int32),('edim', np.int32),('periodic_transformation', np.float64, dim)])
        self._periodicSegmenttype = np.dtype([('entity_id', np.int64), ('p',np.float64,(2,dim))])
        self._periodicTriangletype = np.dtype([('entity_id', np.int64),('p', np.float64,(3,dim))])

    def __del__(self):
        """Deletes the particle solver structure."""
        if(self._p is not None) :
            self._lib.particleProblemDelete(self._p)

    def volume(self):
        """Returns the list of particle volumes."""
        if self._dim == 2 :
            return np.pi * self._get_matrix("Particle", 2)[:, [0]]**2
        else :
            return 4./3.*np.pi * self._get_matrix("Particle", 2)[:, [0]]**3

    def r(self) :
        """Returns the list of particle radii."""
        return self._get_matrix("Particle", 2)[:, 0][:,None]

    def mass(self):
        """Returns the list of particle masses."""
        return self._get_matrix("Particle", 2)[:, 1][:,None]

    def position(self):
        return self._get_matrix("Position", self._dim)

    def velocity(self):
        return self._get_matrix("Velocity", self._dim)

    def omega(self) : 
        d = 1 if self._dim==2 else 3
        if self._friction_enabled and self._rotation_enabled :
            return(self._get_matrix("Omega", d))
        else :
            return np.zeros((self.n_particles(),d))

    def save_state(self) :
        self._saved_velocity = np.copy(self.velocity())
        self._saved_position = np.copy(self.position())
        self._saved_segments = np.copy(self.segments())
        self._saved_disk = np.copy(self.disks())
        if self.dim() == 3 :
            self._saved_triangles = np.copy(self.triangles())

        if self._friction_enabled and self._rotation_enabled :
            self._saved_omega = np.copy(self.omega())

    def restore_state(self) :
        self.velocity()[:] = self._saved_velocity
        self.position()[:] = self._saved_position
        if self._friction_enabled and self._rotation_enabled :
            self.omega()[:] = self._saved_omega
        self.segments()[:] = self._saved_segments
        self.disks()[:] = self._saved_disk
        if self.dim() == 3 :
            self.triangles()[:] = self._saved_triangles

    def particle_material(self):
        """Returns the list of particle materials."""
        return self._get_idx("ParticleMaterial")

    def disk_tag(self):
        """Returns the list of boundary disk tag numbers."""
        return self._get_idx("DiskTag")

    def disks(self) :
        """Returns the list of boundary disks."""
        return self._get_array("Disk",self._disktype)

    def forced_flag(self):
        """Returns the list of particle flags indicating whether they are fixed or not."""
        return self._get_idx("ForcedFlag")

    def get_tag_id(self, tag = "default"):
        """Returns the number associated to a string tag."""
        return self._lib.particleProblemGetMaterialTagId(self._p, tag.encode())

    def n_particles(self) :
        """Returns the number of particles."""
        self._lib.particleProblemNParticle.restype = c_size_t
        return self._lib.particleProblemNParticle(self._p)

    def mu(self) :
        """Returns the matrix of the friction coefficients between materials."""
        return self._get_matrix("Mu", self._lib.particleProblemNMaterial(self._p))

    def segments(self):
        """Returns the list of boundary segments."""
        return self._get_array("Segment",self._segmenttype)

    def periodicEntity(self):
        """Returns the list of periodic entity."""
        return self._get_array("PeriodicEntity", self._periodicEntitytype)

    def periodicSegments(self):
        """Returns the list of periodic segments."""
        return self._get_array("PeriodicSegment", self._periodicSegmenttype)

    def periodicTriangles(self):
        """Returns the list of periodic triangles."""
        if self._dim == 2:
            return np.ndarray((0),self._periodicTriangletype)
        return self._get_array("PeriodicTriangle", self._periodicTriangletype)

    def triangles(self):
        """Returns the list of boundary triangles."""
        if self._dim == 2:
            return np.ndarray((0),self._triangletype)
        return self._get_array("Triangle",self._triangletype)

    def contact_forces(self):
        """Returns the contact forces on each grain."""
        return (self._get_matrix("ContactForces",self._dim))

    def get_boundary_forces(self,tag="default") :
        """Returns the net normal and tangential forces acting on a boundary because of the contacts.
        Keyword arguments:
        tag -- Name of the boundary
        """
        self._lib.particleProblemGetTagId.restype = c_size_t
        tag = self._lib.particleProblemGetTagId(self._p, tag.encode())
        def compute_fn_ft(contact_name,objects,tag) :
            o,v,b =self.get_contacts(contact_name)
            keep = objects["tag"][o[:,0]] == tag
            m = self.mass()[o[keep,1]]
            if m.shape[0] == 0 :
                return np.array([[0.]*self._dim]*2)
            fn = np.sum(m*b[keep,0,:]*v[keep,:][:,[0]],axis=0)
            ft = np.sum(m*b[keep,1,:]*v[keep,:][:,[1]],axis=0)
            if self._dim == 3:
                ft += np.sum(m*b[keep,2,:]*v[keep,:][:,[2]],axis=0)
            return np.array([fn,ft])
        f = compute_fn_ft("particle_disk",self.disks(),tag)
        f2 = compute_fn_ft("particle_segment",self.segments(),tag)
        f += f2
        if self._dim == 3:
            f+= compute_fn_ft("particle_triangle",self.triangles(),tag)
        return -f

    def set_boundary_velocity(self, tag, v) :
        """Sets the velocity of a boundary to a given value.
        Keyword arguments:
        tag -- Name of the boundary
        v -- Velocity vector to be given to the boundary
        """
        self._lib.particleProblemGetTagId.restype = c_size_t
        tag = self._lib.particleProblemGetTagId(self._p, tag.encode())
        disks = self.disks()
        disks["v"][disks["tag"]==tag] = v
        segments = self.segments()
        segments["v"][segments["tag"]==tag] = v
        if self._dim == 3 :
            triangles = self.triangles()
            triangles["v"][triangles["tag"]==tag] = v

    def set_tangent_boundary_velocity(self, tag, vt):
        """ Sets the tangent velocity of the frictional boundary.
        Only in 2D
        Keyword arguments:
        tag -- Name of the boundary
        vt -- Velocity in the tangent direction
        """
        assert self._friction_enabled
        assert self._dim==2
        self._lib.particleProblemGetTagId.restype = c_size_t
        tag = self._lib.particleProblemGetTagId(self._p, tag.encode())
        disks = self.disks()
        segments = self.segments()
        disks["vt"][disks["tag"]==tag] = vt
        segments["vt"][segments["tag"]==tag] = vt

    def set_friction_coefficient(self, mu, mat0="default",mat1="default") :
        """ Sets the friction coefficient between two materials.

        Keyword arguments:
        mu -- Value of the friction coefficient
        mat0 -- First material
        mat1 -- Second material
        """
        assert self._friction_enabled
        self._lib.particleProblemSetFrictionCoefficient(self._p, c_double(mu), mat0.encode(),mat1.encode())

    def iterate(self, dt, forces,tol=1e-8,force_motion=0) :
        """Computes iteratively the set of velocities that respect the non-interpenetration constrain.
           Returns 1 if the computation converged, 0 otherwise.
        Keyword arguments:
        dt -- Numerical time step
        forces -- List of vectors containing the forces applied on the particles
        tol -- Optional argument defining the interpenetration tolerance to stop the NLGS iterations of the NSCD
        force_motion -- Optional argument allowing to move the grains if convergence has not been reached when set to 1
        """ 
        self._lib.particleProblemIterate.restype = c_int
        return self._lib.particleProblemIterate(self._p, c_double(np.max(self.r()) if self.r().size != 0 else tol), c_double(dt), c_double(tol), c_int(-1),c_int(force_motion),_np2c(forces))

    def get_contacts(self,contact_type) :
        """Gives the contact forces. Warning : during the resolution of the contacts, 
           the considered quantities are impulses, while forces are written and read.
        """
        ctype = {"particle_particle":0,"particle_disk":1,"particle_segment":2,"particle_triangle":3}[contact_type]
        n = self._lib.particleProblemContactN(self._p,c_int(ctype))
        basis = np.ndarray((n,self._dim*self._dim),dtype=np.float64,order="C")
        v = np.ndarray((n,self._dim),dtype=np.float64,order="C")
        o = np.ndarray((n,2),dtype=np.uint64,order="C")
        self._lib.particleProblemContact(self._p,c_int(ctype),c_void_p(o.ctypes.data),c_void_p(v.ctypes.data))
        self._lib.particleProblemContactBasis(self._p,c_int(ctype),c_void_p(basis.ctypes.data))
        basis = basis.reshape(n,self._dim, self._dim)
        return o,v,basis

    def computeStressTensor(self, nodes, radius):
        """Computes the stress tensor of the granular material
        Keyword arguments:
        nodes -- Array of nodes at which to compute the stress tensor
        r -- Radius within which the contact forces will be averaged 
        """
        n_nodes = len(nodes[:,0])
        s = np.ndarray((n_nodes,self._dim**2))
        self._lib.particleProblemComputeStressTensor(self._p,_np2c(nodes[:,:self._dim]),c_double(radius),c_int(n_nodes),_np2c(s))
        return s

    def write_vtk(self, odir, i, t) :
        """Writes output files for post-visualization.
        Keyword arguments:
        odir -- Directory in which to write the file
        i -- Number of the fiel to write
        t -- Time at which the simulation is 
        """
        v = self.velocity()
        omega = self.omega()
        x = self.position()
        material = self._get_idx("ParticleMaterial").reshape(-1,1)
        forced = self._get_idx("ForcedFlag").reshape(-1,1)
        if self._dim == 2 :
            v = np.insert(v,self._dim,0,axis=1)
            x = np.insert(x,self._dim,0,axis=1)
        data = [("Mass",self.mass()), ("Radius",self.r()),("Velocity",v),("Omega",omega),("Material",material),("ForcedFlag",forced),("Contacts",self.contact_forces())]
        nmat = self._lib.particleProblemNMaterial(self._p)
        self._lib.particleProblemGetMaterialTagName.restype = c_char_p
        tags = list([self._lib.particleProblemGetMaterialTagName(self._p,i) for i in range(nmat)])
        VTK.write(odir+"/particles",i,t,None,x,data,vtktype="vtp",field_data=[(b"MaterialNames",VTK.string_array_encode(tags))])

        disks = self.disks()
        segments = self.segments()
        triangles = self.triangles()
        x = np.vstack([disks["x"],segments["p"].reshape([-1,self._dim]),triangles["p"].reshape([-1,self._dim])])
        if self._dim == 2 :
            x = np.insert(x,self._dim,0,axis=1)
        connectivity = np.arange(0,x.shape[0],dtype=np.int32)
        types = np.repeat(np.array([1,3,5],dtype=np.int32),[disks.shape[0],segments.shape[0],triangles.shape[0]])
        offsets = np.cumsum(np.repeat([1,2,3],[disks.shape[0],segments.shape[0],triangles.shape[0]]),dtype=np.int32)
        tags = np.array(np.hstack([disks["tag"],segments["tag"],triangles["tag"]]))
        materials = np.array(np.hstack([disks["material"],segments["material"],triangles["material"]]))
        ntagname = self._lib.particleProblemNTag(self._p)
        self._lib.particleProblemGetTagName.restype = c_char_p
        tagnames = list([self._lib.particleProblemGetTagName(self._p,i) for i in range(ntagname)])
        VTK.write(odir+"/boundaries",i,t,(types,connectivity,offsets),x,cell_data=[("Tag",tags.reshape([-1,1])),("Material",materials.reshape([-1,1]))],field_data=[(b"TagNames",VTK.string_array_encode(tagnames))])

        periodicEntity = self.periodicEntity()
        periodicSegments = self.periodicSegments()
        periodicTriangles = self.periodicTriangles()
        periodicX = np.vstack([periodicSegments["p"].reshape([-1,self._dim]), periodicTriangles["p"].reshape([-1,self._dim])])
        if self._dim == 2 :
            periodicX = np.insert(periodicX,self._dim, 0, axis=1)
        periodicConnectivity = np.arange(0,periodicX.shape[0], dtype = np.int32)
        periodicTypes = np.repeat(np.array([3,5],dtype=np.int32),[periodicSegments.shape[0], periodicTriangles.shape[0]])
        periodicOffsets = np.cumsum(np.repeat([2,3],[periodicSegments.shape[0], periodicTriangles.shape[0]]),dtype=np.int32)
        periodicEntityIds = np.array(np.hstack([periodicSegments["entity_id"], periodicTriangles["entity_id"]]))
        entityTransformation = np.array(periodicEntity["periodic_transformation"])
        
        VTK.write(odir+"/periodicBoundaries", i, t, (periodicTypes, periodicConnectivity, periodicOffsets),
                    periodicX, cell_data=[("Entity_id", periodicEntityIds.reshape([-1,1]))], field_data=[(b"Entity_transformation", entityTransformation)])

        #Contacts
        self._lib.particleProblemContactN.restype = c_size_t
        fdata = []
        for name in ("particle_particle","particle_disk","particle_segment","particle_triangle") :
            o,v,basis = self.get_contacts(name)
            nameb = name.encode()
            fdata.append((nameb,v[:,[0]]))
            fdata.append((nameb+b"_t",v[:,[1]]))
            fdata.append((nameb+b"_dir_n",basis[:,0,:]))
            if self._dim == 3:
                fdata.append((nameb+b"_s",v[:,[2]]))
            fdata.append((nameb+b"_idx",o))
        x = np.array([[0.,0.,0.]])
        VTK.write(odir+"/contacts",i,t,None,x,field_data=fdata,vtktype="vtp")
        VTK.write_multipart(odir+"/particle_problem",["particles_%05d.vtp"%i,"boundaries_%05d.vtu"%i,"periodicBoundaries_%05d.vtu"%i,"contacts_%05d.vtp"%i],i,t)

    def read_vtk(self,dirname,i,contact_factor=1) :
        """Reads an existing output file to set the particle data.
        Keyword arguments:
        dirname -- Path to the directory of the file to read
        i -- Number of the file to read
        contact_factor -- Factor that determines how to take the read contacts into account
        """
        self._lib.particleProblemClearBoundaries(self._p)
        x,_,d,cdata,fdata = VTK.read(dirname+"/particles_%05d.vtp"%i)
        matnames =  VTK.string_array_decode(fdata["MaterialNames"])
        matmap = {}
        forced = d["ForcedFlag"] if ("ForcedFlag" in d) else np.zeros_like(d["Mass"]).astype(int)
        for j,n in enumerate(matnames) :
            matmap[j] = self._lib.particleProblemGetMaterialTagId(self._p,n)
        partmat =np.vectorize(matmap.get)(d["Material"])
        self._lib.particleProblemClearParticles(self._p)
        self._lib.particleProblemAddParticles(self._p,c_int(x.shape[0]),
                _np2c(x[:,:self._dim]), _np2c(d["Mass"]), _np2c(d["Radius"]), _np2c(d["Velocity"][:,:self._dim]),_np2c(d["Omega"]),_np2c(partmat,dtype=np.int32),_np2c(forced,dtype=np.int32),_np2c(d["Contacts"][:,:self._dim]*contact_factor))
       
        x,cells,d,cdata,fdata = VTK.read(dirname+"/boundaries_%05d.vtu"%i)
        tagnames =  VTK.string_array_decode(fdata["TagNames"])
        tagmap = {}
        for j,n in enumerate(tagnames) :
            tagmap[j] = self._lib.particleProblemGetTagId(self._p,n)
        offsets = np.hstack([[0],cells["offsets"]])
        el = cells["connectivity"]
        tags = np.vectorize(tagmap.get)(cdata["Tag"])
        materials = cdata["Material"]
        for idx in np.where(cells["types"] == 1)[0] :
            x0 = x[el[offsets[idx]],:self._dim]
            self._lib.particleProblemAddBoundaryDiskTagId(self._p, self._coord_type(*x0), c_double(0.), c_int(tags[idx,0]), c_int(materials[idx,0]))
        for idx in np.where(cells["types"] == 3)[0] :
            x0 = x[el[offsets[idx]],:self._dim]
            x1 = x[el[offsets[idx]+1],:self._dim]
            self._lib.particleProblemAddBoundarySegmentTagId(self._p, self._coord_type(*x0), self._coord_type(*x1), c_int(tags[idx,0]), c_int(materials[idx,0]))
        for idx in np.where(cells["types"] == 5)[0] :
            x0 = x[el[offsets[idx]],:self._dim]
            x1 = x[el[offsets[idx]+1],:self._dim]
            x2 = x[el[offsets[idx]+2],:self._dim]
            self._lib.particleProblemAddBoundaryTriangleTagId(self._p, self._coord_type(*x0), self._coord_type(*x1), self._coord_type(*x2), c_int(tags[idx,0]), c_int(materials[idx,0]))
        
        periodicX, periodicCells,_, periodicCellsData, periodicFieldsData = VTK.read(dirname+"/periodicBoundaries_%05d.vtu"%i)
        entityTransformation = periodicFieldsData["Entity_transformation"]
        entity_ids = periodicCellsData["Entity_id"].ravel()
        periodicOffsets = np.hstack([[0], periodicCells["offsets"]])
        periodicEl = periodicCells["connectivity"]
        # add entity
        for entity_id in range(np.shape(entityTransformation)[0]):
            trans = tuple(entityTransformation[entity_id])
            self.add_boundary_periodic_entity(entity_id, self._dim-1, trans)
        # add periodic segment
        for idx in np.where(periodicCells["types"] == 3)[0]:
            pidx = periodicEl[periodicOffsets[idx]]
            entity_id = entity_ids[pidx//2]
            x0 = periodicX[pidx,:self._dim]
            x1 = periodicX[pidx+1,:self._dim]
            self.add_boundary_periodic_segment(tuple(x0), tuple(x1),entity_id)
        # add periodic triangles
        for idx in np.where(periodicCells["types"] == 5)[0]:
            pidx = periodicEl[periodicOffsets[idx]]
            entity_id = entity_ids[pidx//3]
            x0 = periodicX[pidx,:self._dim]
            x1 = periodicX[pidx+1,:self._dim]
            x2 = periodicX[pidx+2,:self._dim]
            self.add_boundary_periodic_triangle(tuple(x0), tuple(x1), tuple(x2), entity_id)

        _,_,_,_,fdata = VTK.read(dirname+"/contacts_%05d.vtp"%i)
        ks = ("particle_particle","particle_disk","particle_segment","particle_triangle")
        v = []
        basis = []
        v.append(np.vstack([fdata[k] for k in ks]))
        v.append(np.vstack([fdata[k+"_t"] for k in ks]))
        basis.append(np.vstack([fdata[k+"_dir_n"] for k in ks]))
        if self._dim == 2:
            basis.append(np.vstack([fdata[k+"_dir_n"] for k in ks])[:,[1,0]]*np.array([-1, 1]))
        else:
            dirt = np.vstack([fdata[k+"_dir_n"] for k in ks])[:,[2,0,1]]*np.array([-1, 1, -1]) - np.vstack([fdata[k+"_dir_n"] for k in ks])*np.einsum("ij,ij->i",np.vstack([fdata[k+"_dir_n"] for k in ks]),np.vstack([fdata[k+"_dir_n"] for k in ks])[:,[2,0,1]]*np.array([-1, 1, -1]))[:,np.newaxis]
            nnorm = np.linalg.norm(dirt,axis=1)
            nnorm[nnorm==0] = 1
            basis.append(dirt/nnorm[:,np.newaxis])
            basis.append(np.cross(np.vstack([fdata[k+"_dir_n"] for k in ks]),dirt/nnorm[:,np.newaxis]))
            v.append(np.vstack([fdata[k+"_s"] for k in ks]))
        basis = np.column_stack(basis)
        v = np.column_stack(v)*contact_factor
        o = np.vstack([fdata[k+"_idx"] for k in ks])
        t = np.repeat([0,1,2,3],[fdata[k].shape[0] for k in ks])
        self._lib.particleProblemSetContacts(self._p,c_int(t.shape[0]),_np2c(o,np.uint64),_np2c(v),_np2c(basis),_np2c(t,np.int32))

    def add_boundary_disk(self, x0, r, tag, material="default") :
        """Adds a boundary disk.

        Keyword arguments:
        x0 -- Tuple of the coordinates of the centre
        r -- Disk radius
        tag -- Disk tag
        material -- Disk material
        """
        self._lib.particleProblemAddBoundaryDisk.restype = c_size_t
        return self._lib.particleProblemAddBoundaryDisk(self._p, self._coord_type(*x0), c_double(r), tag.encode(),material.encode())

    def add_boundary_periodic_entity(self, etag, edim, transform):
        """Adds a periodic entity.

        Keyword arguments:
        etag -- tag of the entity
        edim -- dimension of the entity
        transform -- tuple of the transformation to applied to the periodic entity
        """
        self._lib.particleProblemAddBoundaryPeriodicEntity.restype = c_size_t
        return self._lib.particleProblemAddBoundaryPeriodicEntity(self._p, c_int(etag), c_int(edim), self._coord_type(*transform))

    def add_boundary_periodic_segment(self, x0, x1, etag) :
        """Adds a boundary periodic segment.

        Keyword arguments:
        x0 -- Tuple of the coordinates of the first endpoint
        x1 -- Tuple of the coordinates of the second endpoint
        tag -- entity tag
        """
        self._lib.particleProblemAddBoundaryPeriodicSegment.restype = c_size_t
        return self._lib.particleProblemAddBoundaryPeriodicSegment(self._p, self._coord_type(*x0), self._coord_type(*x1), c_int(etag))

    def add_boundary_segment(self, x0, x1, tag, material="default") :
        """Adds a boundary segment.

        Keyword arguments:
        x0 -- Tuple of the coordinates of the first endpoint
        x1 -- Tuple of the coordinates of the second endpoint
        tag -- Segment tag
        material -- Segment material
        """
        self._lib.particleProblemAddBoundarySegment.restype = c_size_t
        return self._lib.particleProblemAddBoundarySegment(self._p, self._coord_type(*x0), self._coord_type(*x1), tag.encode(),material.encode())

    def add_boundary_triangle(self, x0, x1, x2, tag, material="default") :
        """Adds a boundary triangle.

        Keyword arguments:
        x0 -- Tuple of the coordinates of the first summit 
        x1 -- Tuple of the coordinates of the second summit 
        x2 -- Tuple of the coordinates of the third summit 
        tag -- Triangle tag
        material -- Triangle material
        """
        if self._dim != 3 :
            raise NameError("Triangle boundaries only available in 3D")
        self._lib.particleProblemAddBoundaryTriangle.restype = c_size_t
        return self._lib.particleProblemAddBoundaryTriangle(self._p, self._coord_type(*x0), self._coord_type(*x1),  self._coord_type(*x2), tag.encode(),material.encode())

    def add_boundary_periodic_triangle(self, x0, x1, x2, etag):
        """Adds a boundary periodic triangle.

        Keyword arguments:
        x0 -- Tuple of the coordinates of the first summit 
        x1 -- Tuple of the coordinates of the second summit 
        x2 -- Tuple of the coordinates of the third summit 
        etag -- tag of the periodic entity 
        """
        if self._dim != 3 :
            raise NameError("Triangle boundaries only available in 3D")
        self._lib.particleProblemAddBoundaryPeriodicTriangle.restype = c_size_t
        return self._lib.particleProblemAddBoundaryPeriodicTriangle(self._p, self._coord_type(*x0), self._coord_type(*x1),  self._coord_type(*x2), c_int(etag))

    def add_particle(self, x, r, m, tag="default",forced = 0):
        """Adds a particle in the particle problem.

        Keyword arguments:
        x -- Tuple to set the centre particle position
        r -- Particle radius
        m -- Particle mass
        tag -- Particle material
        forced -- Flag indicating whether the particle is forced or not
        """
        self._lib.particleProblemAddParticle(self._p, self._coord_type(*x), c_double(r), c_double(m), tag.encode(), c_int(forced))

    def add_particles(self, x, r, m, v=None, omega=None, tag="default", forced=None, contact_forces=None):
        """Adds particles in the particle problem.
        Keyword arguments:
        x -- Array with the particles's centers position
        r -- Array with the particles's radii
        m -- Array with the particles's masses
        v -- Array with the particles's velocities
        omega -- Array with the particles's angular velocities
        tag -- Particle material
        forced -- Array of flags indicating whether the particles are forced or not
        contact_forces -- Array of contact forces between the particles
        """
        n_particles = len(m)
        tags = np.ones(n_particles) * self.get_tag_id(tag)
        if omega is None :
         omega = np.zeros((1 if self._dim == 2 else 3)*n_particles)
        if v is None :
         v = np.zeros(self._dim*n_particles)
        if forced is None :
         forced = np.zeros(n_particles)
        if contact_forces is None :
         contact_forces = np.zeros(self._dim*n_particles)
        self._lib.particleProblemAddParticles(self._p, c_int(n_particles), _np2c(x), _np2c(m), _np2c(r),_np2c(v), _np2c(omega), _np2c(tags,dtype=np.int32), _np2c(forced,dtype=np.int32), _np2c(contact_forces))

    def set_use_queue(self, use_queue=1):
      """Enables the use of the queue if 1 and disables it if 0."""
      self._lib.particleProblemSetUseQueue(self._p, c_int(use_queue))

    def get_tagnames(self):
      """Returns the names of the boundaries """
      self._lib.particleProblemGetTagName.restype = c_char_p
      ntagname = self._lib.particleProblemNTag(self._p)
      tagnames = list([self._lib.particleProblemGetTagName(self._p,i) for i in range(ntagname)])
      return tagnames

    def clear_boundaries(self):
      """Removes the boundaries."""
      self._lib.particleProblemClearBoundaries(self._p)
    def _save_contacts(self):
      """Saves the contacts from the current time step."""
      self._lib.particleProblemSaveContacts(self._p)

    def _restore_contacts(self):
      """Restores the saved contacts from the previous time step."""
      self._lib.particleProblemRestoreContacts(self._p)

    def remove_particles_flag(self,flag) :
      """Removes particles based on given flag."""
      if flag.shape != (self.n_particles(),) :
          raise NameError("size of flag array should be the number of particles")
      self._lib.particleProblemRemoveParticles(self._p, _np2c(flag,np.int32))


    def load_msh_boundaries(self, filename, tags=None, shift=None,material="default") :
        """Loads the numerical domain and set the physical boundaries the particles cannot go through.
        
        Keyword arguments:
        filename -- Name of the msh file
        tags -- Tags of physical boundary defined in the msh file
        shift -- Optional argument to shift the numerical domain
        material -- Material of the boundary
        """
        if not os.path.isfile(filename):
          print("Error : no such file as " + filename)
          exit(1)
        if shift is None :
            shift = [0]*self._dim
        shift = np.array(shift)
        gmsh.model.add("tmp")
        gmsh.open(filename)
        gmsh.model.mesh.renumberNodes()
        addv = set()
        adds = set()
        periodic_entities = set()
        _, x, _ = gmsh.model.mesh.getNodes()
        x = x.reshape([-1,3])[:,:self._dim]

        def get_entity_name(edim, etag) :
            for tag in  gmsh.model.getPhysicalGroupsForEntity(edim, etag):
                name = gmsh.model.getPhysicalName(edim,tag)
                if name is not None :
                    return name
            return "none"

        def add_disk(t, stag) :
            if t in addv : return
            addv.add(t)
            self.add_boundary_disk(x[t]+shift, 0., stag, material)

        def add_segment(t0, t1, stag) :
            key = (min(t0,t1),max(t0,t1))
            if key in adds : return
            adds.add(key)
            self.add_boundary_segment(x[t0]+shift, x[t1]+shift,
                                      stag, material)

        def add_triangle(t0, t1, t2, stag):
            self.add_boundary_triangle(x[t0]+shift, x[t1]+shift,x[t2]+shift,
                                        stag, material)

        for dim, tag in gmsh.model.getEntities(self._dim-1) :
            ptag, cnodes, pnodes, _ = gmsh.model.mesh.getPeriodicNodes(dim, tag)
            if ptag == tag or len(cnodes) == 0: continue
            periodic_entities.add((dim,tag))
            periodic_entities.add((dim,ptag))
            trans = x[(pnodes-1)[0]] - x[(cnodes-1)[0]]
            self.add_boundary_periodic_entity(tag,dim,trans)
            self.add_boundary_periodic_entity(ptag,dim,-trans)
            pmap = dict((int(i)-1,int(j)-1) for i,j in zip (cnodes,pnodes))
            for etype, _, enodes in zip(*gmsh.model.mesh.getElements(dim,tag)):
                if dim == 1 :
                    if etype != 1 : continue
                    for l in (enodes-1).reshape([-1,2]):
                        self.add_boundary_periodic_segment(
                                x[l[0]]+shift, x[l[1]]+shift, tag)
                        self.add_boundary_periodic_segment(
                                x[pmap[l[0]]]+shift, x[pmap[l[1]]]+shift, ptag)
                else :
                    if etype != 2 : continue
                    for l in (enodes-1).reshape([-1,3]):
                        self.add_boundary_periodic_triangle(
                                x[l[0]]+shift, x[l[1]]+shift,
                                x[l[2]]+shift, tag)
                        self.add_boundary_periodic_triangle(
                                x[pmap[l[0]]]+shift, x[pmap[l[1]]]+shift,
                                x[pmap[l[2]]]+shift, ptag)
        for dim, tag in gmsh.model.getEntities(0) :
            stag = get_entity_name(dim,tag)
            if (dim,tag) in periodic_entities : continue
            if not (tags is None or stag in tags) : continue
            for etype, _, enodes in zip(*gmsh.model.mesh.getElements(dim,tag)):
                if etype != 15 : continue
                for t in enodes-1 :
                    add_disk(t, stag)

        for dim, tag in gmsh.model.getEntities(1) :
            stag = get_entity_name(dim,tag)
            if (dim,tag) in periodic_entities : continue
            if not (tags is None or stag in tags) : continue
            for etype, _, enodes in zip(*gmsh.model.mesh.getElements(dim,tag)):
                if etype != 1 : continue
                for t in enodes-1 :
                    add_disk(t, stag)
                for l in (enodes-1).reshape([-1,2]):
                    add_segment(l[0], l[1], stag)

        if self._dim == 3 :
            for dim, tag in gmsh.model.getEntities(2) :
                stag = get_entity_name(dim,tag)
                if (dim,tag) in periodic_entities : continue
                if not (tags is None or stag in tags) : continue
                for etype, _, enodes in zip(*gmsh.model.mesh.getElements(dim,tag)):
                    if etype != 2 : continue
                    for t in enodes-1 :
                        add_disk(t, stag)
                    for v0,v1,v2 in (enodes-1).reshape([-1,3]):
                        add_segment(v0, v1, stag)
                        add_segment(v1, v2, stag)
                        add_segment(v2, v0, stag)
                        add_triangle(v0, v1, v2, stag)

        gmsh.model.remove()
            
    def dim(self) :
        """Returns the dimension of the particle problem"""
        return self._dim
