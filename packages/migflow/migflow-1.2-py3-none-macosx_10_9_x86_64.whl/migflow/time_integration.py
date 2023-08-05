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
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

def _advance_particles(particles, f, dt, min_nsub,contact_tol,max_nsub=None,after_sub_iter=None,n_divide=None) :
    """Contact solver for the grains

    Keyword arguments:
    particles -- particles structure
    f -- external forces on particles
    dt -- time step
    min_nsub -- minimal nsub for the particles iterations
    contact_tol -- tolerance for the contact solver
    after_sub_iter -- callback to execute once a sub iteration has been made
    """
    # Compute free velocities of the grains
    v = particles.velocity()
    if f is None:
        f = np.zeros_like(v)
    # Estimation of the solid sub-time steps
    if particles.r() is not None and particles.r().size != 0:
        vn = v + f*dt / particles.mass()
        vmax = np.max(np.linalg.norm(vn,axis=1))
        nsub = max(min_nsub, int(np.ceil((vmax * dt * 8)/min(particles.r()))))
    else:
        nsub = 1
        vmax = 0
    if max_nsub is None:
      max_nsub = min_nsub*8
    print("NSUB", nsub,"VMAX",vmax, "VMAX * dt", vmax * dt, "r", min(particles.r()) if (particles.r() is not None and particles.r().size !=0) else 0 )
    if n_divide is None:
      n_divide = nsub
    else:
      n_divide *= nsub
    #If time step was split too many times, ignore the convergence and move the grains
    if min_nsub > max_nsub:
      for i in range(nsub) :
        particles.iterate(dt/nsub, f, tol=contact_tol,force_motion=1)
        if after_sub_iter :
            after_sub_iter(n_divide)
      return
    # For each sub-time step solve contacts (do NLGS iterations) and move the grains 
    for i in range(nsub) :
        if not particles.iterate(dt/nsub, f, tol=contact_tol):
          print("Splitting time-step")
          _advance_particles(particles,f,dt/nsub,min_nsub*2,contact_tol/2,max_nsub/nsub,after_sub_iter=after_sub_iter,n_divide=n_divide)
          print("Convergence reached for subinvervals")
        else :
            if after_sub_iter :
                after_sub_iter(n_divide)

      
def predictor_corrector_iterate(fluid, particles, dt, min_nsub=1, contact_tol=1e-8, external_particles_forces=None, alpha=0.5,after_sub_iter=None,max_nsub=None) :  
    """Predictor-corrector scheme to solve fluid and grains.

    Keyword arguments:
    fluid -- fluid structure
    particles -- particles structure
    dt -- time step
    min_nsub -- minimal nsub for the particles iterations
    contact_tol -- tolerance for the contact solver
    external_particles_forces -- external forces applied on the particles
    alpha -- parametre of the predictor-corrector scheme [alpha*f(n)+(1-alpha)*f(n+1)]
    after_sub_iter -- callback to execute once a sub iteration has been made
    max_split -- maximum number of times the time step can be further split if conergence is not reached
    """
    particles.save_state()
    if external_particles_forces is None:
        external_particles_forces = np.zeros_like(particles.velocity())
    # Copy the fluid solution of the previous time step before computing the prediction 
    sf0 = np.copy(fluid.solution())
    # Copy the solid solution of the previous time step before computing the prediction
    x0 = np.copy(particles.position())
    cp0 = np.copy(particles.contact_forces())
    seg0 = np.copy(particles.segments())
    disk0 = np.copy(particles.disks())
    if particles.dim() == 3 :
        tri0 = np.copy(particles.triangles())
    # Predictor
    #
    # Compute the fluid solution and keep a copy of this solution and the forces applied by the fluid on the grains
    fluid.implicit_euler(dt)
    sf1 = np.copy(fluid.solution())
    f0 = np.copy(fluid.compute_node_force(dt))+external_particles_forces
    _advance_particles(particles,f0,dt,min_nsub,contact_tol,max_nsub=max_nsub)

    # Keep same contact forces and positions while giving to the fluid the predicted solid velocities to compute the correction
    fluid.particle_velocity()[:] = particles.velocity()

    # Corrector
    #
    # Compute the fluid solution from the previous time-step one using the predicted solid velocities in the fluid-grain interaction force
    fluid.solution()[:,:] = sf0
    fluid.implicit_euler(dt)
    # Fluid solution is a weighted average of the predicted one and the corrected one.
    # The alpha parametre is the weight
    fluid.solution()[:,:] = (alpha*fluid.solution()+(1-alpha)*sf1)
    f1 = np.copy(fluid.compute_node_force(dt))+external_particles_forces
    # For two fluids flows, advance the concentration field with the fluid velocity.
    # The number of sub-time steps for the advection is automatically computed.
    if fluid.n_fluids() == 2 :
        fluid.advance_concentration(dt)
    # Reset solid velocities
    particles.restore_state()
    _advance_particles(particles,(alpha*f0+(1-alpha)*f1),dt,min_nsub,contact_tol,after_sub_iter=after_sub_iter,max_nsub=max_nsub)
    # Give to the fluid the solid information
    fluid.move_particles(particles.position(), particles.velocity(), particles.contact_forces())


