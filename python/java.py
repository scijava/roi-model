# coding=UTF-8

import os
import subprocess

class Java:
    def __init__(self, model):
        self.model = model

    def dump(self):
        print('Generating Java reference implementation')
        if not os.path.exists("java"):
            os.makedirs("java")
