#!/usr/bin/env python
'''
component_tf
Created by Seria at 05/02/2019 1:41 PM
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
from math import ceil
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras import Model, layers, losses, optimizers


# 'Grad',
# 'EMA',
# 'CBN', 'IN', 'CIN', 'LN', 'SN',
# 'AdaBelief'
__all__ = ('Craft', 'Rudder', 'Nozzle',
           'NEAREST', 'LINEAR', 'CUBIC',
           'Void', 'XavierNorm', 'XavierUnif', 'Normal', 'Uniform', 'Orthog', 'Zeros', 'Ones',
           'Conv', 'TransConv', 'Dense', 'Embed', 'Identity',
           'Mean', 'Max', 'Min', 'Sum', 'MatMul',
           'Reshape', 'Permute', 'Upscale', 'MaxPool', 'AvgPool',
           'EMA',
           'Sqrt',
           'Concat',
           'Clip', 'Dropout', 'BN',
           'Relu', 'LRelu', 'Tanh', 'Sigm', 'Sftm', 'Sftp',
           'MAE', 'MSE', 'SigmXE', 'SftmXE',
           'AccCls',
           'StepLR', 'PolyLR', 'CosLR', 'ExpLR', 'WavyLR',
           'Momentum', 'Nesterov', 'RMSProp', 'Adam',)



NEAREST = 0
LINEAR = 1
CUBIC = 2
TF_INTERP = {NEAREST: 'nearest', LINEAR: 'bilinear', CUBIC: 'bicubic'}




class Craft(Model):
    def __init__(self, engine, scope):
        super(Craft, self).__init__()
        self.engine = engine
        self.scope = scope
        self.__pods = []
        self.__dict = {}
        self.__formulated = False

    # @tf.function
    def run(self, *args, **kwargs):
        raise NotImplementedError

    def call(self, *args, **kwargs):
        # assert all([isinstance(a, Tensor) for a in args])
        kwargs.pop('training')
        return self.run(*args, **kwargs)

    def gear(self, gr=None):
        if isinstance(gr, bool):
            assert not gr
            self.trainable = False
        elif isinstance(gr, tf.python.eager.backprop.GradientTape):
            self._rudder = gr
            self.trainable = True
        elif gr is None:
            pass
        else:
            raise Exception('NEBULAE ERROR ⨷ %s is not a valid type of gear.' % type(gr))

    def vars(self):
        return self.trainable_weights

    @property
    def pods(self):
        return self.__pods

    @pods.setter
    def pods(self, pods):
        if not self.__formulated:
            self.__pods = pods
            self.__formulated = True

    def __getitem__(self, key):
        paths = key.split('/')
        craft = self
        for p in paths[:-1]:
            craft = getattr(craft, p)
        if paths[-1] == '':
            return craft
        else:
            return craft.__dict[paths[-1]]

    def __setitem__(self, key, value):
        self.__dict[key] = value



class Rudder(tf.GradientTape):
    def __init__(self):
        super(Rudder, self).__init__()



class Nozzle(object):
    def __init__(self):
        pass

    def __enter__(self):
        return False

    def __exit__(self, *args):
        pass



# -------------------------------------- Layer --------------------------------------- #

class Void(object):
    def __init__(self):
        self.iniz = 'ConstantV2'

class XavierNorm(object):
    def __init__(self):
        self.iniz = 'GlorotNormalV2'

class XavierUnif(object):
    def __init__(self):
        self.iniz = 'GlorotUniformV2'

class Normal(object):
    def __init__(self):
        self.iniz = 'RandomNormalV2'

class Uniform(object):
    def __init__(self):
        self.iniz = 'RandomUniformV2'

class Orthog(object):
    def __init__(self):
        self.iniz = 'OrthogonalV2'

class Ones(object):
    def __init__(self):
        self.iniz = 'OnesV2'

class Zeros(object):
    def __init__(self):
        self.iniz = 'ZerosV2'



class Conv(Craft):
    def __init__(self, in_chs, out_chs, kernel: tuple, stride=1, padding=0, dilation=1, group=1,
                 w_init=XavierNorm(), b_init=Zeros(), scope='CONV'):
        '''
        Args:
        - in_chs: input channel
        - out_chs: output channel
        - kernel: kernel size (must be a tuple)
        - stride: moving stride
        - padding: padding size
        - dilation: stride in atrous convolution
        - group: number of groups to be divided
        - w_init: weight initializer
        - w_param: options for initializing weight
        - b_init: bias initializer
        - b_param: options for initializing bias
        - scope: name scope
        '''
        super(Conv, self).__init__(None, scope)
        dim = len(kernel)
        if dim == 1:
            conv_fn = layers.Conv1D
            pad_fn = layers.ZeroPadding1D
        elif dim == 2:
            conv_fn = layers.Conv2D
            pad_fn = layers.ZeroPadding2D
        elif dim == 3:
            conv_fn = layers.Conv3D
            pad_fn = layers.ZeroPadding3D
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d convolution is not supported.' % dim)

        if isinstance(stride, int):
            stride = dim * [stride]
        if isinstance(dilation, int):
            dilation = dim * [dilation]
        if isinstance(padding, int):
            padding = dim * [[padding, padding]]
        elif isinstance(padding, (list, tuple)):
            padding = [(padding[2*d], padding[2*d+1]) for d in range(dim-1, -1, -1)]

        self.pad = pad_fn(padding)
        self.conv = conv_fn(out_chs, kernel, strides=stride, dilation_rate=dilation, groups=group,
                            use_bias=False if isinstance(b_init, Void) else True,
                            kernel_initializer=w_init.iniz, bias_initializer=b_init.iniz)

    def run(self, x):
        x = self.pad(x)
        y = self.conv(x)
        return y



class _Interpad(layers.Layer):
    def __init__(self, stride: list):
        super(_Interpad, self).__init__()
        self.stride = stride

    def call(self, x):
        dim = len(x.shape)
        size = x.shape[2:]
        assert len(size) == len(self.stride)
        for d in range(dim-2):
            step = list(x.shape[0:2]) + [1 if i==d else size[i] for i in range(len(size))]
            zeros = tf.zeros_like(tf.slice(x, dim * [0], step))
            lines = tf.split(x, size[d], axis=d+2)
            padded = [lines[0]]
            for l in lines[1:]:
                padded.extend([zeros, l])
            x = tf.concat(padded, axis=d+2)
            size = x.shape[2:]

class TransConv(Craft):
    def __init__(self, in_chs, out_chs, out_size, kernel: tuple, stride=1, padding=0, dilation=1, group=1,
                 w_init=XavierNorm(), b_init=Zeros(), scope='TRANSCONV'):
        '''
        Args:
        - in_chs: input channel
        - out_chs: output channel
        - out_size: output size
        - kernel: kernel size (must be a tuple)
        - stride: moving stride
        - padding: padding size
        - dilation: stride in atrous convolution
        - group: number of groups to be divided
        - w_init: weight initializer
        - w_param: options for initializing weight
        - b_init: bias initializer
        - b_param: options for initializing bias
        - scope: name scope
        '''
        super(TransConv, self).__init__(None, scope)
        dim = len(kernel)
        if dim == 1:
            conv_fn = layers.Conv1D
            pad_fn = layers.ZeroPadding1D
        elif dim == 2:
            conv_fn = layers.Conv2D
            pad_fn = layers.ZeroPadding1D
        elif dim == 3:
            conv_fn = layers.Conv3D
            pad_fn = layers.ZeroPadding1D
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d convolution is not supported.' % dim)

        if isinstance(stride, int):
            stride = dim * [stride]
        if isinstance(dilation, int):
            dilation = dim * [dilation]
        if isinstance(padding, int):
            padding = dim * [2 * padding]
        elif isinstance(padding, (list, tuple)):
            padding = [padding[2*d] + padding[2*d+1] for d in range(dim-1, -1, -1)]

        in_size = []
        total_pad = []
        exter_pad = []
        for d in range(dim):
            in_size.append((out_size[d] + padding[d] - dilation[d]*(kernel[d]-1) -1) // stride[d] + 1)
            total_pad.append(dilation[d]*(kernel[d]-1) + out_size[d] - in_size[d])
            inter_pad = (in_size[d] - 1) * (stride[d] - 1)
            exter_pad.append(((total_pad[d] - inter_pad)//2, (total_pad[d] - inter_pad)-(total_pad[d] - inter_pad)//2))

        # TODO: [to be verified] interpolate stride-1 zeros between every two lines of input
        self.inter_pad = _Interpad(stride)
        self.exter_pad = pad_fn(exter_pad)
        self.conv = conv_fn(out_chs, kernel, strides=1, padding=padding, dilation_rate=dilation, groups=group,
                            use_bias=False if isinstance(b_init, Void) else True,
                            kernel_initializer=w_init.iniz, bias_initializer=b_init.iniz)

    def run(self, x):
        y = self.conv(self.exter_pad(self.inter_pad(x)))
        return y



class Dense(Craft):
    def __init__(self, in_chs, out_chs, axis=-1,
                 w_init=XavierNorm(), b_init=Zeros(), scope='DENSE'):
        super(Dense, self).__init__(None, scope)
        if axis == 0:
            raise Exception('NEBULAE ERROR ⨷ you cannot apply dense layer along batch axis.')
        else:
            self.axis = axis

        self.fc = layers.Dense(out_chs, use_bias=False if isinstance(b_init, Void) else True,
                               kernel_initializer=w_init.iniz, bias_initializer=b_init.iniz)

    def run(self, x):
        if self.axis == -1:
            y = self.fc(x)
        else:
            dim = x.ndim()
            permuted = [i for i in range(dim)]
            permuted = permuted[:self.axis] + permuted[self.axis + 1:] + [self.axis]
            x = x.transpose(*permuted)
            y = self.fc(x)
            permuted = [i for i in range(dim)]
            permuted = permuted[:self.axis] + [dim - 1] + permuted[self.axis:-1]
            y = y.transpose(*permuted)
        return y



class Embed(Craft):
    def __init__(self, ntoken, token_dim, scope='EMBED'):
        super(Embed, self).__init__(None, scope)
        self.embd = layers.Embedding(ntoken, token_dim)

    def run(self, x):
        y = self.embd(x)
        return y



class Identity(Craft):
    def __init__(self, scope='IDENTITY'):
        super(Identity, self).__init__(None, scope)

    def run(self, x):
        return x



# ---------------------------------- Manipulation ------------------------------------ #

class EMA(Craft):
    def __init__(self, hull, decay_fn=lambda x: 0.9, scope='EMA'):
        super(EMA, self).__init__(None, scope)
        self.counter = 0
        self.decay_fn = decay_fn
        self.hull = hull

        # initialize shadow as hull itself



# ----------------------------------- Mathmatic -------------------------------------- #

class Sqrt(Craft):
    def __init__(self, scope='SQRT'):
        super(Sqrt, self).__init__(None, scope)

    def run(self, t):
        y = tf.sqrt(t)
        return y



# ------------------------------------ Polyadic -------------------------------------- #

class Concat(Craft):
    def __init__(self, scope='CONCAT'):
        super(Concat, self).__init__(None, scope)

    def run(self, t, axis=-1):
        y = tf.concat(t, axis)
        return y



# ----------------------------------- Statistics ------------------------------------- #

class Clip(Craft):
    def __init__(self, intrinsic=False, scope='CLIP'):
        super(Clip, self).__init__(None, scope)
        if intrinsic:
            self.clipper = tfp.math.clip_by_value_preserve_gradient
        else:
            self.clipper = tf.clip_by_value

    def run(self, x, ranges):
        if isinstance(ranges, tuple):
            assert len(ranges)==2
        else:
            ranges = (-ranges, ranges)
        return self.clipper(x, *ranges)



class Mean(Craft):
    def __init__(self, scope='MEAN'):
        super(Mean, self).__init__(None, scope)

    def run(self, x, axis=None):
        if axis is None:
            y = tf.reduce_mean(x)
        else:
            y = tf.reduce_mean(x, axis=axis)
        return y



class Max(Craft):
    def __init__(self, scope='MAX'):
        super(Max, self).__init__(None, scope)

    def run(self, x, axis=None):
        if axis is None:
            y = tf.reduce_max(x)
        else:
            y = tf.reduce_max(x, axis=axis)
        return y



class Min(Craft):
    def __init__(self, scope='MIN'):
        super(Min, self).__init__(None, scope)

    def run(self, x, axis=None):
        if axis is None:
            y = tf.reduce_min(x)
        else:
            y = tf.reduce_min(x, axis=axis)
        return y



class Sum(Craft):
    def __init__(self, scope='SUM'):
        super(Sum, self).__init__(None, scope)

    def run(self, x, axis=None):
        if axis is None:
            y = tf.reduce_sum(x)
        else:
            y = tf.reduce_sum(x, axis=axis)
        return y



class MatMul(Craft):
    def __init__(self, scope='MATMUL'):
        super(MatMul, self).__init__(None, scope)

    def run(self, x, y, in_batch=False):
        z = x @ y
        return z


'''
class Grad(Craft):
    def __init__(self, scope='GRAD'):
        super(Grad, self).__init__(None, scope)

    def run(self, i, o):
        grad_out_weight = torch.ones((i.shape[0], 1), device=i.device)
        g = torch.autograd.grad(o, i, grad_outputs=grad_out_weight,
                                retain_graph=True, create_graph=True, only_inputs=True)
        return g


