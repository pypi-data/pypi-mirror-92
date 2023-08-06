#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

# see https://esa.github.io/pygmo2/tutorials/coding_udi.html

import dask
import dask.array as da
import numpy as np
from distributed import Client
from pygmo import ipyparallel_bfe, mp_bfe, mp_island, problem
from typing_extensions import Protocol


class IslandUserDefined(Protocol):
    """Create a user defined Island."""

    def run_evolve(self, algo, pop) -> None:
        ...

    def get_name(self) -> str:
        ...


# TODO: Implement __setstate__, __getstate__ ??
# TODO: Implement __deepcopy__ ?
class IslandDask(IslandUserDefined):
    def __init__(self):
        # # Try to get an already existing `Client`
        # try:
        #     client = Client.current()  # type: Client
        # except ValueError:
        #     client = Client()
        #
        # self._client = client  # type: Client
        self._client = None

    def __repr__(self) -> str:
        cls_name = self.__class__.__name__  # type: str
        return f"{cls_name}<{self._client}>"

    def run_evolve(self, algo, pop):
        """Evolve population using Dask."""
        print("-- run_evolve")
        # This will be runned in Dask
        new_pop = algo.evolve(pop)
        # new_pop = self._client.map(algo.evolve, pop)

        return new_pop

    def get_name(self) -> str:
        # return f"Dask island with client: {self._client!r}"
        return "Dask island"


class BatchUserDefined(Protocol):
    """Create a batch user defined evaluator."""

    def __call__(self, prob: problem, dvs_1d: np.ndarray) -> np.ndarray:
        """Call operator.

        This method will evaluate in batch mode the fitness of the input decision vectors
        *dvs* using the fitness function for the optimization problem *prob*."""
        ...

    def get_extra_info(self) -> str:
        """Extra info for this evaluator."""
        ...

    def get_name(self) -> str:
        """Name of the evaluator."""
        ...


# TODO: Consider using a 'pygmo.member_bfe' and use the
#       method 'pygmo.problem.batch_fitness()' instead of __call__
class BatchFitnessEvaluatorDask:
    """Dask batch fitness evaluator.

    This user-defined batch fitness evaluator will dispatch the fitness evaluation
    in batch mode of a set of decision vectors to a `Dask` scheduler.
    """

    def __init__(self, chunk_size: int = 10):
        self._chunk_size = chunk_size  # type: int

    def __call__(self, prob: problem, dvs_1d: np.ndarray) -> np.ndarray:
        """Call operator.

        This method will evaluate in batch mode the fitness of the input decision vectors
        *dvs* using the fitness function for the optimization problem *prob*."""
        # Fetch the dimension and the fitness
        # dimension of the problem.
        ndim = prob.get_nx()  # Dimension of the problem
        nf = prob.get_nf()  # Dimension of the fitness

        # Convert the decision vectors (dvs) from a 1D numpy array of
        # shape (ndim * population_size,) a 2D dask array of
        # shape (ndim, population_size)
        dvs_2d = dvs_1d.reshape((ndim, -1))  # type: np.ndarray
        arr_2d = da.from_array(dvs_2d, chunks=(-1, self._chunk_size))  # type: da.Array

        # Create a function to compute the fitness
        def my_fitness(data_1d: np.ndarray, prob: problem = prob) -> np.ndarray:
            """Function to compute the fitness function.

            Notes
            -----
            Function `prob.fitness` is not serializable with `cloudpickle`.
            This function is *serializable* with `cloudpicke`.
            """
            return prob.fitness(data_1d)

        # Compute the fitness vectors as a 2D array
        # and get a new 2D array of size (population_size, nf)
        fvs_2d = da.apply_gufunc(
            my_fitness,
            "(i)->(k)",
            arr_2d.T,
            vectorize=True,
            output_sizes={"k": nf},
            output_dtypes=np.float,
        )  # type: da.Array

        # final_fvs_2d = fvs_2d.compute()  # type: np.ndarray
        final_fvs_2d = fvs_2d  # type: da.Array

        # Reshape it into a 1D array
        final_fvs_1d = final_fvs_2d.ravel()

        return final_fvs_1d

    def get_name(self):
        """Name of the evaluator."""
        return "Dask batch fitness evaluator."

    def get_extra_info(self):
        """Extra info for this evaluator."""
        scheduler = dask.config.config.get("scheduler")  # type: t.Optional[str]

        infos_dct = {
            "Chunk size": f"{self._chunk_size} elements",
            "Scheduler": scheduler,
        }
        infos_lst = ["    {key}: {value}" for key, value in infos_dct.items()]

        return "\n".join(["Extra info:", *infos_lst])
