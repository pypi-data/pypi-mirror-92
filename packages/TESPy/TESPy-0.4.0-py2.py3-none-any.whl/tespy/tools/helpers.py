# -*- coding: utf-8

"""Module for helper functions used by several other modules.

This file is part of project TESPy (github.com/oemof/tespy). It's copyrighted
by the contributors recorded in the version control history of the file,
available from its original location tespy/tools/helpers.py

SPDX-License-Identifier: MIT
"""
import logging
import os

import CoolProp as CP
import numpy as np

from tespy.tools.global_vars import err
from tespy.tools.global_vars import fluid_property_data
from tespy.tools.global_vars import molar_masses

# %%


class TESPyNetworkError(Exception):
    """Custom message for network related errors."""

    pass


class TESPyConnectionError(Exception):
    """Custom message for connection related errors."""

    pass


class TESPyComponentError(Exception):
    """Custom message for component related errors."""

    pass


def convert_to_SI(property, value, unit):
    r"""
    Convert a value to its SI value.

    Parameters
    ----------
    property : str
        Fluid property to convert.

    value : float
        Value to convert.

    unit : str
        Unit of the value.

    Returns
    -------
    SI_value : float
        Specified fluid property in SI value.
    """
    if property == 'T':
        converters = fluid_property_data['T']['units'][unit]
        return (value + converters[0]) * converters[1]

    elif property == 'Td_bp':
        return value * fluid_property_data['T']['units'][unit][1]

    else:
        return value * fluid_property_data[property]['units'][unit]


def convert_from_SI(property, SI_value, unit):
    r"""
    Get a value in the network's unit system from SI value.

    Parameters
    ----------
    property : str
        Fluid property to convert.

    SI_value : float
        SI value to convert.

    unit : str
        Unit of the value.

    Returns
    -------
    value : float
        Specified fluid property value in network's unit system.
    """
    if property == 'T':
        converters = fluid_property_data['T']['units'][unit]
        return SI_value / converters[1] - converters[0]

    elif property == 'Td_bp':
        return SI_value / fluid_property_data['T']['units'][unit][1]

    else:
        return SI_value / fluid_property_data[property]['units'][unit]


def latex_unit(unit):
    r"""
    Convert unit to LaTeX.

    Parameters
    ----------
    unit : str
        Value of unit for input, e.g. :code:`m3 / kg`.

    Returns
    -------
    unit : str
        Value of unit for output, e.g. :code:`$\unitfrac{m3}{kg}$`.
    """
    if '/' in unit:
        numerator = unit.split('/')[0].replace(' ', '')
        denominator = unit.split('/')[1].replace(' ', '')
        return r'$\unitfrac[]{' + numerator + '}{' + denominator + '}$'
    else:
        if unit == 'C':
            unit = r'^\circ C'
        return r'$\unit[]{' + unit + '}$'


def newton(func, deriv, params, y, **kwargs):
    r"""
    Find zero crossings with 1-D newton algorithm.

    Parameters
    ----------
    func : function
        Function to find zero crossing in,
        :math:`0=y-func\left(x,\text{params}\right)`.

    deriv : function
        First derivative of the function.

    params : list
        Additional parameters for function, optional.

    y : float
        Target function value.

    val0 : float
        Starting value, default: val0=300.

    valmin : float
        Lower value boundary, default: valmin=70.

    valmax : float
        Upper value boundary, default: valmax=3000.

    max_iter : int
        Maximum number of iterations, default: max_iter=10.

    tol_rel : float
        Maximum relative tolerance :math:`|\frac{y - f(x)}{f(x)}|`, default
        value: 1e-6.

    tol_abs : float
        Maximum absolute tolerance :math:`|y - f(x)|`, default value: 1e-6.

    tol_mode : str
        Check for relative, absolute or both tolerances:

        - :code:`tol_mode='abs'` (default)
        - :code:`tol_mode='rel'`
        - :code:`tol_mode='both'`

    Returns
    -------
    val : float
        x-value of zero crossing.

    Note
    ----
    Algorithm

    .. math::

        x_{i+1} = x_{i} - \frac{f(x_{i})}{\frac{df}{dx}(x_{i})}\\
        f(x_{i}) \leq \epsilon
    """
    # default valaues
    x = kwargs.get('val0', 300)
    valmin = kwargs.get('valmin', 70)
    valmax = kwargs.get('valmax', 3000)
    max_iter = kwargs.get('max_iter', 10)
    tol_rel = kwargs.get('tol_rel', err)
    tol_abs = kwargs.get('tol_abs', err)
    tol_mode = kwargs.get('tol_mode', 'abs')

    # start newton loop
    expr = True
    i = 0
    while expr:
        # calculate function residual and new value
        res = y - func(params, x)
        x += res / deriv(params, x)

        # check for value ranges
        if x < valmin:
            x = valmin
        if x > valmax:
            x = valmax
        i += 1

        if i > max_iter:
            msg = ('Newton algorithm was not able to find a feasible value '
                   'for function ' + str(func) + '. Current value with x=' +
                   str(x) + ' is ' + str(func(params, x)) +
                   ', target value is ' + str(y) + '.')
            logging.debug(msg)

            break
        if tol_mode == 'abs':
            expr = abs(res) >= tol_abs
        elif tol_mode == 'rel':
            expr = abs(res / y) >= tol_rel
        else:
            expr = abs(res / y) >= tol_rel or abs(res) >= tol_abs

    return x