def iterate(fluid, particles, dt, min_nsub=1, contact_tol=1e-8, external_particles_forces=None, fixed_grains=False, after_sub_iter=None,max_nsub=None) :  
    """Migflow solver: the solver type depends on the fluid and particles given as arguments.

    Keyword arguments:
    fluid -- fluid structure
    particles -- particles structure
    dt -- time step
    min_nsub -- minimal nsub for the particles iterations
    contact_tol -- tolerance for the contact solver
    external_particles_forces -- vector of external forces applied on the particles
    fixed_grains -- boolean variable specifying if the grains are fixed in the fluid
    after_sub_iter -- callback to execute once a sub iteration has been made
    max_split -- maximum number of times the time step can be further split if conergence is not reached

    Raises:
        ValueError -- fluid and particles cannot be both None
        ValueError -- external_particles_forces must have shape (number of particles,dimension)
    """
    if particles is None and fluid is None:
        raise ValueError("fluid and particles are both None: not possible to iterate!")
    if particles is not None and external_particles_forces is not None:
        if external_particles_forces.shape!=(particles.n_particles(),particles.dim()):
            raise ValueError("external_particles_forces must have shape (number of particles,dimension!")
    if (particles is None or particles.r() is None or particles.r().size == 0) and fluid is not None:
        fluid.implicit_euler(dt)
        # For two fluids flows, advance the concentration field with the fluid velocity.
        # The number of sub-time steps for the advection is automatically computed.
        if fluid.n_fluids() == 2 :
            fluid.advance_concentration(dt)
    if particles is not None and fluid is None:
        _advance_particles(particles,external_particles_forces,dt,min_nsub,contact_tol,after_sub_iter=after_sub_iter,max_nsub=max_nsub)
    if fluid is not None and particles is not None and particles.r() is not None and particles.r().size !=0:
        if fixed_grains:
            fluid.implicit_euler(dt)
            fluid.move_particles(particles.position(), particles.velocity(),-fluid.compute_node_force(dt))
        else:
            predictor_corrector_iterate(fluid,particles,dt,min_nsub,contact_tol,external_particles_forces,after_sub_iter=after_sub_iter,max_nsub=max_nsub)


