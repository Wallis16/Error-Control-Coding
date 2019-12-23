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
import operator
from gnuradio import gr

class Hamming_decoder_Diogenes_Wallis(gr.sync_block):
    """
    docstring for block Hamming_decoder_Diogenes_Wallis
    """
    def __init__(self, k):
	self.k = k
	#print(self.k)
        gr.sync_block.__init__(self,
            name="Hamming_decoder_Diogenes_Wallis",
            in_sig=[(numpy.float32,7)],
            out_sig=[(numpy.float32,4)])

    def work(self, input_items, output_items):
	#self.k += 1
	#print(self.k)
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
	code = numpy.zeros((1,7))
	code[0][0],code[0][1],code[0][2],code[0][3],code[0][4],code[0][5],code[0][6] = numpy.real(in0[0,0]),numpy.real(in0[0,1]),numpy.real(in0[0,2]),numpy.real(in0[0,3]),numpy.real(in0[0,4]),numpy.real(in0[0,5]),numpy.real(in0[0,6])

	c_vec = numpy.array([[0., 0., 0., 0., 0., 0., 0.],
       [0., 0., 0., 1., 0., 1., 1.],
       [0., 0., 1., 0., 1., 1., 0.],
       [0., 0., 1., 1., 1., 0., 1.],
       [0., 1., 0., 0., 1., 1., 1.],
       [0., 1., 0., 1., 1., 0., 0.],
       [0., 1., 1., 0., 0., 0., 1.],
       [0., 1., 1., 1., 0., 1., 0.],
       [1., 0., 0., 0., 1., 0., 1.],
       [1., 0., 0., 1., 1., 1., 0.],
       [1., 0., 1., 0., 0., 1., 1.],
       [1., 0., 1., 1., 0., 0., 0.],
       [1., 1., 0., 0., 0., 1., 0.],
       [1., 1., 0., 1., 0., 0., 1.],
       [1., 1., 1., 0., 1., 0., 0.],
       [1., 1., 1., 1., 1., 1., 1.]])

	max_ind = numpy.argmax(numpy.dot(code,(2*c_vec.transpose() - 1)))
	msg = c_vec[max_ind][0:4]

	out[:,0],out[:,1],out[:,2],out[:,3] = msg[0],msg[1],msg[2],msg[3]
	#print(in0[0,0]+1)        
	return len(output_items[0])

