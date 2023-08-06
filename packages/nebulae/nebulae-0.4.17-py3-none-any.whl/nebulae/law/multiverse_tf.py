#!/usr/bin/env python
'''
engine_mx
Created by Seria at 12/02/2019 3:45 PM
Email: zzqsummerai@yeah.net

                    _ooOoo_
                  o888888888o
                 o88`_ . _`88o
                 (|  0   0  |)
                 O \   。   / O
              _____/`-----‘\_____
            .’   \||  _ _  ||/   `.
            |  _ |||   |   ||| _  |
            |  |  \\       //  |  |
            |  |    \-----/    |  |
             \ .\ ___/- -\___ /. /
         ,--- /   ___\<|>/___   \ ---,
         | |:    \    \ /    /    :| |
         `\--\_    -. ___ .-    _/--/‘
   ===========  \__  NOBUG  __/  ===========

'''
# -*- coding:utf-8 -*-
import tensorflow as tf
import os
from types import MethodType

class Multiverse(object):
    '''
    Args:
    nworld: world size
    '''

    def __init__(self, universe, nworld=1):
        self.universe = universe
        self.nworld = nworld
        self.rank = -1

    def __call__(self):
        self.universe(self)

    def init(self):
        pass

    def scope(self):
        self.stg = tf.distribute.MirroredStrategy()
        return self.stg.scope()

    def Executor(self, func):
        def _execWrapper(*args, **kwargs):
            return self.stg.run(func, args, kwargs)

        return _execWrapper

    def sync(self, model, data):
        data = self.stg.experimental_distribute_dataset(data)
        return model, data

    def reduce(self, tensor, aggregate=False):
        if aggregate:
            reduce_op = tf.distribute.ReduceOp.SUM
        else:
            reduce_op = tf.distribute.ReduceOp.MEAN
        return self.stg.reduce(reduce_op, tensor, None)