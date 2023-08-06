# -*- coding: utf-8 -*-
import numpy as np
from ..backend.torch.layer import create_tensor
from ..backend.torch.costfunctions import L1Cost, L2Cost, l1, l2, NegLogLikelihoodCost, DummyCost
from ..optim import is_optimizer_grad_based, InputWrapper
from ..costfunctions import CostFunction


def desc_to_dist(desc):
    """
    Converts a description of a distance metric into a `torch` function.

    Supported descriptions:

        - l1: l1-norm
        - l2: l2-norm

    Parameters
    ----------
    desc : `str`
        Description of the distance metric.
    
    Returns
    -------
    `callable`
        The distance function implemented as a `torch` function.
    
    Raises
    ------
    ValueError
        If `desc` contains an invalid description.
    """
    if desc == "l1":
        return l1
    elif desc == "l2":
        return l2
    else:
        raise ValueError(f"Invalid value of 'desc'.\n'desc' has to be 'l1' or 'l2' but not '{desc}'")


def desc_to_regcost(desc, x, input_wrapper):
    """
    Converts a description of a regularization into a `torch` function.

    Supported descriptions:

        - l1: l1-regularization
        - l2: l2-regularization

    Parameters
    ----------
    desc : `str`
        Description of the distance metric.
    x : `numpy.array`
        The original input from which we do not want to deviate much.
    input_wrapper : `callable`
        Converts the input (e.g. if we want to exclude some features/dimensions, we might have to include these missing features before applying any function to it).

        Is ignored!

    Returns
    -------
    `callable`
        The regularization function implemented as a `torch` function.
    
    Raises
    ------
    ValueError
        If `desc` contains an invalid description.
    """
    if desc == "l1":
        return L1Cost(x)
    elif desc == "l2":
        return L2Cost(x)
    else:
        raise ValueError(f"Invalid value of 'desc'.\n'desc' has to be 'l1' or 'l2' but not '{desc}'")


def build_regularization_loss(regularization, x, input_wrapper=None):
    """
    Builds a regularization loss.

    Parameters
    ----------
    desc : `str`, `callable` or None
        Description of the regularization, a callable regularization (not mandatory but we recommend to put your custom regularization into a class and make it a child of :class:`ceml.costfunctions.costfunctions.CostFunction` or  :class:`ceml.costfunctions.costfunctions.DifferentiableCostFunction` if your cost function is differentiable) or None if no regularization is desired.

        See :func:`ceml.torch.utils.desc_to_regcost` for a list of supported descriptions.

        If no regularization is requested, an instance of :class:`ceml.backend.torch.costfunctions.costfunctions.DummyCost` is returned. This cost function always outputs zero, no matter what the input is.
    x : `numpy.array`
        The original input from which we do not want to deviate much.
    input_wrapper : `callable`, optional
        Converts the input (e.g. if we want to exclude some features/dimensions, we might have to include these missing features before applying any function to it).

        If `input_wrapper` is None, input is passed without any modifications.

        The default is None.

    Returns
    -------
    `callable`
        An instance of :class:`ceml.costfunctions.costfunctions.CostFunction` or the user defined, callable, regularization.
    
    Raises
    ------
    TypeError
        If `regularization` has an invalid type.
    """
    if isinstance(regularization, str):
        return desc_to_regcost(regularization, x, input_wrapper)
    elif regularization is None:
        return DummyCost()
    elif not isinstance(regularization, CostFunction):
        raise TypeError("'regularization' has to be either an instance of CostFunction or a valid description of a supported regularization")
    else:
        return regularization


def features_whitelist_to_mask(features_whitelist, x, device):
    return np.array([1.0 if i in features_whitelist else 0.0 for i in range(x.shape[0])])


def wrap_input(features_whitelist, x, model, optimizer, device):
    input_wrapper = InputWrapper(features_whitelist, x)
    grad_based_solver = is_optimizer_grad_based(optimizer) if isinstance(optimizer, str) is True else True    # We assume that all PyTorch optimizers are gradient based optimizers
    grad_mask = features_whitelist_to_mask(features_whitelist, x, device) if grad_based_solver is True and features_whitelist is not None else None
    
    pred = model.predict
    x_orig = x
    if grad_based_solver is not True and features_whitelist is not None:
        pred = lambda z: model.predict(input_wrapper(z))
        x_orig = input_wrapper.extract_from(x)
    
    return input_wrapper, x_orig, pred, grad_mask
