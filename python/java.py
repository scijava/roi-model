# coding=UTF-8

import os
import subprocess
import getpass
import datetime

import model

headertmpl = """/*
 * #%L
 * SciJava ROI Model.
 * %%
 * Copyright © 2012 Open Microscopy Environment:
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


/*─────────────────────────────────────────────────────────────────────────────
 *
 * THIS IS AUTOMATICALLY GENERATED CODE.  DO NOT MODIFY.
 * Created by {0} via genspec on {1}
 *
 *─────────────────────────────────────────────────────────────────────────────
 */

"""

packagetmpl = """package {0};

"""

importtmpl = """import {0};
"""

class Enum(object):
    def __init__(self, model, enum):
        self.model = model
        self.enum = enum

    def write(self):
        nspath = self.enum.namespacepath()
        tn = self.enum.typename()

        if not os.path.exists('java/' + nspath):
            os.makedirs('java/' + nspath)
        ef = open('java/' + nspath + '/' + tn + '.java', 'w')
        ef.write(headertmpl.format(getpass.getuser(), datetime.datetime.now()))
        ef.write(packagetmpl.format(self.enum.namespace()))
        ef.write(importtmpl.format('java.util.EnumSet'))
        ef.write(importtmpl.format('java.util.Map'))
        ef.write(importtmpl.format('java.util.HashMap'))
        ef.write('\n')


        header = """public enum {0}{1}
{{
"""
        implements = ''
#        if len(type.inherits) > 0:
#            implements = ' ' + ', '.join([x.name() for x in self.enum.inherits])
        ef.write(header.format(tn, implements))

        values = sorted(self.enum.values.values(), key=lambda val: val.number)
        for val in values:
            if val.desc != '':
                ef.write('  // ' + val.desc)
                if val.symbol != '':
                    ef.write(' (' + val.symbol + ')')
                ef.write('\n')
            ef.write('  ' + val.name  + '("' + val.name + '", ' + val.number + ')')
            if val == values[-1]:
                ef.write(';\n')
            else:
                ef.write(',\n')

        footer = """
  public static {0} get(String str)
  {{
      {0} ret = strLookup.get(str);
      if (ret == null)
        throw new RuntimeException("{0}: Invalid enum string '" + str + "'");
      return ret;
  }}

  public static {0} get(int value)
  {{
      {0} ret = intLookup.get(value);
      if (ret == null)
        throw new RuntimeException("{0}: Invalid enum value " + value);
      return ret;
  }}

  public String toString()
  {{
    return str;
  }}

  private {0}(String str, int value)
  {{
    this.str = str;
    this.value = value;
  }}

  private final String str;
  private final int value;

  private static final Map<String,{0}> strLookup = new HashMap<String,{0}>();
  private static final Map<Integer,{0}> intLookup = new HashMap<Integer,{0}>();

  static
  {{
      for ({0} e : EnumSet.allOf({0}.class))
      {{
        strLookup.put(e.str, e);
        intLookup.put(e.value, e);
      }}
  }}
}}
"""
        ef.write(footer.format(tn))
        ef.close()

class Interface(object):
    def __init__(self, model, interface):
        self.model = model
        self.interface = interface

    def write(self):
        nspath = self.interface.namespacepath()
        tn = self.interface.typename()

        if not os.path.exists('java/' + nspath):
            os.makedirs('java/' + nspath)
        ef = open('java/' + nspath + '/' + tn + '.java', 'w')
        ef.write(headertmpl.format(getpass.getuser(), datetime.datetime.now()))
        ef.write(packagetmpl.format(self.interface.namespace()))
        if len(self.interface.inherits) > 0:
            for imp in self.interface.inherits:
                ef.write(importtmpl.format(imp.name))
            ef.write('\n')

        header = """public interface {0}{1}
{{
"""
        implements = ''
        if len(self.interface.inherits) > 0:
            implements = ' implements ' + ', '.join([x.typename() for x in self.interface.inherits])
        ef.write(header.format(tn, implements))

        footer = """
  // TODO: Add methods defined elsewhere.

}}
"""
        ef.write(footer.format(tn))
        ef.close()

class Class(object):
    def __init__(self, model, klass):
        self.model = model
        self.klass = klass

    def write(self):
        nspath = self.klass.namespacepath()
        tn = self.klass.typename()

        if not os.path.exists('java/' + nspath):
            os.makedirs('java/' + nspath)
        ef = open('java/' + nspath + '/' + tn + '.java', 'w')
        ef.write(headertmpl.format(getpass.getuser(), datetime.datetime.now()))
        ef.write(packagetmpl.format(self.klass.namespace()))
        if len(self.klass.inherits) > 0:
            for imp in self.klass.inherits:
                ef.write(importtmpl.format(imp.name))
            ef.write('\n')

        header = """public class {0}{1}
{{
"""
        implements = ''
        if len(self.klass.inherits) > 0:
            implements = ' implements ' + ', '.join([x.typename() for x in self.klass.inherits])
        ef.write(header.format(tn, implements))

        footer = """
  // TODO: Add methods defined elsewhere.

}}
"""
        ef.write(footer.format(tn))
        ef.close()

class Java:
    def __init__(self, model):
        self.model = model
        self.enums = set()
        self.classes = set()
        self.interfaces = set()
        self.types = set()
        self.imports = set()

    def dump(self):
        print('Generating Java reference implementation')
        if not os.path.exists("java"):
            os.makedirs("java")

        for typename in self.model.types:
            print 'Generating java code for ' + typename

            typedef = self.model.types[typename]

            if isinstance(typedef, model.Enum):
                self.enums.add(typedef)
                self.imports.add(typedef)
            elif isinstance(typedef, model.Interface):
                self.interfaces.add(typedef)
                self.imports.add(typedef)
            elif isinstance(typedef, model.Compound):
                self.classes.add(typedef)
                self.imports.add(typedef)
            else:
                self.types.add(typedef)

            for enum in self.enums:
                enum = Enum(self, enum)
                enum.write()

            for interface in self.interfaces:
                interface = Interface(self, interface)
                interface.write()

            for klass in self.classes:
                klass = Class(self, klass)
                klass.write()

