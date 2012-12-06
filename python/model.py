# coding=UTF-8

# TODO: Display comment lines from all spec tables in generated output.

import glob
import re

class TypeBase(object):
    def __init__(self):
        super(TypeBase, self).__init__()
        self.comment = ''
        self.name = ''
        self.desc = ''

class Type(TypeBase):
    def __init__(self, name):
        super(Type, self).__init__()
        self.types = dict()
        self.name = name
        self.typeid = -1
        self.rep_in = set()
        self.rep_out = set()
        self.rep_canonical = None

    def check(self):
        return

    # def type(self):
    #     type = 'simple'
    #     if self.bintype == 'compound':
    #         type = 'compound'
    #     if self.cxxtype == 'enum' or self.javatype == 'enum':
    #         type = 'enum'
    #     return type

class Enum(TypeBase):
    def __init__(self, name):
        super(self.__class__, self).__init__()
        self.values = dict()

    def check(self):
# TODO: Check for duplicate names (and values).
        return

class EnumValue:
    def __init__(self, name, number, symbol, description):
        self.name = name
        self.number = number
        self.symbol = symbol
        self.desc = description
        self.comment = ''

    def check(self):
        return

class Inheritable(object):
    def __init__(self):
        super(Inheritable, self).__init__()
        self.inherits = list()

class Compound(TypeBase, Inheritable):
    def __init__(self, name):
        super(Compound, self).__init__()
        self.name = name
        self.templates = dict()
        self.members = dict()

    def check(self):
# TODO: Check for duplicate names (and members).
        return

class CompoundTemplate:
    def __init__(self, type, name, description):
        self.type = type
        self.name = name
        self.desc = description
        self.comment = ''

    def check(self):
        return

class CompoundMember:
    def __init__(self, seqno, type, name, description):
        self.seqno = seqno
        self.type = type
        self.name = name
        self.desc = description
        self.comment = ''

    def check(self):
        return

class Interface(TypeBase, Inheritable):
    def __init__(self, name, desc):
        super(Interface, self).__init__()
        self.name = name
        self.desc = desc

    def check(self):
        return

class ShapeBase(object):
    def __init__(self, text):
        self.id, self.name, self.dim, self.desc = text.split('\t')
        self.inherit_in = set()
        self.inherit_out = set()
        self.rep_in = set()
        self.rep_out = set()
        self.rep_canonical = None
        self.comment = ''
        self.inherit_comment = dict()

        if (self.id != 'ShapeID'):
            self.id = int(self.id)

    def reps(self):
        used = set()
        reps = dict()
        self.__reps(reps, used)

        return reps

    def reps_in(self):
        used = self.rep_in
        for s in self.inherited_in():
            used |= s.rep_in
        return used

    def reps_out(self):
        used = self.rep_out
        for s in self.inherited_out():
            used |= s.rep_out
        return used

    def __reps(self, reps, used):
        for r in self.rep_in | self.rep_out:
            if (r in reps):
                reps[r].add(self)
            else:
                reps[r] = set([self])
        used.add(self)
        for s in self.inherit_in | self.inherit_out:
            if (s not in used):
                s.__reps(reps, used)
        return

    def inherited_in(self):
        used = set()
        self.__inherited_in(used)
        used.remove(self)
        return used

    def __inherited_in(self, used):
        used.add(self)
        for s in self.inherit_in:
            if (s not in used):
                used.add(s)
                s.__inherited_in(used)

    def inherited_out(self):
        used = set()
        self.__inherited_out(used)
        used.remove(self)
        return used

    def __inherited_out(self, used):
        used.add(self)
        for s in self.inherit_out:
            if (s not in used):
                used.add(s)
                s.__inherited_out(used)

    # If we inherit a shape, we can use of all its in representations.
    def has_rep_in(self, rep):
        found = 0
        if rep in self.rep_in:
            found = 1
        else:
            for s in self.inherited_in():
                if s.__has_rep_in(rep):
                    found = 2
                    break
        return found

    def __has_rep_in(self, rep):
        found = 0
        if rep in self.rep_in:
            found = 1
        return found

    # If we inherit a shape, we can't necessarily use its out
    # representations (need to look up if that's possible using its in
    # representations directly).  i.e. we check if it inherits us (in
    # reverse)
    def has_rep_out(self, rep):
        found = 0
        if rep in self.rep_out:
            found = 1
        else:
            for s in self.inherited_out():
                if self in s.inherit_out and s.__has_rep_in(rep):
                    found = 2
                    break
        return found

    def __has_rep_out(self, rep):
        found = 0
        if rep in self.rep_out:
            found = 1
        return found

class Shape(ShapeBase):
    def __init__(self, text):
        super(self.__class__, self).__init__(text)

    def check(self):
        if (self.name not in ['Scale', 'Grid', 'Text']):

            if self.rep_canonical == None:
                raise Exception('Shape ' + str(self.id) + ' has no canonical representation')

            if self.rep_canonical not in self.rep_in:
                raise Exception('Shape ' + str(self.id) + ' does not have the canonical representation as an input representation')

            if self.rep_canonical not in self.rep_out:
                raise Exception('Shape ' + str(self.id) + ' does not have the canonical representation as an output representation')

        return

