#!/usr/bin/env python

# unhashlib: A string class enhancement.

# The MIT License (MIT)
# 
# Copyright (c) 2018-21 Roberto Reale
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from builtins import chr
from builtins import zip

import hashlib
import re


class unhashlib(str):
    def __init__(self, *args, **kwargs):
        super(str, self).__init__() #*args, **kwargs)
        self.__encoding = 'utf-8'

    @property
    def encoding(self):
        return self.__encoding

    @encoding.setter
    def encoding(self, encoding):
        self.__encoding = encoding

    def get_algorithm(self, digest, algorithm="auto"):
        if algorithm == "auto":
            if digest is None or len(digest) == 0:
                return "nodigest"
            for candidate_algorithm in hashlib.algorithms_guaranteed:
                hasher = getattr(hashlib, candidate_algorithm)
                try:
                    if hasher(self.__str__().encode(self.__encoding)).hexdigest() == digest:
                        return candidate_algorithm
                except TypeError:
                    # https://docs.python.org/3/library/hashlib.html#shake-variable-length-digests
                    pass
        else:
            if algorithm in hashlib.algorithms_guaranteed:
                return algorithm
        return None

    def check(self, digest, algorithm="auto"):
        # for our purposes, `nodigest' is an algorithm (ex falso quodlibet)
        return (self.get_algorithm(digest, algorithm) is not None)

                
        
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