# %%


def reverse_2d(params, y):
    r"""
    Calculate the residual value of an inverse function.

    Parameters
    ----------
    params : list
        Variable function parameters.

    y : float
        Function value of function :math:`y = f \left( x_1, x_2 \right)`.

    Returns
    -------
    deriv : float
        Residual value of inverse function :math:`x_2 - f\left(x_1, y \right)`.
    """
    func, x1, x2 = params[0], params[1], params[2]
    return x2 - func.ev(x1, y)


def reverse_2d_deriv(params, y):
    r"""
    Calculate derivative of an inverse function.

    Parameters
    ----------
    params : list
        Variable function parameters.

    y : float
        Function value of function :math:`y = f \left( x_1, x_2 \right)`,
        so that :math:`x_2 - f\left(x_1, y \right) = 0`

    Returns
    -------
    deriv : float
        Partial derivative :math:`\frac{\partial f}{\partial y}`.
    """
    func, x1 = params[0], params[1]
    return - func.ev(x1, y, dy=1)


def bus_char_evaluation(params, bus_value):
    r"""
    Calculate the value of a bus.

    Parameters
    ----------
    comp_value : float
        Value of the energy transfer at the component.

    reference_value : float
        Value of the bus in reference state.

    char_func : tespy.tools.characteristics.char_line
        Characteristic function of the bus.

    Returns
    -------
    residual : float
        Residual of the equation.

        .. math::

            residual = \dot{E}_\mathrm{bus} - \frac{\dot{E}_\mathrm{component}}
            {f\left(\frac{\dot{E}_\mathrm{bus}}
            {\dot{E}_\mathrm{bus,ref}}\right)}
    """
    comp_value = params[0]
    reference_value = params[1]
    char_func = params[2]
    return bus_value - comp_value / char_func.evaluate(
        bus_value / reference_value)


def bus_char_derivative(params, bus_value):
    """Calculate derivative for bus char evaluation."""
    reference_value = params[1]
    char_func = params[2]
    d = 1e-3
    return (1 - (
        1 / char_func.evaluate((bus_value + d) / reference_value) -
        1 / char_func.evaluate((bus_value - d) / reference_value)) / (2 * d))


def molar_mass_flow(flow):
    r"""
    Calculate molar mass flow.

    Parameters
    ----------
    flow : list
        Fluid property vector containing mass flow, pressure, enthalpy and
        fluid composition.

    Returns
    -------
    m_m : float
        Molar mass flow m_m / (mol/s).

        .. math::

            \dot{m}_\mathrm{m} = \sum_{i} \left( \frac{x_{i}}{M_{i}} \right)
    """
    mm = 0
    for fluid, x in flow.items():
        if x > err:
            mm += x / molar_masses[fluid]
    return mm

# %%