class DimConstraint(ShapeBase):
    def __init__(self, text):
        super(self.__class__, self).__init__(text)

    def check(self):
        return

class Representation:
    def __init__(self, text):
        self.id, self.name, self.dim, self.desc = text.split('\t')
        self.members = dict()
        self.comment = ''

        if (self.id != 'RepID'):
            self.id = int(self.id)

    # Consistency check.  Make sure that sequence numbers are correct,
    # with no missing numbers.
    def check(self):
        print('Checking ' + self.name + ':' + self.dim)
        for member in self.members.values():
            member.check()

        s = set()
        for member in self.members.values():
            s.add(member.seq)

        if (len(s) == 0):
            raise Exception("No members for representation " + str(self.id))

        m = max(s)
        if (s != set(range(0,m+1))):
            raise Exception("Invalid sequence IDs for representation " + str(self.id))
        return

    def dump_cxx_header(self, stream):
        name = self.name[1:] + self.dim

        slen = 14 + len(name) + 1
        nlen = max([len(x.name) for x in self.members.values()])
        tlen = max([len(x.type) for x in self.members.values()])

        ctor=''
        members = ''
        mlist = list(self.members.keys())
        mlist.sort()
        for i in mlist:
            m = self.members[i]
            if (i > 0):
                ctor += ' ' * slen
            ctor += m.type + ' ' * (tlen - len(m.type)) + ' ' + m.name;
            if i != max(mlist):
                ctor += ',\n'

            template = """
      class {0}
      {{
         public:
              {0}({1});

              ~{0}()
              {{}}

          {2}
      }}
"""
        stream.write(template.format(name, ctor, members))

class RepresentationMember:
    def __init__(self, seq, name, type, desc):
        self.seq = seq
        self.name = name
        self.type = type
        self.desc = desc
        self.comment = ''

        self.seq = int(self.seq)

    def check(self):
        return

