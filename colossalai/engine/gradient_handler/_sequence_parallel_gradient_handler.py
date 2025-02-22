from colossalai.core import global_context as gpc
from colossalai.registry import GRADIENT_HANDLER
from ._base_gradient_handler import BaseGradientHandler
from ...context.parallel_mode import ParallelMode
from .utils import bucket_allreduce


@GRADIENT_HANDLER.register_module
class SequenceParallelGradientHandler(BaseGradientHandler):
    """A helper class to handle all-reduce operations in a data parallel group.
    A all-reduce collective communication will be operated in 
    :func:`handle_gradient` among a data parallel group.
    For better performance, it bucketizes the gradients of all parameters that are 
    the same type to improve the efficiency of communication.
    """

    def handle_gradient(self):
        """A method running a all-reduce operation in a data parallel group.
        """
        if gpc.get_world_size(ParallelMode.SEQUENCE_DP) > 1:
            bucket_allreduce(param_list=self._model.parameters(), group=gpc.get_group(ParallelMode.SEQUENCE_DP))
