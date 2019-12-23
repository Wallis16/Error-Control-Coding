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

class Hamming_encoder_Diogenes_Wallis(gr.sync_block):
    """
    docstring for block Hamming_encoder_Diogenes_Wallis
    """
    def __init__(self, k):
	self.k = k
        gr.sync_block.__init__(self,
            name="Hamming_encoder_Diogenes_Wallis",
            in_sig=[(numpy.float32,4)],
            out_sig=[(numpy.float32,7)])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
	h = numpy.array([[1,0,1],[1,1,1],[1,1,0],[0,1,1]])
	g = numpy.concatenate((numpy.identity(4), h), axis=1)
	msg = numpy.zeros((1,4))
	msg[0][0],msg[0][1],msg[0][2],msg[0][3] = in0[0,0],in0[0,1],in0[0,2],in0[0,3]
	#out[:] = in0[:,0] + in0[:,1] + in0[:,2] + in0[:,3]
	code = numpy.dot(msg,g)%2
	out[:,0],out[:,1],out[:,2],out[:,3],out[:,4],out[:,5],out[:,6] = code[0][0],code[0][1],code[0][2],code[0][3],code[0][4],code[0][5],code[0][6]
	#print(in0[0,0]+1)
#	aux = numpy.zeros((1,4))
#	for i in range(int(len(in0)/4)):
#		aux[0][0] = in0[i,0]
#		aux[0][1] = in0[i,1]
#		aux[0][2] = in0[i,2]
#		aux[0][3] = in0[i,3]
#		print(aux,i,int(len(in0)/4))
        
	return len(output_items[0])
	#print(in0[0][:].shape[0],in0[0][:].shape[1])


