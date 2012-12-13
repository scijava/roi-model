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

class Base(object):
    def __init__(self, model, typeinfo):
        super(Base, self).__init__()
        self.model = model
        self.typeinfo = typeinfo

    def write_members(self, fh):
        path = 'spec/java/' + self.typeinfo.name + '-members.java'
        if os.path.exists(path):
            fh.write("""
  /*
   * Members (static definitions)
   *
""")
            for line in open(path, 'rt'):
                fh.write('  ' + line)
            fh.write('\n')
        else:
            print "No definitions in " + path

class Enum(Base):
    def __init__(self, model, enum):
        super(Enum, self).__init__(model, enum)

    def write(self):
        nspath = self.typeinfo.namespacepath()
        tn = self.typeinfo.typename()

        if not os.path.exists('java/' + nspath):
            os.makedirs('java/' + nspath)
        filename = 'java/' + nspath + '/' + tn + '.java'
        ef = open(filename, 'w')
        ef.write(headertmpl.format(getpass.getuser(), datetime.datetime.now()))
        ef.write(packagetmpl.format(self.typeinfo.namespace()))
        ef.write(importtmpl.format('java.util.EnumSet'))
        ef.write(importtmpl.format('java.util.Map'))
        ef.write(importtmpl.format('java.util.HashMap'))
        ef.write('\n')


        header = """public enum {0}{1}
{{
"""
        implements = ''
#        if len(type.inherits) > 0:
#            implements = ' ' + ', '.join([x.name() for x in self.typeinfo.inherits])
        ef.write(header.format(tn, implements))

        values = sorted(self.typeinfo.values.values(), key=lambda val: val.number)
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

        return filename

class Interface(Base):
    def __init__(self, model, interface):
        super(Interface, self).__init__(model, interface)

    def write(self):
        nspath = self.typeinfo.namespacepath()
        tn = self.typeinfo.typename()

        if not os.path.exists('java/' + nspath):
            os.makedirs('java/' + nspath)
        filename = 'java/' + nspath + '/' + tn + '.java'
        ef = open(filename, 'w')
        ef.write(headertmpl.format(getpass.getuser(), datetime.datetime.now()))
        ef.write(packagetmpl.format(self.typeinfo.namespace()))
        if len(self.typeinfo.inherits) > 0:
            for imp in self.typeinfo.inherits:
                ef.write(importtmpl.format(imp.name))
            ef.write('\n')

        header = """public interface {0}{1}
{{
"""
        implements = ''
        if len(self.typeinfo.inherits) > 0:
            implements = ' implements ' + ', '.join([x.typename() for x in self.typeinfo.inherits])
        ef.write(header.format(tn, implements))

        footer = """
  // TODO: Add methods defined elsewhere.

}}
"""
        ef.write(footer.format(tn))
        ef.close()

        return filename


class Class(Base):
    def __init__(self, model, klass):
        super(Class, self).__init__(model, klass)

    def write(self):
        nspath = self.typeinfo.namespacepath()
        tn = self.typeinfo.typename()

        shapetype = self.model.types['scijava.roi.shape.PhysicalShape']

        if not os.path.exists('java/' + nspath):
            os.makedirs('java/' + nspath)
        filename = 'java/' + nspath + '/' + tn + '.java'
        ef = open(filename, 'w')
        ef.write(headertmpl.format(getpass.getuser(), datetime.datetime.now()))
        ef.write(packagetmpl.format(self.typeinfo.namespace()))
        imports = set(self.typeinfo.inherits)
        if shapetype in self.typeinfo.inherits:
            imports.add(self.typeinfo.rep_canonical)
        if len(imports) > 0:
            for imp in imports:
                ef.write(importtmpl.format(imp.name))
            ef.write('\n')

        header = """public class {0}{1}
{{
"""
        implements = ''
        if len(self.typeinfo.inherits) > 0:
            implements = ' implements ' + ', '.join([x.typename() for x in self.typeinfo.inherits])
        ef.write(header.format(tn, implements))

        # Generate canonical representation
        if shapetype in self.typeinfo.inherits:
            ef.write("""  /*
   * Members (shape definitions)
   */

  /// Canonical representation
""")
            ef.write('  ' + self.typeinfo.rep_canonical.typename() + ' rep_canonical;\n')
            ef.write("""

  /// Generic representation
  Object rep_generic;
""")

        self.write_members(ef)

        footer = """
  // TODO: Add methods defined elsewhere.

}}
"""
        ef.write(footer.format(tn))
        ef.close()

        return filename

class Java:
    def __init__(self, model):
        self.model = model
        self.enums = set()
        self.classes = set()
        self.interfaces = set()
        self.types = set()
        self.imports = set()
        self.code = set()

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
                enum = Enum(self.model, enum)
                file = enum.write()
                self.code.add(file)

            for interface in self.interfaces:
                interface = Interface(self.model, interface)
                file = interface.write()
                self.code.add(file)

            for klass in self.classes:
                klass = Class(self.model, klass)
                file = klass.write()
                file = self.code.add(file)

            for typename in self.types:
                # Only write out classes, not primitives or aliases for other types
                if 'java' not in typename.types:
                    klass = Class(self.model, typename)
                    klass.write()

            self.dump_sphinx()

    def dump_sphinx(self):
        sj = open('java.rst','w')

        header = """Java code
=========

The following source files have been generated from the specification.

"""
        sj.write(header)

        for file in sorted(self.code):
            sj.write("- :download:`{0} <{0}>`\n".format(file))