'''
# ------------------------------------- Resizer -------------------------------------- #

class Reshape(Craft):
    def __init__(self, scope='RESHAPE'):
        super(Reshape, self).__init__(None, scope)

    def run(self, x, shape):
        y = tf.reshape(x, shape)
        return y



class Permute(Craft):
    def __init__(self, scope='PERMUTE'):
        super(Permute, self).__init__(None, scope)

    def run(self, x, shape):
        y = tf.transpose(x, shape)
        return y



class Upscale(Craft):
    def __init__(self, scale: tuple, interp=NEAREST, scope='UPS'):
        super(Upscale, self).__init__(None, scope)
        dim = len(scale)
        if dim == 1:
            self.fn = layers.UpSampling1D(scale_factor=scale, mode=TF_INTERP[interp])
        elif dim == 2:
            self.fn = layers.UpSampling2D(scale_factor=scale, mode=TF_INTERP[interp])
        elif dim == 3:
            self.fn = layers.UpSampling3D(scale_factor=scale, mode=TF_INTERP[interp])
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d upscaling is not supported.' % dim)

    def run(self, x):
        y = self.fn(x)
        return y



class MaxPool(Craft):
    def __init__(self, kernel: tuple, stride=2, padding=0, scope='MPOOL'):
        super(MaxPool, self).__init__(None, scope)
        dim = len(kernel)
        is_global = True if kernel[-1] < 0 else False
        if dim == 1:
            if is_global:
                self.pool = layers.GlobalMaxPool1D()
            else:
                self.pool = layers.MaxPool1D(kernel, stride)
            pad_fn = layers.ZeroPadding1D
        elif dim == 2:
            if is_global:
                self.pool = layers.GlobalMaxPool2D()
            else:
                self.pool = layers.MaxPool2D(kernel, stride)
            pad_fn = layers.ZeroPadding2D
        elif dim == 3:
            if is_global:
                self.pool = layers.GlobalMaxPool3D()
            else:
                self.pool = layers.MaxPool3D(kernel, stride)
            pad_fn = layers.ZeroPadding3D
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d pooling is not supported.' % dim)

        if isinstance(padding, int):
            padding = dim * [[padding, padding]]
        elif isinstance(padding, (list, tuple)):
            padding = [(padding[2*d], padding[2*d+1]) for d in range(dim-1, -1, -1)]

        self.pad = pad_fn(padding)
        if is_global:
            assert padding == 0

    def run(self, x):
        y = self.pool(self.pad(x))
        return y



class AvgPool(Craft):
    def __init__(self, kernel: tuple, stride=2, padding=0, scope='APOOL'):
        super(AvgPool, self).__init__(None, scope)
        dim = len(kernel)
        is_global = True if kernel[-1]<0 else False
        if dim == 1:
            if is_global:
                self.pool = layers.GlobalAveragePooling1D()
            else:
                self.pool = layers.AveragePooling1D(kernel, stride)
            pad_fn = layers.ZeroPadding1D
        elif dim == 2:
            if is_global:
                self.pool = layers.GlobalAveragePooling2D()
            else:
                self.pool = layers.AveragePooling2D(kernel, stride)
            pad_fn = layers.ZeroPadding2D
        elif dim == 3:
            if is_global:
                self.pool = layers.GlobalAveragePooling3D()
            else:
                self.pool = layers.AveragePooling3D(kernel, stride)
            pad_fn = layers.ZeroPadding3D
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d pooling is not supported.' % dim)

        if isinstance(padding, int):
            padding = dim * [[padding, padding]]
        elif isinstance(padding, (list, tuple)):
            padding = [(padding[2*d], padding[2*d+1]) for d in range(dim-1, -1, -1)]

        self.pad = pad_fn(padding)
        if is_global:
            assert padding == 0

    def run(self, x):
        y = self.pool(self.pad(x))
        return y



# ------------------------------------ Activation ------------------------------------ #

class Relu(Craft):
    def __init__(self, scope='RELU'):
        super(Relu, self).__init__(None, scope)
        self.actv = layers.ReLU()

    def run(self, x):
        y = self.actv(x)
        return y



class LRelu(Craft):
    def __init__(self, alpha=0.2, scope='LRELU'):
        super(LRelu, self).__init__(None, scope)
        self.actv = layers.LeakyReLU(alpha)

    def run(self, x):
        y = self.actv(x)
        return y



class Tanh(Craft):
    def __init__(self, scope='TANH'):
        super(Tanh, self).__init__(None, scope)

    def run(self, x):
        y = tf.math.tanh(x)
        return y



class Sigm(Craft):
    def __init__(self, scope='SIGM'):
        super(Sigm, self).__init__(None, scope)

    def run(self, x):
        y = tf.math.sigmoid(x)
        return y



class Sftm(Craft):
    def __init__(self, axis=-1, scope='SFTM'):
        super(Sftm, self).__init__(None, scope)
        self.actv = layers.Softmax(axis)

    def run(self, x):
        y = self.actv(x)
        return y



class Sftp(Craft):
    def __init__(self, scope='SFTP'):
        super(Sftp, self).__init__(None, scope)

    def run(self, x):
        y = tf.math.softplus(x)
        return y



# ------------------------------------ Distributing ------------------------------------ #

class Dropout(Craft):
    def __init__(self, p_drop, dim, scope='DROPOUT'):
        super(Dropout, self).__init__(None, scope)
        self.dp = layers.Dropout(p_drop)

    def run(self, x):
        y = self.dp(x)
        return y



class BN(Craft):
    def __init__(self, out_chs, dim, mmnt=0.9, resilient=True, scope='BN'):
        super(BN, self).__init__(None, scope)
        self.norm = layers.BatchNormalization(1, momentum=mmnt, center=resilient, scale=resilient, epsilon=1e-5)

    def run(self, x):
        y = self.norm(x)
        return y


'''
class CBN(Craft):
    def __init__(self, in_chs, out_chs, dim, mmnt=0.9, scope='CBN'):
        super(CBN, self).__init__(None, scope)
        if dim == 1:
            norm_fn = nn.BatchNorm1d
        elif dim == 2:
            norm_fn = nn.BatchNorm2d
        elif dim == 3:
            norm_fn = nn.BatchNorm3d
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d CN is not supported.' % dim)
        self.norm = norm_fn(out_chs, momentum=1 - mmnt, affine=False, eps=1e-5)
        self.relu = nn.ReLU()
        self.gamma_1 = nn.Linear(in_chs, in_chs // 2)
        self.gamma_2 = nn.Linear(in_chs // 2, out_chs)
        self.beta_1 = nn.Linear(in_chs, in_chs // 2)
        self.beta_2 = nn.Linear(in_chs // 2, out_chs)

    def run(self, x, z):
        y = self.norm(x)

        g = self.gamma_1(z)
        g = self.relu(g)
        g = self.gamma_2(g)

        b = self.beta_1(z)
        b = self.relu(b)
        b = self.beta_2(b)

        for _ in range(x.ndim - 2):
            g = g.unsqueeze(-1)
            b = b.unsqueeze(-1)

        self.weight = g
        self.bias = b
        y = self.weight * y + self.bias

        return y



class IN(Craft):
    def __init__(self, out_chs, dim, mmnt=0.9, resilient=True, scope='IN'):
        super(IN, self).__init__(None, scope)
        if dim == 1:
            norm_fn = nn.InstanceNorm1d
        elif dim == 2:
            norm_fn = nn.InstanceNorm2d
        elif dim == 3:
            norm_fn = nn.InstanceNorm3d
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d IN is not supported.' % dim)
        self.norm = norm_fn(out_chs, momentum=1 - mmnt, affine=resilient, eps=1e-5)

    def run(self, x):
        y = self.norm(x)
        return y



class CIN(Craft):
    def __init__(self, in_chs, out_chs, dim, mmnt=0.9, scope='CIN'):
        super(CIN, self).__init__(None, scope)
        if dim == 1:
            norm_fn = nn.InstanceNorm1d
        elif dim == 2:
            norm_fn = nn.InstanceNorm2d
        elif dim == 3:
            norm_fn = nn.InstanceNorm3d
        else:
            raise Exception('NEBULAE ERROR ⨷ %d-d CN is not supported.' % dim)
        self.norm = norm_fn(out_chs, momentum=1 - mmnt, affine=False, eps=1e-5)
        self.relu = nn.ReLU()
        self.gamma_1 = nn.Linear(in_chs, in_chs // 2)
        self.gamma_2 = nn.Linear(in_chs // 2, out_chs)
        self.beta_1 = nn.Linear(in_chs, in_chs // 2)
        self.beta_2 = nn.Linear(in_chs // 2, out_chs)

    def run(self, x, z):
        y = self.norm(x)

        g = self.gamma_1(z)
        g = self.relu(g)
        g = self.gamma_2(g)

        b = self.beta_1(z)
        b = self.relu(b)
        b = self.beta_2(b)

        for _ in range(x.ndim - 2):
            g = g.unsqueeze(-1)
            b = b.unsqueeze(-1)

        self.weight = g
        self.bias = b
        y = self.weight * y + self.bias

        return y



class LN(Craft):
    def __init__(self, norm_shape, resilient=True, scope='LN'):
        super(LN, self).__init__(None, scope)
        norm_shape = tuple([norm_shape[-1]] + [ns for ns in norm_shape[:-1]])
        self.norm = nn.LayerNorm(norm_shape, elementwise_affine=resilient, eps=1e-5)

    def run(self, x):
        y = self.norm(x)
        return y



class SN(Craft):
    def __init__(self, craft, niter=3, eps=1e-12, scope='SN'):
        super(SN, self).__init__(None, scope)
        self.name = 'weight'
        if isinstance(craft, (Conv, TransConv)):
            self.key = 'conv/'
        elif isinstance(craft, Dense):
            self.key = 'fc/'
        elif isinstance(craft, Embed):
            self.key = 'embd/'
        elif isinstance(craft, (BN, IN, LN)):
            self.key = 'norm/'
        elif isinstance(craft, (CBN, CIN)):
            self.key = ''
        else:
            raise Exception('NEBULAE ERROR ⨷ SN does not support %s layer.' % type(craft))
        self.craft = craft
        self.hull = craft[self.key]
        self.niter = niter
        self.eps = eps
        if not self._made_params():
            self._make_params()

    def l2normalize(self, v):
        return v / (v.norm() + self.eps)

    def _update_u_v(self):
        if not self._made_params():
            self._make_params()
        w = getattr(self.hull, self.name)
        u = getattr(self.hull, self.name + "_u")

        height = w.data.shape[0]
        for _ in range(self.niter):
            v = self.l2normalize(torch.mv(torch.t(w.view(height, -1).data), u))
            u = self.l2normalize(torch.mv(w.view(height, -1).data, v))

        setattr(self.hull, self.name + "_u", u)
        w.data = w.data / torch.dot(u, torch.mv(w.view(height, -1).data, v))

    def _made_params(self):
        return hasattr(self.hull, self.name + "_u")

    def _make_params(self):
        w = getattr(self.hull, self.name)

        height = w.data.shape[0]
        width = w.view(height, -1).data.shape[1]

        u = self.l2normalize(w.data.new(height).normal_(0, 1))

        self.hull.register_buffer(self.name + "_u", u)

    def run(self, *args, **kwargs):
        self._update_u_v()
        return self.craft.run(*args, **kwargs)


'''
# ------------------------------------ Loss ------------------------------------ #

class MAE(Craft):
    def __init__(self, scope='MAE'):
        super(MAE, self).__init__(None, scope)
        self.cost = losses.MeanAbsoluteError()

    def run(self, x, y):
        z = self.cost(x, y)
        return z



class MSE(Craft):
    def __init__(self, scope='MAE'):
        super(MSE, self).__init__(None, scope)
        self.cost = losses.MeanSquaredError()

    def run(self, x, y):
        z = self.cost(x, y)
        return z



class SigmXE(Craft):
    def __init__(self, scope='SFTMXE'):
        super(SigmXE, self).__init__(None, scope)
        self.cost = losses.BinaryCrossentropy(from_logits=True)

    def run(self, x, y):
        z = self.cost(y, x)
        return z



class SftmXE(Craft):
    def __init__(self, is_one_hot, scope='SFTMXE'):
        super(SftmXE, self).__init__(None, scope)
        if is_one_hot:
            self.cost = losses.CategoricalCrossentropy(from_logits=True)
        else:
            self.cost = losses.SparseCategoricalCrossentropy(from_logits=True)

    def run(self, x, y):
        z = self.cost(y, x)
        return z



# ------------------------------------ Metric ------------------------------------ #

class AccCls(Craft):
    def __init__(self, multi_class, is_one_hot, scope='ACCCLS'):
        super(AccCls, self).__init__(None, scope)
        if multi_class:
            assert not is_one_hot
        self.mulcls = multi_class
        self.ioh = is_one_hot

    def run(self, x, y):
        data_type = x.dtype
        if self.mulcls: # include binary classification as well
            x = tf.round(x)
            correct = tf.reduce_mean(tf.cast(x == y, dtype=data_type), axis=-1)
            z = tf.reduce_mean(tf.cast(correct == 1, dtype=data_type))
        else:
            if self.ioh:
                y = tf.argmax(y, axis=-1)
            x = tf.argmax(x, axis=-1)
            z = tf.reduce_mean(tf.cast(x == y, dtype=data_type))
        return z


# ------------------------------------ Optimizer ------------------------------------ #

class StepLR(object):
    def __init__(self, period, factor):
        self.period = period
        self.factor = factor

    def __call__(self, lr):
        return optimizers.schedules.ExponentialDecay(lr, self.period, self.factor, staircase=True)



class PolyLR(object):
    def __init__(self, cutoff, power):
        self.cutoff = cutoff
        self.power = power

    def __call__(self, lr):
        return optimizers.schedules.PolynomialDecay(lr, self.cutoff, power=self.power)



class CosLR(object):
    def __init__(self, period):
        self.period = period

    def __call__(self, lr):
        return optimizers.schedules.CosineDecay(lr, self.period, lr * 0.001)



class ExpLR(object):
    def __init__(self, period, factor):
        self.period = period
        self.factor = factor

    def __call__(self, lr):
        return optimizers.schedules.ExponentialDecay(lr, self.period, self.factor)



class WavyLR(object):
    def __init__(self, period, dampen):
        self.period = period
        self.dampen = dampen

    def __call__(self, lr):
        return optimizers.schedules.CosineDecayRestarts(lr, self.period // 2, t_mul=1, m_mul=self.dampen)



class Momentum(Craft):
    def __init__(self, hull, lr, mmnt=0.9, wd=0, lr_decay=None,
                 grad_limit=-1, grad_accum=1, update_scope=None, scope='MOMENTUM'):
        super(Momentum, self).__init__(None, scope)
        self.hull = hull
        self.update_scope = update_scope
        self.grad_accum = grad_accum
        self.cnt = 0
        if grad_limit<0:
            grad_limit = None
        if lr_decay is not None:
            lr = lr_decay(lr)
        self.optz = optimizers.SGD(lr, momentum=mmnt, decay=wd, clipvalue=grad_limit)

    def _getVar(self):
        # select parameters await updating
        if self.update_scope is None:
            self.update_var = self.hull.trainable_weights
        else:
            if isinstance(self.update_scope, str):
                self.update_scope = [self.update_scope]
            self.update_var = []
            for us in self.update_scope:
                paths = us.split('/')
                craft = self.hull
                for p in paths:
                    craft = getattr(craft, p)
                self.update_var.extend(craft.trainable_weights)

    def run(self, target):
        if not hasattr(self, 'update_var'):
            self._getVar()
        curr_grads = self.hull._rudder.gradient(target, self.update_var)
        # curr_grads = [g if g is not None else tf.zeros_like(v) for g, v in zip(curr_grads, self.update_var)]
        if self.cnt == 0:
            self.grads = curr_grads
        else:
            self.grads = [self.grads[i] + curr_grads[i] for i in len(curr_grads)]
        self.cnt += 1
        if self.cnt == self.grad_accum:
            self.cnt = 0
            self.optz.apply_gradients(zip(self.grads, self.update_var))



class Nesterov(Craft):
    def __init__(self, hull, lr, mmnt=0.9, wd=0, lr_decay=None,
                 grad_limit=-1, grad_accum=1, update_scope=None, scope='NESTEROV'):
        super(Nesterov, self).__init__(None, scope)
        self.hull = hull
        self.update_scope = update_scope
        self.grad_accum = grad_accum
        self.cnt = 0
        if grad_limit < 0:
            grad_limit = None
        if lr_decay is not None:
            lr = lr_decay(lr)
        self.optz = optimizers.SGD(lr, momentum=mmnt, nesterov=True, decay=wd, clipvalue=grad_limit)

    def _getVar(self):
        # select parameters await updating
        if self.update_scope is None:
            self.update_var = self.hull.trainable_weights
        else:
            if isinstance(self.update_scope, str):
                self.update_scope = [self.update_scope]
            self.update_var = []
            for us in self.update_scope:
                paths = us.split('/')
                craft = self.hull
                for p in paths:
                    craft = getattr(craft, p)
                self.update_var.extend(craft.trainable_weights)

    def run(self, target):
        if not hasattr(self, 'update_var'):
            self._getVar()
        curr_grads = self.hull._rudder.gradient(target, self.update_var)
        if self.cnt == 0:
            self.grads = curr_grads
        else:
            self.grads = [self.grads[i] + curr_grads[i] for i in len(curr_grads)]
        self.cnt += 1
        if self.cnt == self.grad_accum:
            self.cnt = 0
            self.optz.apply_gradients(zip(self.grads, self.update_var))



class RMSProp(Craft):
    def __init__(self, hull, lr, mmnt=0., wd=0, lr_decay=None,
                 grad_limit=-1, grad_accum=1, update_scope=None, scope='RMSPROP'):
        super(RMSProp, self).__init__(None, scope)
        self.hull = hull
        self.update_scope = update_scope
        self.grad_accum = grad_accum
        self.cnt = 0
        if grad_limit < 0:
            grad_limit = None
        if lr_decay is not None:
            lr = lr_decay(lr)
        self.optz = optimizers.RMSprop(lr, momentum=mmnt, decay=wd, clipvalue=grad_limit)

    def _getVar(self):
        # select parameters await updating
        if self.update_scope is None:
            self.update_var = self.hull.trainable_weights
        else:
            if isinstance(self.update_scope, str):
                self.update_scope = [self.update_scope]
            self.update_var = []
            for us in self.update_scope:
                paths = us.split('/')
                craft = self.hull
                for p in paths:
                    craft = getattr(craft, p)
                self.update_var.extend(craft.trainable_weights)

    def run(self, target):
        if not hasattr(self, 'update_var'):
            self._getVar()
        curr_grads = self.hull._rudder.gradient(target, self.update_var)
        if self.cnt == 0:
            self.grads = curr_grads
        else:
            self.grads = [self.grads[i] + curr_grads[i] for i in len(curr_grads)]
        self.cnt += 1
        if self.cnt == self.grad_accum:
            self.cnt = 0
            self.optz.apply_gradients(zip(self.grads, self.update_var))



class Adam(Craft):
    def __init__(self, hull, lr, mmnt1=0.9, mmnt2=0.999, wd=0, lr_decay=None,
                 grad_limit=-1, grad_accum=1, update_scope=None, scope='ADAM'):
        super(Adam, self).__init__(None, scope)
        self.hull = hull
        self.update_scope = update_scope
        self.grad_accum = grad_accum
        self.cnt = 0
        if grad_limit < 0:
            grad_limit = None
        if lr_decay is not None:
            lr = lr_decay(lr)
        self.optz = optimizers.Adam(lr, beta_1=mmnt1, beta_2=mmnt2, decay=wd, clipvalue=grad_limit)

    def _getVar(self):
        # select parameters await updating
        if self.update_scope is None:
            self.update_var = self.hull.trainable_weights
        else:
            if isinstance(self.update_scope, str):
                self.update_scope = [self.update_scope]
            self.update_var = []
            for us in self.update_scope:
                paths = us.split('/')
                craft = self.hull
                for p in paths:
                    craft = getattr(craft, p)
                self.update_var.extend(craft.trainable_weights)

    def run(self, target):
        if not hasattr(self, 'update_var'):
            self._getVar()
        curr_grads = self.hull._rudder.gradient(target, self.update_var)
        if self.cnt == 0:
            self.grads = curr_grads
        else:
            self.grads = [self.grads[i] + curr_grads[i] for i in len(curr_grads)]
        self.cnt += 1
        if self.cnt == self.grad_accum:
            self.cnt = 0
            self.optz.apply_gradients(zip(self.grads, self.update_var))