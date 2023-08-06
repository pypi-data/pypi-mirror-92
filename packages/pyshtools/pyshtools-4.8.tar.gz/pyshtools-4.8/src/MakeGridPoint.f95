function MakeGridPoint(cilm, lmax, lat, lon, norm, csphase, dealloc)
!------------------------------------------------------------------------------
!
!   This function will determine the value at a given latitude and
!   longitude corresponding to the given set of spherical harmonics.
!   Latitude and Longitude must be in degrees.
!
!   Calling Parameters
!
!       IN
!           cilm        Spherical harmonic coefficients, with dimensions
!                       (2, lmax+1, lmax+1).
!           lmax        Maximum degree used in the expansion.
!           lat         latitude (degrees).
!           lon         longitude (degrees).
!
!       OPTIONAL (IN)
!           norm        Spherical harmonic normalization:
!                           (1) "geodesy" (default)
!                           (2) Schmidt
!                           (3) unnormalized
!                           (4) orthonormalized
!           csphase     1: Do not include the phase factor of (-1)^m (default).
!                       -1: Apply the phase factor of (-1)^m.
!           dealloc     If (1) Deallocate saved memory in Legendre function
!                       routines. Default (0) is not to deallocate memory.
!
!   Copyright (c) 2005-2019, SHTOOLS
!   All rights reserved.
!
!------------------------------------------------------------------------------
    use SHTOOLS, only: PlmBar, PLegendreA, PlmSchmidt, PlmON
    use ftypes

    implicit none

    real(dp) :: MakeGridPoint
    real(dp), intent(in) :: cilm(:,:,:), lat, lon
    integer(int32), intent(in) :: lmax
    integer(int32), intent(in), optional :: norm, csphase, dealloc
    real(dp) :: pi, x, expand, lon_rad
    integer(int32) :: index, l, m, l1, m1, lmax_comp, phase, astat(3)
    real(dp), allocatable :: pl(:), cosm(:), sinm(:)

    if (size(cilm(:,1,1)) < 2 .or. size(cilm(1,:,1)) < lmax+1 .or. &
            size(cilm(1,1,:)) < lmax+1) then
        print*, "Error --- MakeGridPoint"
        print*, "CILM must be dimensioned as (2, LMAX+1, LMAX+1) " // &
                "where LMAX is ", lmax
        print*, "Input dimension is ", size(cilm(:,1,1)), size(cilm(1,:,1)), &
                size(cilm(1,1,:))
        stop
    end if

    if (present(norm)) then
        if (norm > 4 .or. norm < 1) then
            print*, "Error - MakeGridPoint"
            print*, "Parameter NORM must be 1, 2, 3, or 4"
            stop
        end if
    end if

    if (present(csphase)) then
        if (csphase == -1) then
             phase = -1
        else if (csphase == 1) then
                phase = 1
        else
            print*, "Error --- MakeGridPoint"
            print*, "CSPHASE must be 1 (exclude) or -1 (include)."
            print*, "Input value is ", csphase
            stop
        end if

    else
        phase = 1

    end if

    lmax_comp = min(lmax, size(cilm(1,1,:)) - 1)

    allocate (pl(((lmax_comp+1) * (lmax_comp+2)) / 2), stat = astat(1))
    allocate (cosm(lmax_comp+1), stat = astat(2))
    allocate (sinm(lmax_comp+1), stat = astat(3))

    if (sum(astat(1:3)) /= 0) then
        print*, "Error --- MakeGridPoint"
        print*, "Cannot allocate memory for arrays PL, COSM and SINM", &
                astat(1), astat(2), astat(3)
        stop
    end if

    pi = acos(-1.0_dp)
    x = sin(lat * pi / 180.0_dp)
    lon_rad = lon * pi / 180.0_dp

    if (present(norm)) then
        if (norm == 1) call PlmBar(pl, lmax_comp, x, csphase = phase)
        if (norm == 2) call PlmSchmidt(pl, lmax_comp, x, csphase = phase)
        if (norm == 3) call PLegendreA(pl, lmax_comp, x, csphase = phase)
        if (norm == 4) call PlmON(pl, lmax_comp, x, csphase = phase)

    else
        call PlmBar(pl, lmax_comp, x, csphase = phase)

    end if

    expand = 0.0_dp

    ! Precompute sines and cosines. Use multiple angle identity to minimize
    ! number of calls to SIN and COS.
    sinm(1) = 0.0_dp
    cosm(1) = 1.0_dp

    if (lmax_comp > 0) then
        sinm(2) = sin(lon_rad)
        cosm(2) = cos(lon_rad)
    end if

    do m = 2, lmax_comp, 1
        m1 = m + 1
        sinm(m1) = 2 * sinm(m) * cosm(2) - sinm(m-1)
        cosm(m1) = 2 * cosm(m) * cosm(2) - cosm(m-1)
    end do

    do l = lmax_comp, 0, -1
        l1 = l + 1
        index = (l+1) * l / 2 + 1
        expand = expand + cilm(1,l1,1) * pl(index)

        do m = 1, l, 1
            m1 = m + 1
            index = index + 1
            expand = expand + (cilm(1,l1,m1) * cosm(m1) + &
                               cilm(2,l1,m1) * sinm(m1)) * pl(index)
        end do

    end do

    MakeGridPoint = expand

    ! deallocate memory
    if (present(dealloc)) then
        if (dealloc == 1) then
            if (present(norm)) then
                if (norm == 1) call PlmBar(pl, -1, x)
                if (norm == 2) call PlmSchmidt(pl, -1, x)
                if (norm == 4) call PlmON(pl, -1, x)
            else
                call PlmBar(pl, -1, x)
            end if
        end if
    end if

    deallocate (pl)
    deallocate (cosm)
    deallocate (sinm)

end function MakeGridPoint
