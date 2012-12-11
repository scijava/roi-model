# coding=UTF-8

# TODO: Display comment lines from all spec tables in generated output.

import glob
import re

# Basic type.  This is just a name.
class TypeBase(object):
    def __init__(self, name):
        super(TypeBase, self).__init__()
        self.comment = ''
        self.name = name
        self.desc = ''
        self.inherits = list()

    def inherited(self):
        used = set()
        self.__inherited(used)
        used.remove(self)
        return used

    def __inherited(self, used):
        used.add(self)
        for s in self.inherits:
            if (s not in used):
                used.add(s)
                s.__inherited(used)

# Basic concrete type.  This is just a name and type identifier
# (i.e. it's used for serialiation)
class ConcreteTypeBase(TypeBase):
    def __init__(self, name):
        if isinstance(name, TypeBase):
            super(ConcreteTypeBase, self).__init__(name.name)
            if isinstance(name, ConcreteTypeBase):
                self.typeid = name.typeid
            else:
                self.typeid = -1
        else:
            super(ConcreteTypeBase, self).__init__(name)
            self.typeid = -1

# Primitive type.
class Type(ConcreteTypeBase):
    def __init__(self, primitive):
        super(Type, self).__init__(primitive)
        self.types = dict()
        self.rep_in = set()
        self.rep_out = set()
        self.rep_canonical = None

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
        for s in self.inherits:
            if (s not in used):
                s.__reps(reps, used)
        return

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

    def check(self):
        return

    # def type(self):
    #     type = 'simple'
    #     if self.bintype == 'compound':
    #         type = 'compound'
    #     if self.cxxtype == 'enum' or self.javatype == 'enum':
    #         type = 'enum'
    #     return type

class Enum(ConcreteTypeBase):
    def __init__(self, primitive):
        super(Enum, self).__init__(primitive)
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


class Compound(Type):
    def __init__(self, primitive):
        super(Compound, self).__init__(primitive)
        self.templates = dict()
        self.members = dict()

    def check(self):
# TODO: Check for duplicate names (and members).
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

class Interface(TypeBase):
    def __init__(self, name, desc):
        super(Interface, self).__init__(name)
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

