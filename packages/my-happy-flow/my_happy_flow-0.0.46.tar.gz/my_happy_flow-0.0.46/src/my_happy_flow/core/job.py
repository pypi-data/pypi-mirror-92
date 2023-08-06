import uuid
import inspect

from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Set,
    Tuple,
    cast,
    Union,
)

class Job:
    """
    Abstract class to be derived for jobs. It provides the `run()` method to execute 
    a collection of dependent tasks(ray.remote) by using the ray.get method.

    Args:
        - name (str): The name of the flow. Cannot be `None` or an empty string
    """
    def __init__(
        self,
        name: str
    ):
        if not name:
            raise ValueError("A name must be provided for the job.")

        self.name = name
        self.id = str(uuid.uuid4())

    def run(
        self,
    ) -> Any:
        """
         The `run()` method is called to run a job.
        """

    def visualize(
        self,
        filename: str = None,
        format: str = None,
    ) -> Any:
        run_method_source_code: str = inspect.getsource(self.run)
        return run_method_source_code
        

    