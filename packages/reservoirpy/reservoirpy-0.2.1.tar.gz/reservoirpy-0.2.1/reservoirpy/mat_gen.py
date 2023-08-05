"""Quick tools for weight matrices initialization.

This module provides simples tools for reservoir internal weights
and input/feedback weights initialization. Spectral radius of the
internal weights, input scaling and sparsity are fully parametrizable.

Because most of the architectures developped in *reservoir computing*
involve sparsely-connected neuronal units, the prefered format for all
generated matrices is a `scipy.sparse` format (in most cases *csr*).
Sparse arrays allow fast computations and compact representations of
weights matrices, and remains easily readable. They can be parsed back to
simple Numpy arrays just by calling their `toarray()`̀ method.

All functions can take as paramater a `numpy.random.RandomState`
instance, or a seed number, to ensure reproducibility. Both distribution
of weights and distribution of non-zero connections are controled with the
seed.

Example
-------

Here, we generate a 1000 units reservoir `W` with a spectral radius of 0.5,
connected to 5 inputs by the `W_in` matrix, with an input scaling of 0.9.

.. code-block:: python

    from reservoirpy.mat_gen import fast_spectral_initialization
    from reservoirpy.mat_gen import generate_input_weights
    W = fast_spectral_initialization(1000, spectral_radius=0.5)
    Win = generate_input_weights(1000, 5, input_scaling=0.9)
"""
from typing import Union

import numpy as np

from numpy.random import RandomState
from scipy import linalg
from scipy import sparse
from scipy.sparse.linalg import eigs

__all__ = [
    "fast_spectral_initialization",
    "generate_internal_weights",
    "generate_input_weights"
]


def _is_probability(proba):
    return 1. - proba >= 0. and proba >= 0.


def _get_random_state(seed):
    if isinstance(seed, RandomState):
        return seed
    else:
        return RandomState(seed)


def fast_spectral_initialization(N: int,
                                 spectral_radius: float = None,
                                 proba: float = 0.1,
                                 seed: Union[int, RandomState] = None,
                                 verbose: bool = False,
                                 sparsity_type: str = 'csr',
                                 typefloat=np.float64):
    """The fast spectral radius (FSI) approach for weights
    initialization introduced in [1].

    This method is well suited for computation and rescaling of
    very large weights matrices, with a number of neurons typically
    above 500-1000.

    Parameters
    ----------
    N : int
        Number of reservoir units, i.e. dimension of
        the square weights matrix.
    spectral_radius : float, optional
        Maximum desired eigenvalue of the
        reservoir weights matrix, by default None.
    proba : float, optional
        Probability of non zero connection,
        density of the weight matrix, by default 0.1
    seed : int or RandomState, optional
        Random state generator seed, for reproducibility,
        by default None
    verbose : bool, optional
    sparsity_type : {"csr", "csc", "coo"} optional
        Scipy sparse matrix format. "csr" by default.
    typefloat : np.dtype, optional

    Returns
    -------
    np.ndarray or scipy.sparse matrix
        A reservoir weights matrix.

    Raises
    ------
    ValueError
        Invalid non zero connection probability.

    References
    -----------

        [1] C. Gallicchio, A. Micheli, L. Pedrelli.
        Fast Spectral Radius Initialization for Recurrent
        Neural Networks. (2020)

    Example
    -------

        >>> from reservoirpy.mat_gen import fast_spectral_initialization
        >>> W = fast_spectral_initialization(5, proba=0.5, seed=42)
        >>> W.toarray()
        array([[ 0.13610996, -0.57035192,  0.        ,  0.        ,  0.        ],
               [ 0.26727631,  0.        , -0.22370579, -0.04951286,  0.        ],
               [ 0.60065244,  0.        , -0.02846888,  0.        ,  0.08786003],
               [ 0.        ,  0.39151551,  0.4157107 ,  0.        ,  0.41754172],
               [ 0.        ,  0.72101228,  0.        ,  0.        ,  0.        ]])
    """
    if not _is_probability(proba):
        raise ValueError(f"proba = {proba} not in [0; 1].")

    rs = _get_random_state(seed)

    if spectral_radius is None or proba == 0.:
        a = 1
    else:
        a = -(6 * spectral_radius) / (np.sqrt(12) * np.sqrt((proba * N)))

    if proba < 1:
        return sparse.random(N, N, density=proba,
                             random_state=rs, format=sparsity_type,
                             data_rvs=lambda s: rs.uniform(a, -a, size=s))

    else:
        return np.random.uniform(a, -a, size=(N, N))


