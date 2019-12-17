# -*- coding: utf-8 -*-


# numpy funktionen
# see https://docs.scipy.org/doc/numpy/reference/ufuncs.html

import FreeCAD
from FreeCAD import Vector as MVector

#from nodeeditor.wrapper import MVector # as Vector

import numpy as np
from nodeeditor.say import *
import nodeeditor.store as store

class Array(object):
    def __init__(self,dat=[]):
        self.dat=np.array(dat)

from PyFlow.Core import(
    FunctionLibraryBase,
    IMPLEMENT_NODE
)
from PyFlow.Core.Common import *

class Numpy(FunctionLibraryBase):
    '''doc string for Vector'''
    def __init__(self,packageName):
        super(Numpy, self).__init__(packageName)



    '''
    Math operations
    add(x1, x2, /[, out, where, casting, order, …])     Add arguments element-wise.
    subtract(x1, x2, /[, out, where, casting, …])   Subtract arguments, element-wise.
    multiply(x1, x2, /[, out, where, casting, …])   Multiply arguments element-wise.
    divide(x1, x2, /[, out, where, casting, …])     Returns a true division of the inputs, element-wise.
    logaddexp(x1, x2, /[, out, where, casting, …])  Logarithm of the sum of exponentiations of the inputs.
    logaddexp2(x1, x2, /[, out, where, casting, …])     Logarithm of the sum of exponentiations of the inputs in base-2.
    true_divide(x1, x2, /[, out, where, …])     Returns a true division of the inputs, element-wise.
    floor_divide(x1, x2, /[, out, where, …])    Return the largest integer smaller or equal to the division of the inputs.
    negative(x, /[, out, where, casting, order, …])     Numerical negative, element-wise.
    positive(x, /[, out, where, casting, order, …])     Numerical positive, element-wise.
    power(x1, x2, /[, out, where, casting, …])  First array elements raised to powers from second array, element-wise.
    remainder(x1, x2, /[, out, where, casting, …])  Return element-wise remainder of division.
    mod(x1, x2, /[, out, where, casting, order, …])     Return element-wise remainder of division.
    fmod(x1, x2, /[, out, where, casting, …])   Return the element-wise remainder of division.
    divmod(x1, x2[, out1, out2], / [[, out, …])     Return element-wise quotient and remainder simultaneously.
    absolute(x, /[, out, where, casting, order, …])     Calculate the absolute value element-wise.
    fabs(x, /[, out, where, casting, order, …])     Compute the absolute values element-wise.
    rint(x, /[, out, where, casting, order, …])     Round elements of the array to the nearest integer.
    sign(x, /[, out, where, casting, order, …])     Returns an element-wise indication of the sign of a number.
    heaviside(x1, x2, /[, out, where, casting, …])  Compute the Heaviside step function.
    conj(x, /[, out, where, casting, order, …])     Return the complex conjugate, element-wise.
    exp(x, /[, out, where, casting, order, …])  Calculate the exponential of all elements in the input array.
    exp2(x, /[, out, where, casting, order, …])     Calculate 2**p for all p in the input array.
    log(x, /[, out, where, casting, order, …])  Natural logarithm, element-wise.
    log2(x, /[, out, where, casting, order, …])     Base-2 logarithm of x.
    log10(x, /[, out, where, casting, order, …])    Return the base 10 logarithm of the input array, element-wise.
    expm1(x, /[, out, where, casting, order, …])    Calculate exp(x) - 1 for all elements in the array.
    log1p(x, /[, out, where, casting, order, …])    Return the natural logarithm of one plus the input array, element-wise.
    sqrt(x, /[, out, where, casting, order, …])     Return the non-negative square-root of an array, element-wise.
    square(x, /[, out, where, casting, order, …])   Return the element-wise square of the input.
    cbrt(x, /[, out, where, casting, order, …])     Return the cube-root of an array, element-wise.
    reciprocal(x, /[, out, where, casting, …])  Return the reciprocal of the argument, element-wise.
    gcd(x1, x2, /[, out, where, casting, order, …])     Returns the greatest common divisor of |x1| and |x2|
    lcm(x1, x2, /[, out, where, casting, order, …])     Returns the lowest common multiple of |x1| and |x2|'
    '''


    '''
    Trigonometric functions

    All trigonometric functions use radians when an angle is called for. The ratio of degrees to radians is 180^{\circ}/\pi.
    sin(x, /[, out, where, casting, order, …])  Trigonometric sine, element-wise.
    cos(x, /[, out, where, casting, order, …])  Cosine element-wise.
    tan(x, /[, out, where, casting, order, …])  Compute tangent element-wise.
    arcsin(x, /[, out, where, casting, order, …])   Inverse sine, element-wise.
    arccos(x, /[, out, where, casting, order, …])   Trigonometric inverse cosine, element-wise.
    arctan(x, /[, out, where, casting, order, …])   Trigonometric inverse tangent, element-wise.
    arctan2(x1, x2, /[, out, where, casting, …])    Element-wise arc tangent of x1/x2 choosing the quadrant correctly.
    hypot(x1, x2, /[, out, where, casting, …])  Given the “legs” of a right triangle, return its hypotenuse.
    sinh(x, /[, out, where, casting, order, …])     Hyperbolic sine, element-wise.
    cosh(x, /[, out, where, casting, order, …])     Hyperbolic cosine, element-wise.
    tanh(x, /[, out, where, casting, order, …])     Compute hyperbolic tangent element-wise.
    arcsinh(x, /[, out, where, casting, order, …])  Inverse hyperbolic sine element-wise.
    arccosh(x, /[, out, where, casting, order, …])  Inverse hyperbolic cosine, element-wise.
    arctanh(x, /[, out, where, casting, order, …])  Inverse hyperbolic tangent element-wise.
    deg2rad(x, /[, out, where, casting, order, …])  Convert angles from degrees to radians.
    rad2deg(x, /[, out, where, casting, order, …])  Convert angles from radians to degrees.
    Bit-twiddling functions

    These function all require integer arguments and they manipulate the bit-pattern of those arguments.
    bitwise_and(x1, x2, /[, out, where, …])     Compute the bit-wise AND of two arrays element-wise.
    bitwise_or(x1, x2, /[, out, where, casting, …])     Compute the bit-wise OR of two arrays element-wise.
    bitwise_xor(x1, x2, /[, out, where, …])     Compute the bit-wise XOR of two arrays element-wise.
    invert(x, /[, out, where, casting, order, …])   Compute bit-wise inversion, or bit-wise NOT, element-wise.
    left_shift(x1, x2, /[, out, where, casting, …])     Shift the bits of an integer to the left.
    right_shift(x1, x2, /[, out, where, …])     Shift the bits of an integer to the right.
    Comparison functions
    greater(x1, x2, /[, out, where, casting, …])    Return the truth value of (x1 > x2) element-wise.
    greater_equal(x1, x2, /[, out, where, …])   Return the truth value of (x1 >= x2) element-wise.
    less(x1, x2, /[, out, where, casting, …])   Return the truth value of (x1 < x2) element-wise.
    less_equal(x1, x2, /[, out, where, casting, …])     Return the truth value of (x1 =< x2) element-wise.
    not_equal(x1, x2, /[, out, where, casting, …])  Return (x1 != x2) element-wise.
    equal(x1, x2, /[, out, where, casting, …])  Return (x1 == x2) element-wise.

    Warning

    Do not use the Python keywords and and or to combine logical array expressions. These keywords will test the truth value of the entire array (not element-by-element as you might expect). Use the bitwise operators & and | instead.

    logical_and(x1, x2, /[, out, where, …])     Compute the truth value of x1 AND x2 element-wise.
    logical_or(x1, x2, /[, out, where, casting, …])     Compute the truth value of x1 OR x2 element-wise.
    logical_xor(x1, x2, /[, out, where, …])     Compute the truth value of x1 XOR x2, element-wise.
    logical_not(x, /[, out, where, casting, …])     Compute the truth value of NOT x element-wise.


    maximum(x1, x2, /[, out, where, casting, …])    Element-wise maximum of array elements.
    minimum(x1, x2, /[, out, where, casting, …])    Element-wise minimum of array elements.



    Floating functions

    Recall that all of these functions work element-by-element over an array, returning an array output. The description details only a single operation.
    isfinite(x, /[, out, where, casting, order, …])     Test element-wise for finiteness (not infinity or not Not a Number).
    isinf(x, /[, out, where, casting, order, …])    Test element-wise for positive or negative infinity.
    isnan(x, /[, out, where, casting, order, …])    Test element-wise for NaN and return result as a boolean array.
    isnat(x, /[, out, where, casting, order, …])    Test element-wise for NaT (not a time) and return result as a boolean array.
    fabs(x, /[, out, where, casting, order, …])     Compute the absolute values element-wise.
    signbit(x, /[, out, where, casting, order, …])  Returns element-wise True where signbit is set (less than zero).
    copysign(x1, x2, /[, out, where, casting, …])   Change the sign of x1 to that of x2, element-wise.
    nextafter(x1, x2, /[, out, where, casting, …])  Return the next floating-point value after x1 towards x2, element-wise.
    spacing(x, /[, out, where, casting, order, …])  Return the distance between x and the nearest adjacent number.
    modf(x[, out1, out2], / [[, out, where, …])     Return the fractional and integral parts of an array, element-wise.
    ldexp(x1, x2, /[, out, where, casting, …])  Returns x1 * 2**x2, element-wise.
    frexp(x[, out1, out2], / [[, out, where, …])    Decompose the elements of x into mantissa and twos exponent.
    fmod(x1, x2, /[, out, where, casting, …])   Return the element-wise remainder of division.
    floor(x, /[, out, where, casting, order, …])    Return the floor of the input, element-wise.
    ceil(x, /[, out, where, casting, order, …])     Return the ceiling of the input, element-wise.
    trunc(x, /[, out, where, casting, order, …])    Return the truncated value of the input, element-wise.


    Linear algebra (numpy.linalg)
    Matrix and vector products

    dot(a, b[, out])    Dot product of two arrays.
    linalg.multi_dot(arrays)    Compute the dot product of two or more arrays in a single function call, while automatically selecting the fastest evaluation order.
    vdot(a, b)  Return the dot product of two vectors.
    inner(a, b)     Inner product of two arrays.
    outer(a, b[, out])  Compute the outer product of two vectors.
    matmul(x1, x2, /[, out, casting, order, …])     Matrix product of two arrays.
    tensordot(a, b[, axes])     Compute tensor dot product along specified axes for arrays >= 1-D.
    einsum(subscripts, *operands[, out, dtype, …])  Evaluates the Einstein summation convention on the operands.
    einsum_path(subscripts, *operands[, optimize])  Evaluates the lowest cost contraction order for an einsum expression by considering the creation of intermediate arrays.
    linalg.matrix_power(a, n)   Raise a square matrix to the (integer) power n.
    kron(a, b)  Kronecker product of two arrays.

    Decompositions
    linalg.cholesky(a)  Cholesky decomposition.
    linalg.qr(a[, mode])    Compute the qr factorization of a matrix.
    linalg.svd(a[, full_matrices, compute_uv])  Singular Value Decomposition.
    Matrix eigenvalues
    linalg.eig(a)   Compute the eigenvalues and right eigenvectors of a square array.
    linalg.eigh(a[, UPLO])  Return the eigenvalues and eigenvectors of a complex Hermitian (conjugate symmetric) or a real symmetric matrix.
    linalg.eigvals(a)   Compute the eigenvalues of a general matrix.
    linalg.eigvalsh(a[, UPLO])  Compute the eigenvalues of a complex Hermitian or real symmetric matrix.

    Norms and other numbers
    linalg.norm(x[, ord, axis, keepdims])   Matrix or vector norm.
    linalg.cond(x[, p])     Compute the condition number of a matrix.
    linalg.det(a)   Compute the determinant of an array.
    linalg.matrix_rank(M[, tol, hermitian])     Return matrix rank of array using SVD method
    linalg.slogdet(a)   Compute the sign and (natural) logarithm of the determinant of an array.
    trace(a[, offset, axis1, axis2, dtype, out])    Return the sum along diagonals of the array.

    Solving equations and inverting matrices
    linalg.solve(a, b)  Solve a linear matrix equation, or system of linear scalar equations.
    linalg.tensorsolve(a, b[, axes])    Solve the tensor equation a x = b for x.
    linalg.lstsq(a, b[, rcond])     Return the least-squares solution to a linear matrix equation.
    linalg.inv(a)   Compute the (multiplicative) inverse of a matrix.
    linalg.pinv(a[, rcond])     Compute the (Moore-Penrose) pseudo-inverse of a matrix.
    linalg.tensorinv(a[, ind])  Compute the ‘inverse’ of an N-dimensional array. 


    #------------
    numpy.polynomial.polynomial.Polynomial

    class numpy.polynomial.polynomial.Polynomial(coef, domain=None, window=None)[source]

        A power series class.

        The Polynomial class provides the standard Python numerical methods ‘+’, ‘-‘, ‘*’, ‘//’, ‘%’, ‘divmod’, ‘**’, and ‘()’ as well as the attributes and methods listed in the ABCPolyBase documentation.
        Parameters: 

        coef : array_like

            Polynomial coefficients in order of increasing degree, i.e., (1, 2, 3) give 1 + 2*x + 3*x**2.
        domain : (2,) array_like, optional

            Domain to use. The interval [domain[0], domain[1]] is mapped to the interval [window[0], window[1]] by shifting and scaling. The default value is [-1, 1].
        window : (2,) array_like, optional

            Window, see domain for its use. The default value is [-1, 1].

            New in version 1.6.0.

        Attributes: 

        basis_name

        Methods
        degree()    The degree of the series.
        deriv([m])  Differentiate.
        fit(x, y, deg[, domain, rcond, full, w, window])    Least squares fit to data.
        fromroots(roots[, domain, window])  Return series instance that has the specified roots.
        integ([m, k, lbnd])     Integrate.
        linspace([n, domain])   Return x, y values at equally spaced points in domain.
        roots()     Return the roots of the series polynomial.

        
        
    Basics
    polyval(x, c[, tensor])     Evaluate a polynomial at points x.
    polyval2d(x, y, c)  Evaluate a 2-D polynomial at points (x, y).
    polyval3d(x, y, z, c)   Evaluate a 3-D polynomial at points (x, y, z).
    polygrid2d(x, y, c)     Evaluate a 2-D polynomial on the Cartesian product of x and y.
    polygrid3d(x, y, z, c)  Evaluate a 3-D polynomial on the Cartesian product of x, y and z.
    polyroots(c)    Compute the roots of a polynomial.
    polyfromroots(roots)    Generate a monic polynomial with given roots.
    polyvalfromroots(x, r[, tensor])    Evaluate a polynomial specified by its roots at points x.
    Fitting
    polyfit(x, y, deg[, rcond, full, w])    Least-squares fit of a polynomial to data.
    polyvander(x, deg)  Vandermonde matrix of given degree.
    polyvander2d(x, y, deg)     Pseudo-Vandermonde matrix of given degrees.
    polyvander3d(x, y, z, deg)  Pseudo-Vandermonde matrix of given degrees.
    Calculus
    polyder(c[, m, scl, axis])  Differentiate a polynomial.
    polyint(c[, m, k, lbnd, scl, axis])     Integrate a polynomial.
    Algebra
    polyadd(c1, c2)     Add one polynomial to another.
    polysub(c1, c2)     Subtract one polynomial from another.
    polymul(c1, c2)     Multiply one polynomial by another.
    polymulx(c)     Multiply a polynomial by x.
    polydiv(c1, c2)     Divide one polynomial by another.
    polypow(c, pow[, maxpower])     Raise a polynomial to a power.
    Miscellaneous
    polycompanion(c)    Return the companion matrix of c.
    polydomain  
    polyzero    
    polyone     
    polyx   
    polytrim(c[, tol])  Remove “small” “trailing” coefficients from a polynomial.
    polyline(off, scl)  Returns an array representing a linear polynomial.


    Random sampling (numpy.random)
    Simple random data
    rand(d0, d1, …, dn)     Random values in a given shape.
    randn(d0, d1, …, dn)    Return a sample (or samples) from the “standard normal” distribution.
    randint(low[, high, size, dtype])   Return random integers from low (inclusive) to high (exclusive).
    random_integers(low[, high, size])  Random integers of type np.int between low and high, inclusive.
    random_sample([size])   Return random floats in the half-open interval [0.0, 1.0).
    random([size])  Return random floats in the half-open interval [0.0, 1.0).
    ranf([size])    Return random floats in the half-open interval [0.0, 1.0).
    sample([size])  Return random floats in the half-open interval [0.0, 1.0).
    choice(a[, size, replace, p])   Generates a random sample from a given 1-D array
    bytes(length)   Return random bytes.
    Permutations
    shuffle(x)  Modify a sequence in-place by shuffling its contents.
    permutation(x)  Randomly permute a sequence, or return a permuted range.
    Distributions
    beta(a, b[, size])  Draw samples from a Beta distribution.
    binomial(n, p[, size])  Draw samples from a binomial distribution.
    chisquare(df[, size])   Draw samples from a chi-square distribution.
    dirichlet(alpha[, size])    Draw samples from the Dirichlet distribution.
    exponential([scale, size])  Draw samples from an exponential distribution.
    f(dfnum, dfden[, size])     Draw samples from an F distribution.
    gamma(shape[, scale, size])     Draw samples from a Gamma distribution.
    geometric(p[, size])    Draw samples from the geometric distribution.
    gumbel([loc, scale, size])  Draw samples from a Gumbel distribution.
    hypergeometric(ngood, nbad, nsample[, size])    Draw samples from a Hypergeometric distribution.
    laplace([loc, scale, size])     Draw samples from the Laplace or double exponential distribution with specified location (or mean) and scale (decay).
    logistic([loc, scale, size])    Draw samples from a logistic distribution.
    lognormal([mean, sigma, size])  Draw samples from a log-normal distribution.
    logseries(p[, size])    Draw samples from a logarithmic series distribution.
    multinomial(n, pvals[, size])   Draw samples from a multinomial distribution.
    multivariate_normal(mean, cov[, size, …)    Draw random samples from a multivariate normal distribution.
    negative_binomial(n, p[, size])     Draw samples from a negative binomial distribution.
    noncentral_chisquare(df, nonc[, size])  Draw samples from a noncentral chi-square distribution.
    noncentral_f(dfnum, dfden, nonc[, size])    Draw samples from the noncentral F distribution.
    normal([loc, scale, size])  Draw random samples from a normal (Gaussian) distribution.
    pareto(a[, size])   Draw samples from a Pareto II or Lomax distribution with specified shape.
    poisson([lam, size])    Draw samples from a Poisson distribution.
    power(a[, size])    Draws samples in [0, 1] from a power distribution with positive exponent a - 1.
    rayleigh([scale, size])     Draw samples from a Rayleigh distribution.
    standard_cauchy([size])     Draw samples from a standard Cauchy distribution with mode = 0.
    standard_exponential([size])    Draw samples from the standard exponential distribution.
    standard_gamma(shape[, size])   Draw samples from a standard Gamma distribution.
    standard_normal([size])     Draw samples from a standard Normal distribution (mean=0, stdev=1).
    standard_t(df[, size])  Draw samples from a standard Student’s t distribution with df degrees of freedom.
    triangular(left, mode, right[, size])   Draw samples from the triangular distribution over the interval [left, right].
    uniform([low, high, size])  Draw samples from a uniform distribution.
    vonmises(mu, kappa[, size])     Draw samples from a von Mises distribution.
    wald(mean, scale[, size])   Draw samples from a Wald, or inverse Gaussian, distribution.
    weibull(a[, size])  Draw samples from a Weibull distribution.
    zipf(a[, size])     Draw samples from a Zipf distribution.



    #----------------------------------

    Array manipulation routines
    Basic operations
    copyto(dst, src[, casting, where])  Copies values from one array to another, broadcasting as necessary.
    Changing array shape
    reshape(a, newshape[, order])   Gives a new shape to an array without changing its data.
    ravel(a[, order])   Return a contiguous flattened array.
    ndarray.flat    A 1-D iterator over the array.
    ndarray.flatten([order])    Return a copy of the array collapsed into one dimension.
    Transpose-like operations
    moveaxis(a, source, destination)    Move axes of an array to new positions.
    rollaxis(a, axis[, start])  Roll the specified axis backwards, until it lies in a given position.
    swapaxes(a, axis1, axis2)   Interchange two axes of an array.
    ndarray.T   Same as self.transpose(), except that self is returned if self.ndim < 2.
    transpose(a[, axes])    Permute the dimensions of an array.
    Changing number of dimensions
    atleast_1d(*arys)   Convert inputs to arrays with at least one dimension.
    atleast_2d(*arys)   View inputs as arrays with at least two dimensions.
    atleast_3d(*arys)   View inputs as arrays with at least three dimensions.
    broadcast   Produce an object that mimics broadcasting.
    broadcast_to(array, shape[, subok])     Broadcast an array to a new shape.
    broadcast_arrays(*args, **kwargs)   Broadcast any number of arrays against each other.
    expand_dims(a, axis)    Expand the shape of an array.
    squeeze(a[, axis])  Remove single-dimensional entries from the shape of an array.
    Changing kind of array
    asarray(a[, dtype, order])  Convert the input to an array.
    asanyarray(a[, dtype, order])   Convert the input to an ndarray, but pass ndarray subclasses through.
    asmatrix(data[, dtype])     Interpret the input as a matrix.
    asfarray(a[, dtype])    Return an array converted to a float type.
    asfortranarray(a[, dtype])  Return an array (ndim >= 1) laid out in Fortran order in memory.
    ascontiguousarray(a[, dtype])   Return a contiguous array (ndim >= 1) in memory (C order).
    asarray_chkfinite(a[, dtype, order])    Convert the input to an array, checking for NaNs or Infs.
    asscalar(a)     Convert an array of size 1 to its scalar equivalent.
    require(a[, dtype, requirements])   Return an ndarray of the provided type that satisfies requirements.
    Joining arrays
    concatenate((a1, a2, …)[, axis, out])   Join a sequence of arrays along an existing axis.
    stack(arrays[, axis, out])  Join a sequence of arrays along a new axis.
    column_stack(tup)   Stack 1-D arrays as columns into a 2-D array.
    dstack(tup)     Stack arrays in sequence depth wise (along third axis).
    hstack(tup)     Stack arrays in sequence horizontally (column wise).
    vstack(tup)     Stack arrays in sequence vertically (row wise).
    block(arrays)   Assemble an nd-array from nested lists of blocks.

    Splitting arrays
    split(ary, indices_or_sections[, axis])     Split an array into multiple sub-arrays.
    array_split(ary, indices_or_sections[, axis])   Split an array into multiple sub-arrays.
    dsplit(ary, indices_or_sections)    Split array into multiple sub-arrays along the 3rd axis (depth).
    hsplit(ary, indices_or_sections)    Split an array into multiple sub-arrays horizontally (column-wise).
    vsplit(ary, indices_or_sections)    Split an array into multiple sub-arrays vertically (row-wise).
    '''






    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', None, 
            {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
            meta={'Category': 'numpy|array',  'Keywords': []},)
    def subarray(data=('FloatPin', None),umin=('IntPin',0),umax=('IntPin',0),vmin=('IntPin',0),vmax=('IntPin',0)):
        '''
        returns data[umin:umax,vmin:vmax]
        '''

        if umax != 0 and vmax != 0:
            return np.flipud(np.array(data))[umin:umax,vmin:vmax].tolist()
        elif umax != 0:
            return np.flipud(np.array(data))[umin:umax,vmin:].tolist()
        elif vmax != 0:
            return np.flipud(np.array(data))[umin:,vmin:vmax].tolist()
        else:
            return np.flipud(np.array(data))[umin:,vmin:].tolist()

    '''
    Tiling arrays
    #tile(A, reps)  Construct an array by repeating A the number of times given by reps.
    #repeat(a, repeats[, axis])     Repeat elements of an array.

    #Adding and removing elements
    #delete(arr, obj[, axis])   Return a new array with sub-arrays along an axis deleted.
    #insert(arr, obj, values[, axis])   Insert values along the given axis before the given indices.
    #append(arr, values[, axis])    Append values to the end of an array.

    # Rearranging elements
    '''

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', None, 
            {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
            meta={'Category': 'numpy|array',  'Keywords': []},)
    def flipud(data=('FloatPin', None)):
        '''
        fliplr(data)    Flip array in the up/down  direction.
        '''
        return np.flipud(np.array(data)).tolist()


    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', None, 
            {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
            meta={'Category': 'numpy|array',  'Keywords': []},)
    def fliplr(data=('FloatPin', None)):
        '''
        fliplr(data)    Flip array in the left/right direction.
        '''
        return np.fliplr(np.array(data)).tolist()


    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', None, 
            {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
            meta={'Category': 'numpy|array',  'Keywords': []},)
    def reshape(data=('FloatPin', [1,2,3,4]),a=('IntPin',2),b=('IntPin',2),c=('IntPin',0)):
        '''
        reshape(data, (a [,b {,c]]))    Gives a new shape to an array without changing its data.
        '''
        if c  !=  0 :
            return np.reshape(np.array(data), (a,b,c)).tolist()
        elif b  !=  0 :
            return np.reshape(np.array(data), (a,b)).tolist()
        elif a  !=  0 :
            return np.reshape(np.array(data), (a)).tolist()
        else:
            raise Exception("no valid shape")


    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', None, 
            {'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}),
            meta={'Category': 'numpy|array',  'Keywords': []},)
    def roll(data=('FloatPin', None),shift=('IntPin',1),axis=('IntPin',0)):
        '''
        roll(a, shift[, axis])  Roll array elements along a given axis. 
        '''
        return np.roll(np.array(data), shift, axis=axis).tolist()


