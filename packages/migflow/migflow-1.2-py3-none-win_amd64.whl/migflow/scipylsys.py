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
import scipy.sparse
import scipy.sparse.linalg

class LinearSystem :
    _initialized = False
    def __init__(self, elements, n_fields,options) :
        localsize = n_fields*elements.shape[1]
        self.el = elements
        idx = (elements[:,:,None]*n_fields+np.arange(n_fields)[None,None,:]).reshape([-1,localsize])
        self.rows = np.repeat(idx[:,:,None],localsize,axis=2)
        self.rows = self.rows.reshape([-1])
        self.cols = np.repeat(idx[:,None,:],localsize,axis=1)
        self.cols = self.cols.reshape([-1])
        self.idx = (elements[:,None,:]*n_fields+np.arange(n_fields)[None,:,None]).reshape([-1])
        self.localsize = localsize
        nnodes = np.max(elements)+1
        self.globalsize = nnodes*n_fields;

    def local_to_global(self,localv,localm,rhs):
        np.add.at(rhs.reshape([-1]),self.idx,localv)
        coo = scipy.sparse.coo_matrix((localm.reshape([-1]),(self.rows,self.cols)))
        self.matrix = coo.tocsc()

    def solve(self,rhs) :
        return scipy.sparse.linalg.splu(self.matrix).solve(rhs.reshape([-1])).reshape(rhs.shape)

