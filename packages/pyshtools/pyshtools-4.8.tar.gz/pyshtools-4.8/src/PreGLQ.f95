subroutine PreGLQ(x1, x2, n, zero, w, exitstatus)
!------------------------------------------------------------------------------
!
!   This routine will find the zeros and weights that are
!   used in Gauss-Legendre quadrature routines. (Based on routines
!   in Numerical Recipes).
!
!   Calling Parameters
!
!       IN
!           x1      Lower bound of integration.
!           x2      Upper bound of integration.
!           n       Number of points used in the quadrature. n points
!                   will integrate a polynomial of degree 2n-1 exactly.
!
!       OUT
!           zero    Array of n Gauss points, which correspond to the zeros
!                   of P(n,0).
!           w       Array of n weights used in the quadrature.
!
!       OPTIONAL (OUT)
!           exitstatus  If present, instead of executing a STOP when an error
!                       is encountered, the variable exitstatus will be
!                       returned describing the error.
!                       0 = No errors;
!                       1 = Improper dimensions of input array;
!                       2 = Improper bounds for input variable;
!                       3 = Error allocating memory;
!                       4 = File IO error.
!
!   Note 
!       1.  If EPS is less than what is defined, then the do
!           loop for finding the roots might never terminate for some
!           values of lmax. If the algorithm doesn't converge, consider
!           increasing itermax, or decreasing eps.
!
!   Copyright (c) 2005-2019, SHTOOLS
!   All rights reserved.
!
!------------------------------------------------------------------------------
    use ftypes

    implicit none

    real(dp), intent(in) :: x1, x2
    real(dp), intent(out) :: zero(:), w(:)
    integer(int32), intent(in) :: n
    integer(int32), intent(out), optional :: exitstatus
    integer(int32) :: i, j, m, iter
    integer(int32), parameter :: itermax = 1000
    real(dp), parameter :: eps=1.0e-15_dp
    real(dp) :: p1, p2, p3, pp, z, z1, xm, xu, pi

    if (present(exitstatus)) exitstatus = 0

    if (size(zero) < n) then
        print*, "Error --- PreGLQ"
        print*, "ZERO must be dimensioned as (N) where N is ", n
        print*, "Input array is dimensioned ", size(zero)
        if (present(exitstatus)) then
            exitstatus = 1
            return
        else
            stop
        end if

    else if (size(w) < n) then
        print*, "Error --- PreGLQ"
        print*, "W must be dimensioned as (N) where N is ", n
        print*, "Input array is dimensioned ", size(w)
        if (present(exitstatus)) then
            exitstatus = 1
            return
        else
            stop
        end if

    end if

    pi = acos(-1.0_dp)

    zero = 0.0_dp
    w = 0.0_dp

!------------------------------------------------------------------------------
!
!   The roots are symmetric in the interval, so we only have to find half of
!   them. xm is the midpoint of integration, and xu is the scaling factor
!   between the interval of integration and that of the -1 to 1 interval for
!   the Gauss-Legendre interval.
!
!------------------------------------------------------------------------------
    m = (n+1) / 2
    xm = (x2 + x1) / 2.0_dp
    xu = (x2 - x1) / 2.0_dp

    !   Compute roots and weights
    do i = 1, m
        iter = 0
        ! Approximation for the ith root
        z=cos(pi * (i-0.25_dp) / (n+0.5_dp))

        ! Find the true value using Newton's method
        do
            iter = iter + 1

            p1 = 1.0_dp
            p2 = 0.0_dp

            ! Determine the Legendre polynomial evaluated at z (p1) using
            ! recurrence relationships.
            do j = 1, n
                p3 = p2
                p2 = p1
                p1 = (dble(2*j-1)*z*p2-dble(j-1)*p3) / dble(j)

            end do

            ! This is the derivative of the legendre polynomial using 
            ! recurrence relationships.
            pp = dble(n) * (z * p1 - p2) / (z * z-1.0_dp)

            ! This is Newton's method here
            z1 = z
            z = z1-p1 / pp

            if (abs(z-z1) <= eps) exit

            if (iter >itermax) then
                print*, "Error --- PreGLQ"
                print*, "Root Finding of PreGLQ not converging."
                print*, "m , n = ", m, n
                if (present(exitstatus)) then
                    exitstatus = 5
                    return
                else
                    stop
                end if

            end if

        end do

        zero(i) = xm + xu * z
        zero(n+1-i) = xm - xu * z
        w(i) = 2.0_dp * xu / ((1.0_dp-z * z) * pp *pp)
        w(n+1-i) = w (i)

    end do

end subroutine PreGLQ


function NGLQ(degree)
!------------------------------------------------------------------------------
!
!   For a polynomial of order degree, this simple function
!   will determine how many gauss-legendre quadrature points
!   are needed in order to integrate the function exactly.
!
!------------------------------------------------------------------------------
    use ftypes

    implicit none

    integer(int32) :: NGLQ
    integer(int32), intent(in) :: degree

    if (degree < 0) then
        print*, "Error --- NGLQ"
        print*, "DEGREE must be greater or equal to zero"
        print*, "DEGREE = ", degree
        stop
    end if

    nglq = ceiling((degree+1.0_dp) / 2.0_dp)

end function NGLQ


function NGLQSH(degree)
!------------------------------------------------------------------------------
!
!   This function returns the number of gauss-legendre points that
!   are needed to exactly integrate a spherical harmonic field of
!   Lmax = degree.
!
!------------------------------------------------------------------------------
    use ftypes

    implicit none

    integer(int32) :: NGLQSH
    integer(int32), intent(in) :: degree

    if (degree < 0) then
        print*, "Error --- NGLQSH"
        print*, "DEGREE must be greater or equal to zero"
        print*, "DEGREE = ", degree
        stop
    end if

    nglqsh = degree + 1

end function NGLQSH


function NGLQSHN(degree, n)
!------------------------------------------------------------------------------
!
!   This function returns the number of gauss-legendre points that
!   are needed to exactly integrate a spherical harmonic field of
!   Lmax = degree raised to the nth power. Here, the maximum degree
!   of the integrand is n*lmax + lmax, or (n+1)*lmax
!
!------------------------------------------------------------------------------
    use ftypes

    implicit none

    integer(int32) :: NGLQSHN
    integer(int32), intent(in) :: degree, n

    if (degree < 0) then
        print*, "Error --- NGLQSHN"
        print*, "DEGREE must be greater or equal to zero"
        print*, "DEGREE = ", degree
        stop
    end if

    nglqshn = ceiling(((n+1.0_dp)*degree + 1.0_dp)/2.0_dp)

end function NGLQSHN