def num_fluids(fluids):
    r"""
    Return number of fluids in fluid mixture.

    Parameters
    ----------
    fluids : dict
        Fluid mass fractions.

    Returns
    -------
    n : int
        Number of fluids in fluid mixture n / 1.

        .. math::

            n = \sum_{i} \left( \begin{cases}
            0 & x_{i} < \epsilon \\
            1 & x_{i} \geq \epsilon
            \end{cases} \right)\;
            \forall i \in \text{network fluids}
    """
    n = 0
    for fluid, x in fluids.items():
        if x > err:
            n += 1

    return n

# %%


def single_fluid(fluids):
    r"""
    Return the name of the pure fluid in a fluid vector.

    Parameters
    ----------
    fluids : dict
        Fluid mass fractions.

    Returns
    -------
    fluid : str
        Name of the single fluid or None in case of mixtures.
    """
    if num_fluids(fluids) == 1:
        for fluid, x in fluids.items():
            if x > err:
                return fluid
    else:
        return None

# %%


def fluid_structure(fluid):
    r"""
    Return the checmical formula of fluid.

    Parameters
    ----------
    fluid : str
        Name of the fluid.

    Returns
    -------
    parts : dict
        Dictionary of the chemical base elements as keys and the number of
        atoms in a molecule as values.

    Example
    -------
    Get the chemical formula of methane.

    >>> from tespy.tools.helpers import fluid_structure
    >>> elements = fluid_structure('methane')
    >>> elements['C'], elements['H']
    (1, 4)
    """
    parts = {}
    for element in CP.CoolProp.get_fluid_param_string(
            fluid, 'formula').split('}'):
        if element != '':
            el = element.split('_{')
            parts[el[0]] = int(el[1])

    return parts

# %%


def darcy_friction_factor(re, ks, d):
    r"""
    Calculate the Darcy friction factor.

    Parameters
    ----------
    re : float
        Reynolds number re / 1.

    ks : float
        Pipe roughness ks / m.

    d : float
        Pipe diameter/characteristic lenght d / m.

    Returns
    -------
    darcy_friction_factor : float
        Darcy friction factor :math:`\lambda` / 1

    Note
    ----
    **Laminar flow** (:math:`re \leq 2320`)

    .. math::

        \lambda = \frac{64}{re}

    **turbulent flow** (:math:`re > 2320`)

    *hydraulically smooth:* :math:`\frac{re \cdot k_{s}}{d} < 65`

    .. math::

        \lambda = \begin{cases}
        0.03164 \cdot re^{-0.25} & re \leq 10^5\\
        \left(1.8 \cdot \log \left(re\right) -1.5 \right)^{-2} &
        10^5 < re < 5 \cdot 10^6\\
        solve \left(0 = 2 \cdot \log\left(re \cdot \sqrt{\lambda} \right) -0.8
        - \frac{1}{\sqrt{\lambda}}\right) & re \geq 5 \cdot 10^6\\
        \end{cases}

    *transition zone and hydraulically rough:*

    .. math::

        \lambda = solve \left( 0 = 2 \cdot \log \left( \frac{2.51}{re \cdot
        \sqrt{\lambda}} + \frac{k_{s}}{d \cdot 3.71} \right) -
        \frac{1}{\sqrt{\lambda}} \right)

    Reference: :cite:`Nirschl2018`.

    Example
    -------
    Calculate the Darcy friction factor at different hydraulic states.

    >>> from tespy.tools.helpers import darcy_friction_factor
    >>> ks = 5e-5
    >>> d = 0.05
    >>> re_laminar = 2000
    >>> re_turb_smooth = 20000
    >>> re_turb_trans = 70000
    >>> re_high = 1000000
    >>> d_high = 0.8
    >>> re_very_high = 6000000
    >>> d_very_high = 1
    >>> ks_low = 1e-5
    >>> ks_rough = 1e-3
    >>> darcy_friction_factor(re_laminar, ks, d)
    0.032
    >>> round(darcy_friction_factor(re_turb_smooth, ks, d), 3)
    0.027
    >>> round(darcy_friction_factor(re_turb_trans, ks, d), 3)
    0.023
    >>> round(darcy_friction_factor(re_turb_trans, ks_rough, d), 3)
    0.049
    >>> round(darcy_friction_factor(re_high, ks, d_high), 3)
    0.012
    >>> round(darcy_friction_factor(re_very_high, ks_low, d_very_high), 3)
    0.009
    """
    if re <= 2320:
        return 64 / re
    else:
        if re * ks / d < 65:
            if re <= 5e4:
                return blasius(re)
            elif re < 1e6:
                return hanakov(re)
            else:
                l0 = 0.02
                return newton(
                    prandtl_karman, prandtl_karman_derivative, [re],
                    0, val0=l0, valmin=0.00001, valmax=0.2)

        else:
            l0 = 0.002
            return newton(
                colebrook, colebrook_derivative, [re, ks, d], 0,
                val0=l0, valmin=0.0001, valmax=0.2)


