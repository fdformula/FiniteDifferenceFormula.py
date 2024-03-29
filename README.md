# Finite Difference Formula Toolkit

Ported from a Julia package, https://github.com/fdformula/FiniteDifferenceFormula.jl, this
Python package provides a general and comprehensive toolkit for generating finite difference formulas, working with Taylor series expansions,
and teaching/learning finite difference formulas. It generates finite difference formulas
for derivatives of various orders by using Taylor series expansions of a function at evenly
spaced points. It also gives the truncation error of a formula in the big-O notation. We
can use it to generate new formulas in addition to verification of known ones. By changing
decimal places, we can also investigate how rounding errors may affect a result.

Beware, though formulas are mathematically correct, they may not be numerically useful.
This is true especially when we derive formulas for a derivative of higher order. For
example, run compute(9,range(-5, 6)), provided by this package, to generate a 10-point
central formula for the 9-th derivative. The formula is mathematically correct, but it
can hardly be put into use for numerical computing without, if possible, rewriting it
in a special way. Similarly, the more points are used, the more precise a formula
is mathematically. However, due to rounding errors, this may not be true numerically.

To run the code, you need the Python programming language (https://python.org/).

## How to install the package

In OS termial, execute the following command.

- python -m pip install FiniteDifferenceFormula

## The package exports a class, ```FDFormula```, ```fd``` (an object of the class), and the following member functions

```activatepythonfunction```, ```compute```, ```decimalplaces```, ```find```, ```findbackward```,
```findforward```, ```formula```, ```formulas```, ```loadcomputingresults```, ```taylor```,
```taylorcoefs```, ```tcofs```, ```truncationerror```, ```verifyformula```

### functions, ```compute```, ```find```, ```findforward```, and ```findbackward```

All take the same arguments (n, points, printformulaq = False).

#### Input

```
            n: the n-th order derivative to be found
       points: in the format of range(start, stop) or a list
printformulaq: print the computed formula or not
```

|   points       |   The points/nodes to be used                  |
| -------------- | ---------------------------------------------- |
|  range(0,3)    |   x[i], x[i+1], x[i+2]                         |
|  range(-3, 3)  |   x[i-3], x[i-2], x[i-1], x[i], x[i+1], x[i+2] |
|  [1, 0, 1, -1] |   x[i-1], x[i], x[i+1]                         |

A list of points will be rearranged so that elements are ordered
from lowest to highest with duplicate ones removed.

#### Output

Each function returns a tuple, (n, points, k[:], m), where n, points, k[:] and m are described below.
With the information, you may generate functions for any programming language of your choice.

While 'compute' may fail to find a formula using the points, others try to find one, if possible,
by using fewer points in different ways. (See the docstring of each function.)

The algorithm uses the linear combination of f(x[i+j]) = f(x[i] + jh), where h is the increment
in x and j ∈ points, to eliminate f(x[i]), f'(x[i]), f''(x[i]), ..., so that the first nonzero
term of the Taylor series of the linear combination is f^(n)(x[i]).

```Python
k[1]*f(x[i+points[1]]) + k[2]*f(x[i+points[2]]) + ... + k[L]*f(x[i+points[L]]) = m*f^(n)(x[i]) + ..., m > 0
```

where L = len(points) - 1. It is this equation that gives the formula for computing f^(n)(x[i])
and the truncation error in the big-O notation as well.

### function ```loadcomputingresults```(results)

The function loads results, a tuple of the form (n, points, k, m), returned by ```compute```.
For example, it may take hours to compute/find formulas invloving hundreds of points. In this
case, we can save the results in a text file and come back later to work on the results
with ```activatepythonfunction```, ```formula```, ```truncationerror```, and so on.

### function ```formula```()

The function generates and lists

1. k[0]\*f(x[i+points[0]]) + k[1]\*f(x[i+points[1]]) + ... + k[L]\*f(x[i+points[L]])
= m\*f^(n)(x[i]) + ..., where m > 0, L = length(points) - 1

1. The formula for f^(n)(x[i]), including estimation of accuracy in the big-O notation.

1. "Python" function(s) for f^(n)(x[i]).

### function ```truncationerror```()

The function returns a tuple, (n, "O(h^n)"), the truncation error of the newly computed finite
difference formula in the big-O notation.

### function ```decimalplaces```(n = 16)

The function sets to n the decimal places for generating Python function(s) for formulas. It
returns the (new) decimal places. Note: Passing to it a negative integer will return th
present decimal places (without making any changes).

This function can only affect Python functions with the suffix "d" such as f1stderiv2ptcentrald.
See function activatepythonfunction().

### function ```activatepythonfunction```()

Call this function to activate the Python function(s) for the newly computed finite
difference formula. For example, after compute(1, [-1, 0, 1]) and decimalplaces(4), it activates the
following Python functions.

```Python
fde(f, x, i, h)  = ( -f(x[i-1]) + f(x[i+1]) ) / (2 * h)             # i.e., f1stderiv2ptcentrale
fde1(f, x, i, h) = ( -1/2 * f(x[i-1]) + 1/2 * f(x[i+1]) ) / h       # i.e., f1stderiv2ptcentrale1
fdd(f, x, i, h)  = ( -0.5000 * f(x[i-1]) + 0.5000 * f(x[i+1]) ) / h # i.e., f1stderiv2ptcentrald
```
The suffixes 'e' and 'd' stand for 'exact' and 'decimal', respectively. No suffix? It is "exact".
After activating the function(s), we can evaluate right away in the present Python REPL session. For example,

```Python
fd.compute(1, range(-10,9))
fd.activatepythonfunction()
fd.fde(sin, [ 0.01*i for i in range(0, 1000)], 501, 0.01)
```
Below is the output of activatepythonfunction(). It gives us the first chance to examine the usability
of the computed or tested formula.

```Python
f, x, i, h = sin, [ 0.01*i for i in range(0, 1000) ], 501, 0.01
fd.fde(f, x, i, h)   # result: 0.2836574577837647, relative error = 0.00166666%
fd.fde1(f, x, i, h)  # result: 0.2836574577837647, relative error = 0.00166666%
fd.fdd(f, x, i, h)   # result: 0.2836574577837647, relative error = 0.00166666%
                     # cp:     0.2836621854632262
```

### function ```verifyformula```(n, points, k, m)

It allows users to load a formula from some source to test and see if it is correct. If it is valid,
its truncation error in the big-O notation can be determined. Furthermore, if the input data is not
for a valid formula, it tries also to find one, if possible, using n and points.

Here, n is the order of a derivative, points are a list of points, k is a list of the corresponding
coefficients of a formula, and m is the coefficient of the term f^(n)(x[i]) in the linear
combination of f(x[i+j]), where j ∈ points. In general, m is the coefficient of h^n in the
denominator of a formula. For example,

```Python
fd.verifyformula(2, [-1, 0, 2, 3, 6], [12, 21, 2, -3, -9], -12)
fd.truncationerror()
fd.verifyformula(4, [0, 1, 2, 3, 4], [2/5, -8/5, 12/5, -8/3, 2/5], 5)
fd.verifyformula(2, [-1, 2, 0, 2, 3, 6], [1.257, 21.16, 2.01, -3.123, -9.5], -12)
```

### function ```taylorcoefs```(j, n = 10) or ```tcoefs```(j, n = 10)

The function returns the coefficients of the first n terms of the Taylor series of f(x[i+j])
about x[i].

### function ```taylor```(j, n = 10)

The function prints the first n terms of the Taylor series of f(x[i+j]) about x[i].

### function ```taylor```(coefficients_of_taylor_series, n = 10)

The function prints the first n nonzero terms of a Taylor series of which the coefficients are
provided.

### function ```taylor```((points, k), n = 10)

The function prints the first n nonzero terms of a Taylor series of which the linear combination
of k[0]f(x[i+points[0]]) + k[1]f(x[i+points[1]]) + ... + k[L]f(x[i+points[L]]), where L = len(points).

### function ```formulas```(orders = [1, 2, 3], min_num_of_points = 2, max_num_of_points = 5)

By default, the function prints all forward, backward, and central finite difference formulas for
the 1st, 2nd, and 3rd derivatives, using 2 to 5 points.

## Examples

```Python
from FiniteDifferenceFormula import fd
fd.compute(1, range(0,3), True)        # find, generate, and print "3"-point forward formula for f'(x[i])
fd.compute(2, range(-3,1), True)       # find, generate, and print "4"-point backward formula for f''(x[i])
fd.compute(3, range(-9,10))            # find "19"-point central formula for f'''(x[i])
fd.decimalplaces(6)                    # use 6 decimal places to generate Python functions of computed formulas
fd.compute(2, [-3, -2, 1, 2, 7])       # find formula for f''(x[i]) using points x[i+j], j = -3, -2, 1, 2, and 7
fd.compute(1, range(-230, 231))        # find "461"-point central formula for f'(x[i]). does it exist? run the code!
fd.formula()                           # generate and print the formula computed last time you called compute(...)
fd.truncationerror()                   # print and return the truncation error of the newly computed formula
fd.taylor(-2, 50)                      # print the first 50 terms of the Taylor series of f(x[i-2]) about x[i]

import numpy as np
coefs  = -2 * np.array(fd.tcoefs(1)) + 3 * np.array(fd.tcoefs(2)) - 4 * np.array(fd.tcoefs(5))
fd.taylor(list(coefs), 9)              # print the first 9 nonzero terms of the Taylor series of -2f(x[i+1) + 3f(x[i+2]) - 4f(x[i+5])

fd.taylor(([1, 2, 5], [-2, 3, -4]), 9) # same as above

fd.activatepythonfunction()            # activate Python function(s) of the newly computed formula in present REPL session
fd.verifyformula(1, [2,3], [-4, 5], 6) # verify if f'(x[i]) = (-4f(x[i+2] + 5f(x[i+3)) / (6h) is a valid formula
fd.formulas(2, 5, 9)                   # print all forward, backword, and central formulas for the 2nd derivative, using 5 to 9 points
fd.formulas([2, 4], 5, 9)              # print all forward, backword, and central formulas for the 2nd and 4th derivatives, using 5 to 9 points
```