def generate_internal_weights(N: int,
                              spectral_radius: float = None,
                              proba: float = 0.1,
                              Wstd: float = 1.0,
                              sparsity_type: str = 'csr',
                              seed: Union[int, RandomState] = None,
                              verbose: bool = False,
                              typefloat=np.float64):
    """Method that generate the weight matrix that will be used
    for the internal connections of the reservoir.

    Weights will follow a normal distribution of mean 0 and
    scale `Wstd` (by default 1), and can then be rescale to
    reach a specific spectral radius.

    Parameters
    ----------
    N : int
        Number of reservoir units, i.e. dimension of
        the square weights matrix.
    spectral_radius : float, optional
        Maximum desired eigenvalue of the
        reservoir weights matrix, by default None
    proba : float, optional
        Probability of non zero connection,
        density of the weight matrix, by default 0.1
    Wstd : float, optional
        Standard deviation of internal weights, by default 1.0
    sparsity_type : str, optional
        If set ot one of the scipy.sparse matrix format,
        will generate internal weights matrix in a sparse
        format, by default None
    seed : int or RandomState, optional
        Random state generator seed, for reproducibility,
        by default None
    verbose : bool, optional
    typefloat : numpy.dtype, optional

    Returns
    -------
    np.ndarray or scipy.sparse matrix
        A reservoir weights matrix.

    Raises
    ------
    ValueError
        Invalid non zero connection probability.

    Example
    -------

        >>> from reservoirpy.mat_gen import fast_spectral_initialization
        >>> W = generate_internal_weights(5, proba=0.5, seed=42)
        >>> W.toarray()
        array([[-1.72491783, -0.2257763 ,  0.        ,  0.        ,  0.        ],
               [-1.4123037 ,  0.        , -1.01283112, -1.91328024,  0.        ],
               [ 0.0675282 ,  0.        , -1.42474819,  0.        ,  1.46564877],
               [ 0.        ,  0.24196227, -0.90802408,  0.        , -0.56228753],
               [ 0.        ,  0.31424733,  0.        ,  0.        ,  0.        ]])
    """
    if not _is_probability(proba):
        raise ValueError(f"proba = {proba} not in [0; 1].")

    rs = _get_random_state(seed)

    if sparsity_type is not None:
        w = sparse.random(N, N, density=proba, format=sparsity_type,
                          random_state=rs,
                          data_rvs=lambda s: rs.normal(0, Wstd, size=s))
        rhoW = max(abs(eigs(w, k=1, which='LM', return_eigenvectors=False)))
    else:
        mask = 1 * (rs.rand(N, N) < proba)
        mat = rs.normal(0, Wstd, (N, N))
        w = np.multiply(mat, mask, dtype=typefloat)

        # Computing the spectral radius of W matrix
        rhoW = max(abs(linalg.eig(w)[0]))

    if verbose:
        print("Spectra radius of generated matrix before "
              "applying another spectral radius: " + str(rhoW))

    if spectral_radius is not None:
        w *= spectral_radius / rhoW
        if verbose:
            if sparse.issparse(w):
                rhoW_after = max(abs(sparse.linalg.eigs(w,
                                                        k=1,
                                                        which='LM',
                                                        return_eigenvectors=False)))
            else:
                rhoW_after = max(abs(linalg.eig(w)[0]))
            print("Spectra radius matrix after applying "
                  "another spectral radius: " + str(rhoW_after))

    return w


def generate_input_weights(N: int,
                           dim_input: int,
                           input_scaling: float = None,
                           proba: float = 0.1,
                           input_bias: bool = False,
                           seed: Union[int, RandomState] = None,
                           verbose: bool = False,
                           typefloat=np.float64):
    """
    Generate input or feedback weights for the reservoir.

    Weights are drawn from a discrete bimodal distribution,
    i.e. are always equal to 1 or -1. Then, they can be rescaled
    to a specific constant using the `input_scaling` parameter.

    Parameters
    ----------
        N: int
            Number of units in the connected reservoir.
        dim_input: int
            Dimension of the inputs connected to the reservoir.
        input_scaling: float, optional
            Constant value used to rescale the weights.
        input_bias: bool, optional
            If True, will add a row to the matrix to take into
            account a constant bias added to the input.
            Mandatory when using a :py:class:`reservoirpy.ESN` with
            `input_bias` set.
        proba: float, optional
            Probability of non-zero connections, density of
            the matrix, by default 0.1.
        seed : int or RandomState, optional
            Random state generator seed, for reproducibility,
            by default None
        verbose : bool, optional
        typefloat : numpy.dtype, optional
    Returns
    -------
    np.ndarray or scipy.sparse matrix
        A reservoir input or feedback weights matrix.

    Raises
    ------
    ValueError
        Invalid non zero connection probability.

    Example
    -------

        >>> from reservoirpy.mat_gen import generate_input_weights
        >>> Win = generate_input_weights(10, 2, input_scaling=2., proba=0.5, seed=42)
        >>> Win
        array([[-2., -0.],
               [ 0.,  0.],
               [ 2.,  2.],
               [ 2., -0.],
               [ 0.,  0.],
               [-2.,  0.],
               [-0.,  2.],
               [-2.,  2.],
               [ 2., -0.],
               [-2., -2.]])

    """
    if not _is_probability(proba):
        raise ValueError(f"proba = {proba} not in [0; 1].")

    rs = _get_random_state(seed)

    if input_bias:
        dim_input += 1
    mask = 1 * (rs.rand(N, dim_input) < proba)
    mat = rs.randint(0, 2, (N, dim_input)) * 2 - 1
    w = np.multiply(mat, mask, dtype=typefloat)
    if input_scaling is not None:
        w = input_scaling * w

    return w
