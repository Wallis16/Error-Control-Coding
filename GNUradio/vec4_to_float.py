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

class vec4_to_float(gr.sync_block):
    """
    docstring for block vec4_to_float
    """
    def __init__(self, k):
        gr.sync_block.__init__(self,
            name="vec4_to_float",
            in_sig=[(numpy.float32,4)],
            out_sig=[numpy.float32])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
	for i in range(int(len(in0)/4)):
		out[4*i] = in0[i,0]
		out[4*i+1] = in0[i,1]
		out[4*i+2] = in0[i,2]
		out[4*i+3] = in0[i,3]

        #out[:] = in0
        return len(output_items[0])