#-------------------------

#-------------numpy lib starts here -------------------------

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [], {'constraint': '1'}), meta={'Category': 'numpy|array', 'Keywords': ['list','interval']})
    def linSpace(start=('FloatPin',0.),stop=('FloatPin',10), num=('IntPin', 50)):
        """create a linear Space"""

        x1 = np.linspace(start, stop, num, endpoint=True)
        say("linspace",x1)
        return x1.tolist()

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [2.],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|random', 'Keywords': ['list','random']})
    def randomList(size=('IntPin', 50)):
        """create a random list"""
        
        x1 = np.random.random(size)
        return x1.tolist()

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [2.],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|random', 'Keywords': ['list','random']})
    def onesList(size=('IntPin', 50)):
        """create a list of ones"""
        
        x1 = np.ones(size)
        return x1.tolist()

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [2.],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|random', 'Keywords': ['list','random']})
    def zerosList(size=('IntPin', 50)):
        """create a list of zeros"""
        
        x1 = np.zeros(size)
        return x1.tolist()


    @staticmethod
    @IMPLEMENT_NODE(returns=('VectorPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|array', 'Keywords': ['list','random']})
    def zip(x=('FloatPin', [0]),y=('FloatPin', [1]),z=('FloatPin', [2])) :
        """combine """
        
        res=np.array([x,y,z]).swapaxes(0,1)
        points=[FreeCAD.Vector(list(a)) for a in res]    
        return points

    @staticmethod
    @IMPLEMENT_NODE(returns=('RotationPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|array', 'Keywords': ['list','random']})
    def zipRotation(x=('FloatPin', [0]),y=('FloatPin', [1]),z=('FloatPin', [2]),angle=('FloatPin', [2])) :
        """combine """
        
        res=np.array([x,y,z]).swapaxes(0,1)
        rots=[FreeCAD.Rotation(FreeCAD.Vector(list(a)),b) for a,b in zip(res,angle)]    
        return rots

    @staticmethod
    @IMPLEMENT_NODE(returns=('RotationPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|array', 'Keywords': ['list','random']})
    def zipPlacement(Base=('FloatPin', []),Rotation=('FloatPin', [])) :
        """combine """
        
        pms=[FreeCAD.Placement(base,rot) for base,rot in zip(Base,Rotation)]    
        return pms


    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|operations', 'Keywords': ['list','scale','multiply']})
    def scale(data=('FloatPin', [0]),factor=('FloatPin', 1.)) :
        """multiply datalist with factor """
        
        return (np.array(data)*factor).tolist()

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|operations', 'Keywords': ['list','scale','multiply']})
    def round(data=('FloatPin', [0]),decimals=('IntPin', 1)) :
        """multiply datalist with factor """
        
        return np.round(np.array(data),decimals).tolist()

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|operations', 'Keywords': ['list','scale','multiply']})
    def linearTrafo(data=('FloatPin', [0]),a=('FloatPin', 1.),b=('FloatPin', 0.)) :
        """
        a*x + b
        """
        
        return (np.array(data)*a +b).tolist()

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|trigonometry', 'Keywords': ['list','scale','multiply']})
    def sin(data=('FloatPin', [0]),a=('FloatPin', 1.),b=('FloatPin', 1.),c=('FloatPin', 0.)) :
        """a*sin(b*x+c)"""
        
        return (a*np.sin(np.array(data)*b +c)).tolist()

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|trigonometry', 'Keywords': ['list','scale','multiply']})
    def cos(data=('FloatPin', [0]),a=('FloatPin', 1.),b=('FloatPin', 1.),c=('FloatPin', 0.)) :
        """a*cos(b*x+c)"""
        
        return list(a*np.cos(np.array(data)*b +c))

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|trigonometry', 'Keywords': ['list','scale','multiply']})
    def tan(data=('FloatPin', [0]),a=('FloatPin', 1.),b=('FloatPin', 1.),c=('FloatPin', 1.)) :
        """a*tan(b*x+c)"""
        
        return list(a*np.tan(np.array(data)*b +c))

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|trigonometry', 'Keywords': ['list','scale','multiply']})
    def arctan(data=('FloatPin', [0]),a=('FloatPin', 1.),b=('FloatPin', 1.),c=('FloatPin', 1.)) :
        """arctan(x)"""
        
        return list(np.arctan(np.array(data)))

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|trigonometry', 'Keywords': ['list','scale','multiply']})
    def arctan2(y=('FloatPin', [0]),x=('FloatPin', [0])) :
        """arctan2(y,x)"""
        
        return list(np.arctan2(np.array(y),np.array(x)))

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|trigonometry', 'Keywords': ['list','scale','multiply']})
    def rad2deg(radians=('FloatPin', [0])) :
        """radians to degree"""
        
        return list(np.rad2deg(np.array(radians)))

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|trigonometry', 'Keywords': ['degree','radian','angle']})
    def deg2rad(degree=('FloatPin', [0])) :
        """
        degree to radians
        """
        
        return list(np.deg2rad(np.array(degree)))


    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|trigonometry', 'Keywords': ['list','scale','multiply']})
    def unwrap(radians=('FloatPin', [0])) :
        """
        Unwrap by changing deltas between values to 2*pi complement.
        Unwrap radian phase p by changing absolute jumps greater than discont to their 2*pi complement along the given axis.
        """
        
        return list(np.unwrap(np.array(radians)))


    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|interpolate', 'Keywords': ['list','scale','multiply']})
    def interp_lin(x=('FloatPin', [0,0.5,1.,1.5]),xp=('FloatPin', [0,1,2]),yp=('FloatPin', [0.,2.,0.]),) :
        """
    One-dimensional linear interpolation.
    Returns the one-dimensional piecewise linear interpolant 
    to a function with given discrete data points (xp, fp), 
    evaluated at x.
        """
        
        return list(np.interp(x,xp,yp))

    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|operations', 'Keywords': ['list','scale','multiply']})
    def add(x=('FloatPin', [0,1]),y=('FloatPin', [0,2])) :
        """
        """
        
        return list(np.array(x)+np.array(y))


    @staticmethod
    @IMPLEMENT_NODE(returns=('FloatPin', [],{'constraint': '1', "enabledOptions": PinOptions.ArraySupported | PinOptions.AllowAny}), meta={'Category': 'numpy|interpolate', 'Keywords': ['list','scale','multiply']})
    def interp_cubic(x=('FloatPin', [0,0.5,1.,1.5]),xp=('FloatPin', [0,1,2]),yp=('FloatPin', [0.,2.,0.]),) :
        """
    Interpolate a 1-D function.
    xp and yp are arrays of values used to approximate some function 
    f: y = f(x). 
    This class returns a function whose call method 
    uses interpolation to find the value of new points x.
        """
        from scipy import interpolate
        f = interpolate.interp1d(xp, yp,kind='cubic')
        y = f(np.array(x)) 
        
        return list(y)




