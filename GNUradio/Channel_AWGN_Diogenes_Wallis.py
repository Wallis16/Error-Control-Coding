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

class Channel_AWGN_Diogenes_Wallis(gr.sync_block):
    """
    docstring for block Channel_AWGN_Diogenes_Wallis
    """
    def __init__(self, k):
	self.k = k
        gr.sync_block.__init__(self,
            name="Channel_AWGN_Diogenes_Wallis",
            in_sig=[(numpy.float32,7)],
            out_sig=[(numpy.float32,7)])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
	#code = numpy.zeros((1,7))

	Ec_N0_dB = numpy.array([-2.43038049, -1.43038049, -0.43038049,  0.56961951,  1.56961951,
        2.56961951,  3.56961951,  4.56961951,  5.56961951,  6.56961951,7.56961951])

	#Channel - AWGN
	mu, sigma = 0, 1
	n = (1/numpy.sqrt(2))*(numpy.random.normal(mu, sigma, (1,28)) + 1j*numpy.random.normal(mu, sigma, (1,28))) #white gaussian noise, 0dB variance

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

		#Noise addition
		aux = aux + (10**(-Ec_N0_dB[self.k]/20))*n

		for j in range(4):
			out[4*i+j,0] = aux[0][0+7*j]
			out[4*i+j,1] = aux[0][1+7*j]
			out[4*i+j,2] = aux[0][2+7*j]
			out[4*i+j,3] = aux[0][3+7*j]
			out[4*i+j,4] = aux[0][4+7*j]
			out[4*i+j,5] = aux[0][5+7*j]
			out[4*i+j,6] = aux[0][6+7*j]


#	code[0][0],code[0][1],code[0][2],code[0][3],code[0][4],code[0][5],code[0][6] = in0[0,0],in0[0,1],in0[0,2],in0[0,3],in0[0,4],in0[0,5],in0[0,6]
		
	#Noise addition
	#y = code + (10**(-Ec_N0_dB[self.k]/20))*n
	#y = numpy.real(y)

	#out[:,0],out[:,1],out[:,2],out[:,3],out[:,4],out[:,5],out[:,6] = y[0][0],y[0][1],y[0][2],y[0][3],y[0][4],y[0][5],y[0][6]

        #out[:] = in0
        return len(output_items[0])

