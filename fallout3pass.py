#!/usr/bin/env python
import sys

# ============================================================================
# The MIT License (MIT)
# 
# Copyright (c) 2014 Michael Hansen
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ============================================================================

#  EXAMPLE
#  -------
#  1. Enter all words
#  2. Try a word, enter it and the number of correct characters
#  3. Possible words are printed - if only one, that's it!
#  -------
#
#  Enter words (blank line when done, quit to exit)
#  >> sneaking
#  >> lockpick
#  >> throwing
#  >> smelling
#  >> grenades 
#  >> 
#  Enter attempts (word number_right)
#  >> lockpick 0
#  grenades
#  >> quit

def matches(w1, w2):
    """Returns the number of matching characters in two words"""
    assert len(w1) == len(w2)
    m = 0

    for (c1, c2) in zip(w1, w2):
        if c1 == c2:
            m += 1

    return m

def filter_words(words, attempts):
    """Filter candidate words according to attempts (word, # correct)"""
    words = set(words)

    for a in attempts:
        words.remove(a[0])

    for w in words:
        valid = True

        for a in attempts:
            if matches(w, a[0]) != a[1]:
                valid = False
                break

        if valid:
            print w

if __name__ == '__main__':
    words = []
    attempts = []

    print "Enter words (blank line when done, quit to exit)"

    input = raw_input(">> ")
    inputting_words = True

    while input != "quit":
        if inputting_words:
            if len(input.strip()) == 0:
                inputting_words = False
                print "Enter attempts (word number_right)"
            else:
                words.append(input.strip())
        else:
            parts = input.strip().split(' ')
            attempts.append((parts[0], int(parts[1])))
            filter_words(words, attempts)

        input = raw_input(">> ")
