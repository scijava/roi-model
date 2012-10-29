# coding=UTF-8

import os
import subprocess

class Cxx:
    def __init__(self, model):
        self.model = model

    def dump(self):
        print('Generating C++ reference implementation')
        if not os.path.exists("c++"):
            os.makedirs("c++")

        header = """/*
 * #%L
 * SciJava ROI Model.
 * %%
 * Copyright (C) 2012 Open Microscopy Environment:
 *   - Board of Regents of the University of Wisconsin-Madison
 *   - Glencoe Software, Inc.
 *   - University of Dundee
 * %%
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as
 * published by the Free Software Foundation, either version 2 of the 
 * License, or (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public 
 * License along with this program.  If not, see
 * <http://www.gnu.org/licenses/gpl-2.0.html>.
 * #L%
 */
"""

        nstart = """
#ifndef {0}
#define {0} 1

namespace scijava {{
  namespace roi {{
"""
        nend = """  }}
}}

// {0}
"""

        reph = open('c++/representations.h', 'w')
        repc = open('c++/representations.cpp', 'w')

        print('  representations')

        reph.write(header)
        repc.write(header)
        reph.write(nstart.format('SCIJAVA_REPRESENTATIONS_H'))
        reph.write('    namespace representation {\n')
        for rep in self.model.representation_ids.values():
 
            rep.dump_cxx_header(reph)

        reph.write('    }\n')
        reph.write(nend.format('SCIJAVA_REPRESENTATIONS_H'))
