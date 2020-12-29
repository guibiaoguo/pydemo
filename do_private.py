#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '
__author__ = 'GuiBiao Guo'

import hello

def _private_1(name):
    return 'Hello, %s' % name

def _private_2(name):
    return 'Hi, %s' % name

def greeting(name):
    if len(name) > 3:
        return _private_1(name)
    else:
        return _private_2(name)
if __name__ == '__main__':
    print(greeting('Bill'))
    print(hello.test())