def blasius(re):
    """
    Calculate friction coefficient according to Blasius.

    Parameters
    ----------
    re : float
        Reynolds number.

    Returns
    -------
    darcy_friction_factor : float
        Darcy friction factor.
    """
    return 0.3164 * re ** (-0.25)


def hanakov(re):
    """
    Calculate friction coefficient according to Hanakov.

    Parameters
    ----------
    re : float
        Reynolds number.

    Returns
    -------
    darcy_friction_factor : float
        Darcy friction factor.
    """
    return (1.8 * np.log10(re) - 1.5) ** (-2)


def prandtl_karman(params, darcy_friction_factor):
    """
    Calculate friction coefficient according to Prandtl and v. Kármán.

    Applied in smooth conditions.

    Parameters
    ----------
    re : float
        Reynolds number.

    darcy_friction_factor : float
        Darcy friction factor.

    Returns
    -------
    darcy_friction_factor : float
        Darcy friction factor.
    """
    re = params[0]
    return (
        2 * np.log10(re * darcy_friction_factor ** 0.5) - 0.8 -
        1 / darcy_friction_factor ** 0.5)


def prandtl_karman_derivative(params, darcy_friction_factor):
    """Calculate derivative for Prandtl and v. Kármán equation."""
    return (
        1 / (darcy_friction_factor * np.log(10)) +
        1 / 2 * darcy_friction_factor ** (-1.5))


def colebrook(params, darcy_friction_factor):
    """
    Calculate friction coefficient accroding to Colebrook-White equation.

    Applied in transition zone and rough conditions.

    Parameters
    ----------
    re : float
        Reynolds number.

    ks : float
        Equivalent sand roughness.

    d : float
        Pipe's diameter.

    darcy_friction_factor : float
        Darcy friction factor.

    Returns
    -------
    darcy_friction_factor : float
        Darcy friction factor.
    """
    re, ks, d = params[0], params[1], params[2]
    return (
        2 * np.log10(
            2.51 / (re * darcy_friction_factor ** 0.5) + ks / (3.71 * d)) +
        1 / darcy_friction_factor ** 0.5)


def colebrook_derivative(params, darcy_friction_factor):
    """Calculate derivative for Colebrook-White equation."""
    d = 0.001
    return (colebrook(params, darcy_friction_factor + d) -
            colebrook(params, darcy_friction_factor - d)) / (2 * d)

# %%


def modify_path_os(path):
    """
    Modify a path according the os.

    Also detects weather the path specification is absolute or relative and
    adjusts the path respectively.

    Parameters
    ----------
    path : str
        Path to modify.

    Returns
    -------
    path : str
        Modified path.
    """
    if os.name == 'nt':
        # windows
        path = path.replace('/', '\\')
        if path[0] != '\\' and path[1:2] != ':' and path[0] != '.':
            # relative path
            path = '.\\' + path
    else:
        # linux, mac
        path = path.replace('\\', '/')
        if path[0] != '/' and path[0] != '.':
            # relative path
            path = './' + path

    return path

# %%


def get_basic_path():
    """
    Return the basic tespy path and creates it if necessary.

    The basic path is the '.tespy' folder in the $HOME directory.
    """
    basicpath = os.path.join(os.path.expanduser('~'), '.tespy')
    if not os.path.isdir(basicpath):
        os.mkdir(basicpath)
    return basicpath


def extend_basic_path(subfolder):
    """
    Return a path based on the basic tespy path and creates it if necessary.

    The subfolder is the name of the path extension.
    """
    extended_path = os.path.join(get_basic_path(), subfolder)
    if not os.path.isdir(extended_path):
        os.mkdir(extended_path)
    return extended_path
