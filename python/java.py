# coding=UTF-8

import os
import subprocess

from model import PrimitiveBase

class TypeBase(object):
    def __init__(self):
        # Documentation for JavaDocs
        doc=''
        # Dependencies for imports
        deps=''

class File(object):
    def __init__(self):
        # Copyright header
        header = ''
        # From class namespace
        package = ''
        # From class imports
        imports = ''
        # From namespace and class name
        filename = ''
        classname = None

class Compound(TypeBase):
    def __init(self):
        name = ''
        namespace = ''

class Class(Compound):
    def __init__(self):
        superclass = None
        interfaces = []
        constants = []
        fields = []
        ctors = []
        dtor = None
        methods = []

class Interface(Compound):
    def __init__(self):
        interfaces = []
        # List of method objects
        methods = []

class Enum(Class):
    def __init__(self):
        # Mapping of enumerated values to objects
        values = map()

class TypeInstance(TypeBase):
    def __init__(self):
        typename = ''
        typeinstancename = ''
        defaultvalue = ''

class Method(TypeBase):
    def __init__(self):
        args = []
        implementation = ''

class Java:
    def __init__(self, model):
        self.model = model
        self.classes = dict()
        self.interfaces = dict()
        self.enum = dict()

    def dump(self):
        print('Generating Java reference implementation')
        if not os.path.exists("java"):
            os.makedirs("java")