class Model:
    def __init__(self):
        self.type_names = dict()
        self.primitive_names = dict()
        self.enum_names = dict()
        self.compound_names = dict()
        self.interface_names = dict()

        self.load_types()
        self.load_typeids()
        self.load_typereps()
        self.load_typecanonreps()
        self.load_enums()
        self.load_compounds()
        self.load_interfaces()
        self.load_inherits()
        self.check()

    def load_types(self):
        comment = ''
        for file in ['spec/types.txt'] + glob.glob('spec/types-*.txt'):
            print "Reading " + file
            find = re.search('^spec/types-(.*).txt$', file)
            lang = 'raw'
            if find:
                lang = find.group(1)
            print "Language " + lang
            for line in open (file, 'rt'):
                line = line.rstrip('\n')
                if (len(line) == 0):
                    continue
                if (line[0] == '#'):
                    if (len(line) > 1 and line[1] == ' '):
                        comment += line[2:] + '\n'
                    continue
                name, typename = line.split('\t')
                primitive = None
                if lang == 'raw':
                    primitive = Type(name)
                    if (len(comment) > 0):
                        primitive.comment = comment
                        comment = ''
                    if primitive.name in self.primitive_names:
                        raise Exception("Duplicate primitive: " + primitive.name)
                    self.primitive_names[primitive.name] = primitive
                else:
                    if name not in self.primitive_names.keys():
                        raise Exception("Type not found: " + name)
                    primitive = self.primitive_names[name]
                primitive.types[lang] = typename

        # TODO: Sort
        for primitive in self.primitive_names.values():
            print(primitive.name)

    def load_typeids(self):
        comment = ''

        used = set()

        for line in open ('spec/typeids.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0):
                continue
            if (line[0] == '#'):
                if (len(line) > 1 and line[1] == ' '):
                    comment += line[2:] + '\n'
                continue
            typeid, typename = line.split('\t')
            typeid = int(typeid)
            if typename not in self.primitive_names.keys():
                raise Exception("Type not found: " + typename)
            primitive = self.primitive_names[typename]

            if primitive.typeid != -1:
                raise Exception("Type has duplicate typeid: " + typename)

            if typeid in used:
                raise Exception("Duplicate typeid: " + str(typeid))
            used.add(typeid)

            primitive.typeid = typeid

        # TODO: Sort
        for primitive in self.primitive_names.values():
            print(primitive.name + ' = ' + str(primitive.typeid))

    def load_typereps(self):
        # Load type representations
        for line in open ('spec/typereps.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0 or line[0] == '#'):
                continue
            print line
            typename, rep, repin, repout  = line.split('\t')

            if typename not in self.primitive_names.keys():
                raise Exception("Type not found: " + typename)
            primitive = self.primitive_names[typename]

            if (repin == 'true'):
                if rep in primitive.rep_in:
                    raise Exception("Type "+typename+" has duplicate rep_in: " + rep_in)
                primitive.rep_in.add(rep)
            if (repout == 'true'):
                if rep in primitive.rep_out:
                    raise Exception("Type "+typename+" has duplicate rep_out: " + rep_out)
                primitive.rep_out.add(rep)

    def load_typecanonreps(self):
        # Load type representations
        for line in open ('spec/typecanonreps.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0 or line[0] == '#'):
                continue
            print line
            typename, canonrep = line.split('\t')

            if typename not in self.primitive_names.keys():
                raise Exception("Type not found: " + typename)
            primitive = self.primitive_names[typename]

            if canonrep not in primitive.rep_in:
                raise Exception("Type "+typename+" has no rep_in for canonrep: " + canonrep)
            primitive.rep_canonical = canonrep

    def load_enums(self):
        comment = ''
        for line in open ('spec/enums.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0):
                continue
            if (line[0] == '#'):
                if (len(line) > 1 and line[1] == ' '):
                    comment += line[2:] + '\n'
                continue
            print(line)

            primitive, name, number, symbol, desc = line.split('\t')

            if primitive not in self.primitive_names.keys():
                raise Exception("Type not found: " + primitive)

            enum = None
            if primitive in self.enum_names:
                enum = self.enum_names[primitive]
            else:
                enum = Enum(primitive)
                self.enum_names[primitive] = enum
                print('** Added ** ' + primitive)

            val = EnumValue(name, number, symbol, desc)
            if (len(comment) > 0):
                val.comment = comment
                comment = ''
            if val.name in enum.values:
                raise Exception("Duplicate enum " + enum.name+':'+ val.name)
            enum.values[val.name] = val

        # TODO: Sort
        for enum in self.enum_names.values():
            print(enum.name)

    def load_compounds(self):
        comment = ''
        for line in open ('spec/compounds.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0):
                continue
            if (line[0] == '#'):
                if (len(line) > 1 and line[1] == ' '):
                    comment += line[2:] + '\n'
                continue
            print(line)
            primitive, seqno, name, type, desc = line.split('\t')

            compound = None
            if primitive in self.compound_names:
                compound = self.compound_names[primitive]
            else:
                compound = Compound(primitive)
                self.compound_names[primitive] = compound
                print('** Added ** ' + primitive)

            try:
                seqno = int(seqno)

                mb = CompoundMember(seqno, type, name, desc)
                if (len(comment) > 0):
                    mb.comment = comment
                    comment = ''
                    if mb.name in compound.members:
                        raise Exception("Duplicate compound " + compound.name+':'+ mb.name)
                compound.members[mb.name] = mb

            except ValueError:
                # if seqno is not a number, it's a template parameter
                tp = CompoundTemplate(type, name, desc)
                if (len(comment) > 0):
                    tp.comment = comment
                    comment = ''
                    if tp.name in compound.templates:
                        raise Exception("Duplicate template parameter " + compound.name+':'+ tp.name)
                compound.templates[tp.name] = tp

        # TODO: Sort
        for compound in self.compound_names.values():
            print(compound.name)

    def load_interfaces(self):
        comment = ''
        for line in open ('spec/interfaces.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0):
                continue
            if (line[0] == '#'):
                if (len(line) > 1 and line[1] == ' '):
                    comment += line[2:] + '\n'
                continue
            print(line)
            name, desc = line.split('\t')

            interface = Interface(name, desc)

            if (len(comment) > 0):
                interface.comment = comment
                comment = ''

            if (len(comment) > 0):
                interface.comment = comment
                comment = ''

            if interface.name in self.interface_names:
                raise Exception("Duplicate interface: " + interface.name)
            if interface.name in self.type_names:
                raise Exception("Duplicate type: " + interface.name)

            self.interface_names[interface.name] = interface
            self.type_names[interface.name] = interface

        # TODO: Sort
        for interface in self.interface_names.values():
            print(interface.name)

    def load_inherits(self):
        comment = ''
        for line in open ('spec/inherits.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0):
                continue
            if (line[0] == '#'):
                if (len(line) > 1 and line[1] == ' '):
                    comment += line[2:] + '\n'
                continue
            print(line)
            name, inherits = line.split('\t')

            if name not in self.type_names:
                raise Exception("Type not found: " + name)
            itype = self.type_names[name]

            if not isinstance(itype, Inheritable):
                raise Exception("Type does not support inheritance: " + name)

            if (inherits != ''):
                for iname in inherits.split(','):
                    iface = None
                    if iname in self.interface_names and isinstance(self.interface_names[iname], Inheritable):
                        iface = self.interface_names[iname]
                    else:
                        raise Exception("Invalid interface: " + iname)
                    if iface in itype.inherits:
                        raise Exception("Duplicated inheritance for "+name+" interface: " + iname)
                    itype.inherits.append(iface)

    def check(self):
#        for shape in self.shape_ids.values():
#            shape.check()
#        for representation in self.representation_ids.values():
#            representation.check()
# TODO: Add other types
# Validate that all enums and compounds have detailed form.
        return
