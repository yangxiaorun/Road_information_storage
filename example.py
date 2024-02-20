from typing import Any, Dict, Iterator, List, Optional, Tuple, Union, Callable
import torch
from torch.library import Library, impl
import torch_npu
import torchair
from torchair.ge_concrete_graph.utils import dtype_promote
from torchair.ge_concrete_graph.fx2ge_converter import register_fx_node_ge_converter
from torchair.ge_concrete_graph.ge_graph import Tensor, TensorSpec
from torchair.ge_concrete_graph.ge_graph import get_default_ge_graph, next_unique_name
from torchair.ge_concrete_graph.ge_graph import compat_as_bytes, compat_as_bytes_list

# 为了演示，通过torch接口临时注册算子，注册namespace为"npu_define"
_lib = torch.library.Library("npu_define", "DEF") 
op_name = _lib.define("plug_in_op(Tensor input1, Tensor input2) -> Tensor")
m = Library("npu_define", "IMPL", "Meta")

def plug_in_op(
    input1: torch.Tensor,
    input2: torch.Tensor,
):
    out_tensor = input1 + input2
    return out_tensor


_lib.impl(op_name, plug_in_op, "PrivateUse1")


@impl(m, "plug_in_op")
def plug_in_op_meta(input1, input2):
    return torch.empty_like(input1)


def Custom_Add(x1: Tensor, x2: Tensor, *, dependencies=[], node_name=None):
    """REG_OP(Add)\n
.INPUT(x1, TensorType({DT_FLOAT, DT_INT32, DT_INT64, DT_FLOAT16, DT_BF16, DT_INT16, DT_INT8, DT_UINT8, DT_DOUBLE, DT_COMPLEX128, DT_COMPLEX64, DT_STRING}))\n
.INPUT(x2, TensorType({DT_FLOAT, DT_INT32, DT_INT64, DT_FLOAT16, DT_BF16, DT_INT16, DT_INT8, DT_UINT8, DT_DOUBLE, DT_COMPLEX128, DT_COMPLEX64, DT_STRING}))\n
.OUTPUT(y, TensorType({DT_FLOAT, DT_INT32, DT_INT64, DT_FLOAT16, DT_BF16, DT_INT16, DT_INT8, DT_UINT8, DT_DOUBLE, DT_COMPLEX128, DT_COMPLEX64, DT_STRING}))\n
"""

    op = get_default_ge_graph().op.add()
    op.type = "Add"
    op.name = next_unique_name(node_name, "Add")

    # process dependices
    for dependency in dependencies:
        op.input.append(dependency.controller)

    # process inputs
    op.input.append(x1.tensor)
    op.input_desc.add().CopyFrom(x1.desc)
    op.input_desc[-1].name = "x1"
    op.input.append(x2.tensor)
    op.input_desc.add().CopyFrom(x2.desc)
    op.input_desc[-1].name = "x2"

    # process attrs

    # process outputs
    output_index = 0
    op.output_desc.add().name = "y"
    y = Tensor(op, output_index)
    output_index += 1

    
    return y


@register_fx_node_ge_converter(torch.ops.npu_define.plug_in_op.default)
def conveter_plug_in_op(
        input1: Tensor,
        input2: Tensor,
        *,
        out: Tensor = None,
        meta_outputs: Any = None):
    input1, input2 = dtype_promote(input1, input2, target_dtype=meta_outputs.dtype)
    return Custom_Add(input1, input2)


###############################test########################################
class Plug_In_Add(torch.nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, input, output):
        return torch.ops.npu_define.plug_in_op(input, output)


def test_add():
    torch.npu.set_device(0)
    input1 = torch.arange(4).npu()
    input2 = torch.arange(4).npu()
    print("input1: ", input1)
    print("input2: ", input2)

    model = Plug_In_Add().npu()

    from torchair.core.utils import logger
    import logging
    from torchair.configs.compiler_config import CompilerConfig
    config = CompilerConfig()
    npu_backend = torchair.get_npu_backend(compiler_config=config)
    model = torch.compile(model, backend=npu_backend, dynamic=True)

    with torch.no_grad():
        output = model(input1, input2)

    print("output: ", output)


if __name__ == '__main__':
    test_add()