class Shape(ShapeBase):
    def __init__(self, text):
        super(Shape, self).__init__(text)

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
        super(DimConstraint, self).__init__(text)

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
        self.types = dict()

        self.load_types(self.types)
        self.load_enums(self.types)
        self.load_interfaces(self.types)
        self.load_compounds(self.types)

        self.load_typeids(self.types)
        self.load_typereps(self.types)
        self.load_typecanonreps(self.types)
        self.load_inherits(self.types)
        self.check()

    def load_types(self, type_names):
        comment = ''
        for file in ['spec/types.txt'] + glob.glob('spec/types-*.txt'):
            print "Reading " + file
            find = re.search('^spec/types-(.*).txt$', file)
            lang = 'undefined'
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
                if lang == 'undefined':
                    primitive = Type(name)
                    primitive.desc = typename
                    if (len(comment) > 0):
                        primitive.comment = comment
                        comment = ''
                    if primitive.name in type_names:
                        raise Exception("Duplicate primitive: " + primitive.name)
                    type_names[primitive.name] = primitive
                    print "Added primitive type: " + primitive.name + ' (' + type_names[primitive.name].name + ')'
                else:
                    if name not in type_names.keys():
                        raise Exception("Type not found: " + name)
                    primitive = type_names[name]
                if lang != 'undefined':
                    primitive.types[lang] = typename

        # TODO: Sort
        for primitive in type_names.values():
            print(primitive.name)

    def load_typeids(self, type_names):
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
            if typename not in type_names.keys():
                raise Exception("Type not found: " + typename)
            primitive = type_names[typename]

            if not isinstance(primitive, ConcreteTypeBase):
                raise Exception("Type is not concrete, and does not permit setting a typeid: " + typename)

            if primitive.typeid != -1:
                raise Exception("Type has duplicate typeid: " + typename)

            if typeid in used:
                raise Exception("Duplicate typeid: " + str(typeid))
            used.add(typeid)

            primitive.typeid = typeid

        # TODO: Sort
        for primitive in type_names.values():
            if isinstance(primitive, ConcreteTypeBase):
                print(primitive.name + ' = ' + str(primitive.typeid))

    def load_typereps(self, type_names):
        # Load type representations
        for line in open ('spec/typereps.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0 or line[0] == '#'):
                continue
            print line
            typename, rep, repin, repout  = line.split('\t')

            if typename not in type_names.keys():
                raise Exception("Type not found: " + typename)
            primitive = type_names[typename]

            if rep not in type_names.keys():
                raise Exception("Type representation not found: " + rep)
            rep = type_names[rep]

            if (repin == 'true'):
                if rep in primitive.rep_in:
                    raise Exception("Type "+typename+" has duplicate rep_in: " + rep_in)
                primitive.rep_in.add(rep)
            if (repout == 'true'):
                if rep in primitive.rep_out:
                    raise Exception("Type "+typename+" has duplicate rep_out: " + rep_out)
                primitive.rep_out.add(rep)

    def load_typecanonreps(self, type_names):
        # Load type representations
        for line in open ('spec/typecanonreps.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0 or line[0] == '#'):
                continue
            print line
            typename, canonrep = line.split('\t')

            if typename not in type_names.keys():
                raise Exception("Type not found: " + typename)
            primitive = type_names[typename]

            if canonrep not in type_names.keys():
                raise Exception("Canonical type representation not found: " + typename)
            canonrep = type_names[canonrep]

            if canonrep not in primitive.rep_in:
                raise Exception("Type "+typename+" has no rep_in for canonrep: " + canonrep)
            primitive.rep_canonical = canonrep

    def load_enums(self, type_names):
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

            if primitive not in type_names.keys():
                raise Exception("Type not found: " + primitive)

            enum = None
            if primitive in type_names and isinstance(type_names[primitive], Enum):
                if isinstance(type_names[primitive], Enum):
                    enum = type_names[primitive]
            else:
                enum = Enum(primitive)
                type_names[primitive] = enum

            val = EnumValue(name, number, symbol, desc)
            if (len(comment) > 0):
                val.comment = comment
                comment = ''
            if val.name in enum.values:
                raise Exception("Duplicate enum " + enum.name+':'+ val.name)
            enum.values[val.name] = val

    def load_compounds(self, type_names):
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
            primitive, seqno, name, typename, desc = line.split('\t')

            compound = None
            if primitive in type_names:
                if isinstance(type_names[primitive], Compound):
                    compound = type_names[primitive]
                else:
                    compound = Compound(type_names[primitive])
                    type_names[primitive] = compound
            else:
                raise Exception("Invalid compound name: " + primitive)

            try:
                seqno = int(seqno)

                mb = CompoundMember(seqno, typename, name, desc)
                if (len(comment) > 0):
                    mb.comment = comment
                    comment = ''
                    if mb.name in compound.members:
                        raise Exception("Duplicate compound " + compound.name+':'+ mb.name)
                compound.members[mb.name] = mb
                print "COMPOUND = " + compound.name + "  MEMBERSCOUNT=" + str(len(compound.members))

            except ValueError:
                seqno = re.sub('^T', '', seqno)
                seqno = int(seqno)
                # if seqno is not a number, it's a template parameter
                tp = CompoundMember(seqno, typename, name, desc)
                if (len(comment) > 0):
                    tp.comment = comment
                    comment = ''
                    if tp.name in compound.templates:
                        raise Exception("Duplicate template parameter " + compound.name+':'+ tp.name)
                compound.templates[tp.name] = tp

        # TODO: Sort
        for compound in type_names.values():
            if isinstance(compound, Compound):
                print(compound.name)

    def load_interfaces(self, type_names):
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

            if interface.name in type_names:
                raise Exception("Duplicate interface: " + interface.name)
            if interface.name in type_names:
                raise Exception("Duplicate type: " + interface.name)

            type_names[interface.name] = interface

        # TODO: Sort
        for interface in type_names.values():
            if isinstance(interface, Interface):
                print(interface.name)

    def load_inherits(self, type_names):
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

            if name not in type_names:
                raise Exception("Type not found: " + name)
            itype = type_names[name]

            if not isinstance(itype, TypeBase):
                raise Exception("Type does not support inheritance: " + name)

            iface = None
            if inherits in type_names and isinstance(type_names[inherits], Interface):
                iface = type_names[inherits]
            else:
                raise Exception("Invalid interface: " + inherits)
            if iface in itype.inherits:
                raise Exception("Duplicated inheritance for "+name+" interface: " + inherits)
            itype.inherits.append(iface)

    def check(self):
#        for shape in self.shape_ids.values():
#            shape.check()
#        for representation in self.representation_ids.values():
#            representation.check()
# TODO: Add other types
# Validate that all enums and compounds have detailed form.
        return