class FreeSurface():
    def __init__(self, fluid, tagFS, tagOFS, isCentered=True, correctVelocity=False, origin = (0,0)):
        if fluid._dim != 2:
            print("Free Surface not available for this dimension !")
        self.fluid = fluid
        self.tagFS = tagFS
        self.tafOFS = tagOFS
        self.fs_nodes = self.get_nodes(tagFS)
        self.ofs_nodes = self.get_nodes(tagOFS)
        self.scheme = self.compute_h_centered if isCentered else self.compute_h_decentered
        self.correctVelocity = correctVelocity
        self.nodes_struct = self.get_nodes_struct(self.fs_nodes, self.ofs_nodes, origin[0], origin[1])
        self.alpha = self.get_alpha()

    def iterate(self,dt,vbox = [0,0]):
        dim = self.fluid._dim
        vbox = np.array(vbox, dtype=np.float)
        newx = np.copy(self.fluid.coordinates())
        if self.correctVelocity :
            self.corr_un(vbox)
        self.scheme(dt,newx)
        newx[self.ofs_nodes,:dim] += vbox[None,:dim]*dt
        self.update_inside_points(newx)
        self.fluid.mesh_velocity()[:,:dim] = (newx[:,:dim] - self.fluid.coordinates()[:,:dim])*self.fluid.porosity()[:]
        self.fluid.coordinates()[:] = newx[:]


    def get_nodes_struct(self, fs_nodes, ofs_nodes, Ox, Oy):
        eps = 1e-4
        x = self.fluid.coordinates()[:,0]
        y = self.fluid.coordinates()[:,1]
        nodes = np.arange(np.size(x))
        nodes = np.setdiff1d(nodes, fs_nodes)
        nodes = np.setdiff1d(nodes, ofs_nodes)
        min_node = fs_nodes[0] if x[fs_nodes[0]] < x[ofs_nodes[0]] else ofs_nodes[0]
        nodes_to_delete = [node for node in nodes if x[node] < x[min_node]]
        nodes = np.setdiff1d(nodes,nodes_to_delete)
        nodes = sorted(nodes, key = lambda x: self.fluid.coordinates()[x,0])
        L = []
        for node in nodes:
            if y[node] > Oy-eps and x[node] > Ox-eps:
                node_struct = dict(node_index = node)
                n = np.size(fs_nodes)
                for i in range(0,n):
                    current_top_node = fs_nodes[i]
                    next_top_node = fs_nodes[i+1]
                    if x[node] >= x[current_top_node]-eps and x[node] < x[next_top_node]+eps:
                        node_struct["upper_nodes"] = [fs_nodes[i], fs_nodes[i+1]]
                        break
                m = np.size(ofs_nodes)
                for i in range(0,m):
                    current_bottom_node = ofs_nodes[i]
                    next_bottom_node = ofs_nodes[i+1]
                    if x[node] >= x[current_bottom_node] - eps and x[node] < x[next_bottom_node] + eps:
                        node_struct["lower_nodes"] = [ofs_nodes[i], ofs_nodes[i+1]]
                        break
                L.append(node_struct)
        return L
    
    def get_nodes(self, tag):
        nodes = (self.fluid._mesh_boundaries())[tag.encode()]
        nodes = np.unique(nodes.reshape(np.size(nodes)))
        nodes = sorted(nodes, key=lambda node: self.fluid.coordinates()[node,0])
        return nodes

    def get_alpha(self):
        fluid = self.fluid
        nodes_struct = self.nodes_struct
        x = fluid.coordinates()[:,0]
        h_old = fluid.coordinates()[:,1]
        alpha = np.zeros_like(x)
        for node_struct in nodes_struct:
            node = node_struct.get("node_index")
            upper_nodes = node_struct.get("upper_nodes")
            lower_nodes = node_struct.get("lower_nodes")

            upper_dx = x[upper_nodes[1]] - x[upper_nodes[0]]
            lower_dx = x[lower_nodes[1]] - x[lower_nodes[0]]

            upper_wRight = (x[node] - x[upper_nodes[0]])/upper_dx
            upper_wLeft  = 1 - upper_wRight
            lower_wRight = (x[node] - x[lower_nodes[0]])/lower_dx
            lower_wLeft  = 1 - lower_wRight

            H_old = upper_wLeft*h_old[upper_nodes[0]] + upper_wRight*h_old[upper_nodes[1]]
            O_old = lower_wLeft*h_old[lower_nodes[0]] + lower_wRight*h_old[lower_nodes[1]]

            alpha[node] = (h_old[node] - O_old)/(H_old - O_old)
        return alpha

    def update_inside_points(self, newx):
        x, h = newx[:,0], newx[:,1]
        h_old = self.fluid.coordinates()[:,1]
        for node_struct in self.nodes_struct:
            node = node_struct.get("node_index")
            upper_nodes = node_struct.get("upper_nodes")
            lower_nodes = node_struct.get("lower_nodes")

            upper_dx = x[upper_nodes[1]] - x[upper_nodes[0]]
            lower_dx = x[lower_nodes[1]] - x[lower_nodes[0]]
            upper_wRight = (x[node] - x[upper_nodes[0]])/upper_dx
            upper_wLeft  = 1 - upper_wRight
            lower_wRight = (x[node] - x[lower_nodes[0]])/lower_dx
            lower_wLeft  = 1 - lower_wRight
            # H_old = upper_wLeft*h_old[upper_nodes[0]] + upper_wRight*h_old[upper_nodes[1]]
            # O_old = lower_wLeft*h_old[lower_nodes[0]] + lower_wRight*h_old[lower_nodes[1]]
            H_new = upper_wLeft*h[upper_nodes[0]] + upper_wRight*h[upper_nodes[1]]
            O_new = lower_wLeft*h[lower_nodes[0]] + lower_wRight*h[lower_nodes[1]]

            newx[node,1] = (self.alpha)[node]*(H_new - O_new) +  O_new
    
    def compute_h_centered(self,dt,newx):
        nodes = self.fs_nodes
        n = len(nodes)-1
        enodes = np.column_stack([np.arange(0,n),np.arange(1,n+1)])
        x = self.fluid.coordinates()[nodes,0]
        y = self.fluid.coordinates()[nodes,1]
        u = self.fluid.solution()[nodes,:2]/self.fluid.porosity()[:]
        l = (x[1:]-x[:-1])
        J = l/2
        #nu = 1e-5
        dphidx = np.column_stack([-1/l,1/l])
        xi = np.array([-1/3,1/3])
        phi = np.column_stack([(1-xi)/2,(1+xi)/2])
        qw = np.array([1,1])
        yqp = y[enodes]@phi
        uqp = u[enodes,0]@phi
        vqp = u[enodes,1]@phi
        dudx = np.sum(u[enodes,0]*dphidx,axis=1)
        dydx = np.sum(y[enodes]*dphidx,axis=1)
        # rhsqp : element, test function, qp
        rhsqp = J[:,None,None]*qw[None,None,:]*(
                vqp[:,None,:]*phi[None,:,:]
                - uqp[:,None,:]*phi[None,:,:]*dydx[:,None,None]
                #+ nu*dphidx[:,:,None]*dudx[:,None,None]]
                )
        rhslocal = np.sum(rhsqp,axis=2)
        rhs = np.zeros((n+1))
        np.add.at(rhs,enodes.flat,rhslocal.flat)
        massparent = np.array([[2/3,1/3],[1/3,2/3]])
        masslocal = J[:,None,None]*massparent[None,:,:]
        rows = np.repeat(enodes[:,:,None],2,axis=2)
        cols = np.repeat(enodes[:,None,:],2,axis=1)
        massglobal = coo_matrix((masslocal.flat,(rows.flat,cols.flat))).tocsr()
        dhdt = spsolve(massglobal,rhs)
        newx[nodes,1] += dhdt*dt

    def compute_h_decentered(self,dt,newx):
        nodes = self.fs_nodes
        x = self.fluid.coordinates()[nodes,0]
        y = self.fluid.coordinates()[nodes,1]
        u = self.fluid.solution()[nodes,:2]/self.fluid.porosity()[nodes]
        dx = x[1:] - x[:-1]
        dhdx = (y[1:]- y[:-1])/dx
        ux = (u[1:,0] + u[:-1,0])/2
        uy = (u[1:,1] + u[:-1,1])/2
        rhs = uy - ux*dhdx
        newx[nodes[1:],1] += rhs*dt

    def compute_lapl_fs(self,nodes):
        n = len(nodes)-1
        enodes = np.column_stack([np.arange(0,n), np.arange(1,n+1)])
        x = self.fluid.coordinates()[nodes,0]
        h = self.fluid.coordinates()[nodes,1]
        l = (x[1:] - x[:-1])
        J = l/2
        dphidx = np.column_stack([-1/l,1/l])
        xi = np.array([-1/3,1/3])
        phi = np.column_stack([(1-xi)/2, (1+xi)/2])
        qw = np.array([1,1])
        dhqp = np.sum(h[enodes]*dphidx,axis=1)
        rhsqp = -J[:,None,None]*qw[None,None,:]*(dphidx[:,:,None]*dhqp[:,None,None])
        rhslocal= np.sum(rhsqp,axis=2)
        rhs = np.zeros((n+1))
        np.add.at(rhs,enodes.flat,rhslocal.flat)
        massparent = np.array([[2/3,1/3],[1/3,2/3]])
        masslocal = J[:,None,None]*massparent[None,:,:]
        rows = np.repeat(enodes[:,:,None],2,axis=2)
        cols = np.repeat(enodes[:,None,:],2,axis=1)
        massglobal= coo_matrix((masslocal.flat, (rows.flat, cols.flat))).tocsr()
        ddhdx = spsolve(massglobal,rhs)
        return ddhdx

    def compute_integral_un(self):
        bnd = self.fluid._mesh_boundaries()[(self.tagFS).encode()]
        x = self.fluid.coordinates()[bnd]
        dx = x[:,1,:]-x[:,0,:]
        l = np.linalg.norm(dx,axis=1)
        n = np.column_stack([dx[:,1],-dx[:,0]])/l[:,None]
        u = np.mean(self.fluid.solution()[bnd,:2],axis=1)
        un = u[:,0]*n[:,0]+u[:,1]*n[:,1]
        return np.sum(un*l)

    def corr_un(self, vbox):
        integral_un = self.compute_integral_un()
        print(f"Integral un before correction: {integral_un - vbox[-1]}")
        self.fluid.solution()[self.fs_nodes,1] += (vbox[-1]-integral_un)
