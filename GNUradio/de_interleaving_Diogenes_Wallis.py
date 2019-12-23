#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2019 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr

class de_interleaving_Diogenes_Wallis(gr.sync_block):
    """
    docstring for block de-interleaving_Diogenes_Wallis
    """
    def __init__(self, k):
        gr.sync_block.__init__(self,
            name="de_interleaving_Diogenes_Wallis",
            in_sig=[(numpy.float32,7)],
            out_sig=[(numpy.float32,7)])
	

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
	
	aux = numpy.zeros((1,28))
	for i in range(int(len(in0)/28)):
		for j in range(4):
			aux[0][0+7*j] = in0[4*i+j,0]
			aux[0][1+7*j] = in0[4*i+j,1]
			aux[0][2+7*j] = in0[4*i+j,2]
			aux[0][3+7*j] = in0[4*i+j,3]
			aux[0][4+7*j] = in0[4*i+j,4]
			aux[0][5+7*j] = in0[4*i+j,5]
			aux[0][6+7*j] = in0[4*i+j,6]

		aux2 = numpy.array(list(zip(*[aux[0][idx:idx + 4] for idx in range(0, 28, 4)]))).flatten()
		#print(aux2)
		for j in range(4):
			out[4*i+j,0] = aux2[0+7*j]
			out[4*i+j,1] = aux2[1+7*j]
			out[4*i+j,2] = aux2[2+7*j]
			out[4*i+j,3] = aux2[3+7*j]
			out[4*i+j,4] = aux2[4+7*j]
			out[4*i+j,5] = aux2[5+7*j]
			out[4*i+j,6] = aux2[6+7*j]
		#print(out[i,0],out[i,1],out[i,2],out[i,3],out[i,4],out[i,5],out[i,6])

        #out[:] = in0
        return len(output_items[0])

