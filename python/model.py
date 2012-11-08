# coding=UTF-8

# TODO: Display comment lines from all spec tables in generated output.

class Primitive:
    def __init__(self, text):
        self.name, self.bintype, self.cxxtype, self.javatype, self.desc = text.split('\t')
        self.comment = ''

    def check(self):
        return

    def type(self):
        type = 'simple'
        if self.bintype == 'compound':
            type = 'compound'
        if self.cxxtype == 'enum' or self.javatype == 'enum':
            type = 'enum'
        return type

class Enum:
    def __init__(self, name):
        self.name = name
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

class Compound:
    def __init__(self, name):
        self.name = name
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

class Shape:
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

    def check(self):
        if (self.name not in ['Scale', 'Grid', 'Text']):

            if self.rep_canonical == None:
                raise Exception('Shape ' + str(self.id) + ' has no canonical representation')

            if self.rep_canonical not in self.rep_in:
                raise Exception('Shape ' + str(self.id) + ' does not have the canonical representation as an input representation')

            if self.rep_canonical not in self.rep_out:
                raise Exception('Shape ' + str(self.id) + ' does not have the canonical representation as an output representation')

        return

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
        self.primitive_names = dict()
        self.enum_names = dict()
        self.compound_names = dict()
        self.shape_ids = dict()
        self.shape_names = dict()
        self.representation_ids = dict()
        self.representation_names = dict()

        self.load_primitives()
        self.load_enums()
        self.load_compounds()
        self.load_shapes()
        self.load_reps()
        self.load_rep_members()
        self.load_shape_reps()
        self.load_shape_canonical_reps()
        self.load_shape_rels()
        self.check()

    def load_primitives(self):
        # Load shapes
        comment = ''
        for line in open ('spec/primitives.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0):
                continue
            if (line[0] == '#'):
                if (len(line) > 1 and line[1] == ' '):
                    comment += line[2:] + '\n'
                continue
            primitive = Primitive(line)
            if (len(comment) > 0):
                primitive.comment = comment
                comment = ''
            if primitive.name in self.primitive_names:
                raise Exception("Duplicate primitive " + primitive.name+':'+primitive.dim)
            self.primitive_names[primitive.name] = primitive

        # TODO: Sort
        for primitive in self.primitive_names.values():
            print(primitive.name)


    def load_enums(self):
        # Load shapes
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
        # Load shapes
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
            primitive, seqno, type, name, desc = line.split('\t')

            compound = None
            if primitive in self.compound_names:
                compound = self.compound_names[primitive]
            else:
                compound = Compound(primitive)
                self.compound_names[primitive] = compound
                print('** Added ** ' + primitive)

            mb = CompoundMember(seqno, type, name, desc)
            if (len(comment) > 0):
                mb.comment = comment
                comment = ''
            if mb.name in compound.members:
                raise Exception("Duplicate compound " + compound.name+':'+ mb.name)
            compound.members[mb.name] = mb

        # TODO: Sort
        for compound in self.compound_names.values():
            print(compound.name)


    def load_shapes(self):
        # Load shapes
        comment = ''
        for line in open ('spec/shapes.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0):
                continue
            if (line[0] == '#'):
                if (len(line) > 1 and line[1] == ' '):
                    comment += line[2:] + '\n'
                continue
            shape = Shape(line)
            if (len(comment) > 0):
                shape.comment = comment
                comment = ''
            if shape.id in self.shape_ids:
                raise Exception("Duplicate shape ID " + shape.id)
            self.shape_ids[shape.id] = shape
            if shape.name+':'+shape.dim in self.shape_names:
                raise Exception("Duplicate shape " + shape.name+':'+shape.dim)
            self.shape_names[shape.name+':'+shape.dim] = shape

    def load_reps(self):
        comment = ''
        # Load representations
        for line in open ('spec/representations.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0):
                continue
            if (line[0] == '#'):
                if (len(line) > 1 and line[1] == ' '):
                    comment += line[2:] + '\n'
                continue
            representation = Representation(line)
            if (len(comment) > 0):
                representation.comment = comment
                comment = ''
            if representation.id in self.representation_ids:
                raise Exception("Duplicate representation ID " + str(representation.id))
            self.representation_ids[representation.id] = representation
            if representation.name+':'+representation.dim in self.representation_names:
                raise Exception("Duplicate representation name+dim " + representation.name+':'+representation.dim)
            self.representation_names[representation.name+':'+representation.dim] = representation

    def load_rep_members(self):
        # Load representation members
        comment = ''
        for line in open ('spec/representationmembers.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0):
                continue
            if (line[0] == '#'):
                if (len(line) > 1 and line[1] == ' '):
                    comment += line[2:] + '\n'
                continue
            print(line)
            name, dim, memberseq, membername, membertype, memberdesc = line.split('\t')
            memberseq = int(memberseq)
            representation = self.representation_names[name+':'+dim]
            member = RepresentationMember(memberseq, membername, membertype, memberdesc)
            if (len(comment) > 0):
                member.comment = comment
                comment = ''
            if memberseq in representation.members:
                raise Exception("Duplicate representation " + str(representation.id) + " sequence " + str(memberseq))
            representation.members[memberseq] = member

    def load_shape_reps(self):
        # Load shape representations
        for line in open ('spec/shapereps.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0 or line[0] == '#'):
                continue
            shape, dim, rep, repdim, repin, repout, details = line.split('\t')
            s = self.shape_names[shape+':'+dim]
            srep = self.representation_names[rep+':'+repdim]
            if (repin == 'true'):
                s.rep_in.add(srep)
            if (repout == 'true'):
                s.rep_out.add(srep)

    def load_shape_canonical_reps(self):
        # Load shape representations
        for line in open ('spec/shapecanonreps.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0 or line[0] == '#'):
                continue
            shape, dim, rep, repdim = line.split('\t')
            s = self.shape_names[shape+':'+dim]
            srep = self.representation_names[rep+':'+repdim]
            if s.rep_canonical != None:
                raise Exception("Duplicate canonical representation for " + s.name+':'+s.dim)
            s.rep_canonical = srep

    def load_shape_rels(self):
        # Load shape relations
        comment = ''
        for line in open ('spec/shaperel.txt', 'rt'):
            line = line.rstrip('\n')
            if (len(line) == 0):
                continue
            if (line[0] == '#'):
                if (len(line) > 1 and line[1] == ' '):
                    comment += line[2:] + '\n'
                continue
            shape, dim, inherit, inheritdim, shapein, shapeout = line.split('\t')
            s = self.shape_names[shape+':'+dim]
            si = self.shape_names[inherit+':'+inheritdim]
            if (shapein == 'true'):
                s.inherit_in.add(si)
            if (shapeout == 'true'):
                s.inherit_out.add(si)
            if (len(comment) > 0):
                s.inherit_comment[inherit] = comment
                comment = ''

    def check(self):
        for shape in self.shape_ids.values():
            shape.check()
        for representation in self.representation_ids.values():
            representation.check()
# TODO: Add other types
# Validate that all enums and compounds have detailed form.
        return
