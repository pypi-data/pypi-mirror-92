# QNQ -- QNQ's not quantization

version 1.0.0 2021.1.22

## Description

The toolkit is for Techart algorithm team to quantize their custom neural network's pretrained model.
The toolkit is beta now, you can contact me with email(dongz.cn@outlook.com) for adding ops and fixing bugs.

## How to install

`pip install qnq`

## How to use

This README.MD is in very early stages, and will be updated soon.
you can visit https://git.zwdong.com/zhiwei.dong/qnq_tutorial for more examples for QNQ.

1. Prepare your model.
   1. Check if your model contains non-class operator, like torch.matmul.
   2. If `True`, add `from qnq.operators.torchfunc_ops import *` to your code.
   3. Then use class replace non-class operator, you can refer fellow `#! add by dongz`

    ```python

    class BasicBlock(nn.Module):
        expansion = 1

        def __init__(self, inplanes, planes, stride=1, downsample=None):
            super(BasicBlock, self).__init__()
            self.conv1 = conv3x3(inplanes, planes, stride)
            self.bn1 = nn.BatchNorm2d(planes)
            self.relu1 = nn.ReLU(inplace=True)
            self.relu2 = nn.ReLU(inplace=True)
            self.conv2 = conv3x3(planes, planes)
            self.bn2 = nn.BatchNorm2d(planes)
            self.downsample = downsample
            self.stride = stride

            #! add by dongz
            self.torch_add = TorchAdd()

        def forward(self, x):
            identity = x

            out = self.conv1(x)
            out = self.bn1(out)
            out = self.relu1(out)

            out = self.conv2(out)
            out = self.bn2(out)

            if self.downsample is not None:
                identity = self.downsample(x)

            #! add by dongz
            out = self.torch_add(out, identity)
            # out += identity
            out = self.relu2(out)

            return out
    ```

2. Prepare 'metrics' and 'steper'.
   1. Choose at least 1k data to calibration your quantized model.
   2. 'metrics' inference without input params, return metrics value(a float number).
   3. 'steper' done inference and without input params too, but add quant.step(), and no return.
   4. Check qnq_tutorial for details.

3. Prepare pretrained checkpoints.
   1. Train your model and use `torch.save()` to save your checkpoints.
   2. Use `checkpoints = torch.load(checkpoints_path)` and `model.load_state_dict(checkpoints)` to load your checkpoints.

4. Quantize
   1. For code
      1. Add `from qnq import QNQ`
      2. Add `quant = QNQ(model, save_path, config_path, metrics, steper)`.
      3. Add `quant.search()`
   2. First run the program will exit, but the config_path will show a json file.
   3. Edit config.json and rerun for quantization.

## Operators supported

- Convolution Layers
  - Conv
  - ConvTranspose
- Pooling Layers
  - MaxPool
  - AveragePool
  - AdaptiveAvgPool
- Activation
  - Relu、Relu6
  - PRelu、LeakyRelu
  - LogSoftmax
- Normalization Layers
  - BatchNorm
  - LayerNorm
- Recurrent
  - LSTM
- Linear Layers
  - Linear
- Vision Layers
  - Upsample
  - Embedding
- Torch Function
  - Add, Sum, Minus, DotMul, MatMul, Div,
  - Sqrt, Exp
  - Sin, Cos
  - SoftMax, Sigmoid, Tanh
  - TorchTemplate, TorchDummy
