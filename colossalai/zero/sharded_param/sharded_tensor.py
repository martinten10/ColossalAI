import torch
from colossalai.zero.sharded_param.tensorful_state import StatefulTensor, TensorState
from typing import Optional


class ShardedTensor(StatefulTensor):

    def __init__(self, tensor: torch.Tensor, state: TensorState = TensorState.HOLD) -> None:
        r"""
        A tensor sharded in multiple processes. Constructed from an existing torch.Tensor instance.
        """
        super().__init__(tensor, state)

        # kept the shape, numel and dtype of the init tensor.
        self._origin_shape = tensor.shape
        self._origin_numel = tensor.numel()
        self._origin_dtype = tensor.dtype
        self._is_sharded = False

    @property
    def origin_numel(self) -> int:
        return self._origin_numel

    @property
    def origin_shape(self) -> int:
        return self._origin_shape

    @property
    def is_sharded(self):
        return self._is_sharded

    @is_sharded.setter
    def is_sharded(self, flag: bool):
        self._is_sharded = flag
