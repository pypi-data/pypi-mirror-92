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
import petsc4py
petsc4py.init()
from petsc4py import PETSc
import numpy as np

class LinearSystem :
    def __init__(self, elements, n_fields, options) :
        nnodes = np.max(elements)+1
        nn = elements.shape[1]
        pairs = np.ndarray((elements.shape[0],nn*(nn-1)),dtype=([('i0',np.int32),('i1',np.int32)]))
        pairs['i0'] = elements[:,np.repeat(range(nn),nn-1)]
        idx = np.hstack([[i for i in range(nn) if i!=j] for j in range(nn)]) 
        pairs['i1'] = elements[:,idx]
        pairs = np.unique(pairs)
        nnz = (np.bincount(pairs["i0"])+1).astype(np.int32)
        PETSc.Options().prefixPush("fluid_")
        PETSc.Options().insertString(options)
        PETSc.Options().prefixPop()
        self.mat = PETSc.Mat().createBAIJ(nnodes*n_fields,n_fields,nnz)
        self.ksp = PETSc.KSP().create()
        self.ksp.setOptionsPrefix(b"fluid_")
        self.ksp.setFromOptions()
        self.mat.zeroEntries()
        ###
        self.localsize = elements.shape[1]*n_fields
        self.elements = elements
        self.idx = (self.elements[:,None,:]*n_fields+np.arange(n_fields)[None,:,None]).reshape([-1])
        self.globalsize = nnodes*n_fields;

    def local_to_global(self,localv,localm,rhs):
        self.mat.zeroEntries()
        np.add.at(rhs.reshape([-1]),self.idx,localv)
        for e,m in zip(self.elements,localm.reshape([-1,self.localsize**2])) :
            self.mat.setValuesBlocked(e,e,m,PETSc.InsertMode.ADD)
        self.mat.assemble()

    def solve(self,rhs) :
        x = np.ndarray(rhs.shape)
        prhs = PETSc.Vec().createWithArray(rhs.reshape([-1]))
        px = PETSc.Vec().createWithArray(x.reshape([-1]))
        self.ksp.setOperators(self.mat)
        self.ksp.solve(prhs,px)
        return x
