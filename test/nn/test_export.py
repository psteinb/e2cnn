import unittest
from unittest import TestCase

import e2cnn.nn.init as init
from e2cnn.nn import *
from e2cnn.gspaces import *

import torch
from torch.optim import SGD
from torch import nn

import numpy as np


class TestExport(TestCase):
    
    def test_R2Conv(self):
        
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            for ks in [1, 5]:
                for pd in [0, 1, 2]:
                    for st in [1, 2]:
                        for d in [1, 3]:
                            for gr in [1, 3]:
                                for i in range(2):
                                
                                    c_in = 1 + np.random.randint(4)
                                    c_out = 1 + np.random.randint(4)
                                    
                                    c_in *= gr
                                    c_out *= gr

                                    f_in = FieldType(gs, [gs.regular_repr]*c_in)
                                    f_out = FieldType(gs, [gs.regular_repr]*c_out)
                                    
                                    conv = R2Conv(
                                        f_in, f_out,
                                        kernel_size=ks,
                                        padding=pd,
                                        stride=st,
                                        dilation=d,
                                        groups=gr,
                                        bias=True,
                                    )
                                    
                                    self.check_exported(conv)

    def test_R2Conv_mix(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            gs.fibergroup._build_quotient_representations()
            for ks in [1, 5]:
                for pd in [0, 1, 2]:
                    for st in [1, 2]:
                        for d in [1, 3]:
                            
                            ft = FieldType(gs, list(gs.representations.values()))
                        
                            conv = R2Conv(
                                ft, ft,
                                kernel_size=ks,
                                padding=pd,
                                stride=st,
                                dilation=d,
                                groups=1,
                                bias=True,
                            )
                        
                            self.check_exported(conv)

    def test_R2ConvTransposed(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            for ks in [1, 5]:
                for pd in [0, 1, 2]:
                    for st in [1, 2]:
                        for d in [1, 3]:
                            for gr in [1, 3]:
                                for i in range(2):
                                    c_in = 1 + np.random.randint(4)
                                    c_out = 1 + np.random.randint(4)
                                
                                    c_in *= gr
                                    c_out *= gr
                                
                                    f_in = FieldType(gs, [gs.regular_repr] * c_in)
                                    f_out = FieldType(gs, [gs.regular_repr] * c_out)
                                
                                    conv = R2ConvTransposed(
                                        f_in, f_out,
                                        kernel_size=ks,
                                        padding=pd,
                                        stride=st,
                                        dilation=d,
                                        groups=gr,
                                        bias=True,
                                    )
                                
                                    self.check_exported(conv)

    def test_R2ConvTransposed_mix(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            gs.fibergroup._build_quotient_representations()
            for ks in [1, 5]:
                for pd in [0, 1, 2]:
                    for st in [1, 2]:
                        for d in [1, 3]:
                            ft = FieldType(gs, list(gs.representations.values()))
                        
                            conv = R2ConvTransposed(
                                ft, ft,
                                kernel_size=ks,
                                padding=pd,
                                stride=st,
                                dilation=d,
                                groups=1,
                                bias=True,
                            )
                        
                            self.check_exported(conv)

    def test_InnerBatchNorm(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            for i in range(4):
                c_in = 1 + np.random.randint(4)
            
                f_in = FieldType(gs, [gs.regular_repr] * c_in)
            
                batchnorm = InnerBatchNorm(f_in, affine=True)
                self.check_exported(batchnorm)
            
                batchnorm = InnerBatchNorm(f_in, affine=False)
                self.check_exported(batchnorm)

    def test_InnerBatchNorm_mix(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            gs.fibergroup._build_quotient_representations()
            reprs = [r for r in gs.representations.values() if 'pointwise' in r.supported_nonlinearities]
            
            f_in = FieldType(gs, reprs)
        
            batchnorm = InnerBatchNorm(f_in, affine=True)
            self.check_exported(batchnorm)
        
            batchnorm = InnerBatchNorm(f_in, affine=False)
            self.check_exported(batchnorm)

    def test_PointwiseDropout(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            for p in [1e-2, 1e-1, 5e-1, 8e-1]:
                for i in range(4):
                    c_in = 1 + np.random.randint(4)
                
                    f_in = FieldType(gs, [gs.regular_repr] * c_in)
                
                    relu = PointwiseDropout(f_in, p=p)
                    self.check_exported(relu)

    def test_R2Upsampling(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            for m in ['bilinear', 'nearest']:
                for sf in [1, 2, 4]:
                    for ac in [True, False]:
                        for i in range(3):
                        
                            f_in = FieldType(gs, list(gs.representations.values()))
                        
                            upsample = R2Upsampling(
                                f_in,
                                scale_factor=sf,
                                mode=m,
                                align_corners=ac
                            )
                            self.check_exported(upsample)

    def test_PointwiseAdaptiveAvgPool(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            for os in [1, 5, 11]:
                for i in range(3):
                    c_in = 1 + np.random.randint(4)
                
                    f_in = FieldType(gs, [gs.regular_repr] * c_in)
                
                    avgpool = PointwiseAdaptiveAvgPool(
                        f_in,
                        output_size=os
                    )
                    self.check_exported(avgpool)

    def test_PointwiseAdaptiveMaxPool(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            for os in [1, 5, 11]:
                for i in range(3):
                    c_in = 1 + np.random.randint(4)
                
                    f_in = FieldType(gs, [gs.regular_repr] * c_in)
                
                    maxpool = PointwiseAdaptiveMaxPool(
                        f_in,
                        output_size=os
                    )
                    self.check_exported(maxpool)

    def test_PointwiseMaxPool(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            for ks in [2, 3, 5]:
                for pd in range(min(ks-1, 2)):
                    for st in [1, 2]:
                        for d in [1, 3]:
                            for i in range(3):
                                c_in = 1 + np.random.randint(4)
                            
                                f_in = FieldType(gs, [gs.regular_repr] * c_in)
                            
                                maxpool = PointwiseMaxPool(
                                    f_in,
                                    kernel_size=ks,
                                    stride=st,
                                    padding=pd,
                                    dilation=d
                                )
                                self.check_exported(maxpool)

    def test_ReLU(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            for i in range(4):
                c_in = 1 + np.random.randint(4)
            
                f_in = FieldType(gs, [gs.regular_repr] * c_in)
            
                relu = ReLU(f_in)
                self.check_exported(relu)

    def test_ELU(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            for i in range(4):
                c_in = 1 + np.random.randint(4)
            
                f_in = FieldType(gs, [gs.regular_repr] * c_in)
            
                elu = ELU(f_in)
                self.check_exported(elu)

    def test_GPool_unique(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            gs.fibergroup._build_quotient_representations()
            for repr in gs.representations.values():
                if 'pointwise' in repr.supported_nonlinearities:
                
                    for i in range(4):
                        c_in = 1 + np.random.randint(8)
                    
                        f_in = FieldType(gs, [repr] * c_in)
                    
                        gpool = GroupPooling(f_in)
                        self.check_exported(gpool)

    def test_Sequential(self):
    
        for gs in [Rot2dOnR2(9), FlipRot2dOnR2(7), Flip2dOnR2(), TrivialOnR2()]:
            gs.fibergroup._build_quotient_representations()
            reprs = [r for r in gs.representations.values() if 'pointwise' in r.supported_nonlinearities]
    
            f_in = FieldType(gs, reprs)
            f_out = FieldType(gs, [gs.regular_repr]*1)
            
            for i in range(20):
                net = SequentialModule(
                    R2Conv(f_in, f_in, 7, bias=True),
                    InnerBatchNorm(f_in, affine=True),
                    ReLU(f_in, inplace=True),
                    PointwiseMaxPool(f_in, 3, 2, 1),
                    R2Conv(f_in, f_out, 3, bias=True),
                    InnerBatchNorm(f_out, affine=False),
                    ELU(f_out, inplace=True),
                    GroupPooling(f_out),
                )

                print(net)
                print(net.export())

                self.check_exported(net)

    def check_exported(self, equivariant: EquivariantModule):
    
        in_size = equivariant.in_type.size

        equivariant.train()
        
        if len(list(equivariant.parameters())) > 0:
            sgd = SGD(equivariant.parameters(), lr=1e-3)
        else:
            sgd = None
        
        for i in range(5):
            x = torch.randn(5, in_size, 31, 31)
            x = GeometricTensor(x, equivariant.in_type)
            
            if sgd is not None:
                sgd.zero_grad()
            
            y = equivariant(x).tensor
            y = ((y - 1.)**2).mean()
            
            if sgd is not None:
                y.backward()
                sgd.step()
        
        conventional = equivariant.export()
        
        for _ in range(5):
            x = torch.randn(5, in_size, 31, 31)

            ye = equivariant(GeometricTensor(x, equivariant.in_type)).tensor
            yc = conventional(x)
            
            # print(torch.abs(ye-yc).max())
            
            self.assertTrue(torch.allclose(ye, yc, atol=5e-7, rtol=5e-4))


if __name__ == '__main__':
    unittest.main()
