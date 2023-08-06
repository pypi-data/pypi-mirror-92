subroutine SHExpandGLQC(cilm, lmax, gridglq, w, plx, zero, norm, csphase, &
                        lmax_calc, exitstatus)
!------------------------------------------------------------------------------
!
!   This program will expand a grid of complex data (regulary spaced in
!   longitude, and irregurarly in latitude according to the Guass-Legendre
!   quadrature points) into complex spherical harmonics by utilizing an FFT of
!   each latitudinal band, and a Guass-Legendre Quadrature in latitute. Note
!   that the array PLX (obtained from SHGLQ with CNORM=1) is optional, and
!   should not be precomputed when memory is an issue (i.e., LMAX>360). It is
!   implicitly assumed that the gridded data are bandlimited to degree LMAX. If
!   the optional parameter LMAX_CALC is specified, the spherical harmonic
!   coefficients will be calculated only up to and including this degree.
!
!   If PLX is not present, the Legendre functions are computed on the fly
!   using the scaling methodolgy presented in Holmes and Featherston (2002).
!   When NORM is 1, 2 or 4, these are accurate to degree 2800. When NORM is 3,
!   the routine is only stable to about degree 15.
!
!   Calling Parameters
!
!       IN
!           gridglq     Gridded data used in the expansion generated
!                       from a call to MakeGridGLQ, with dimensions
!                       (LMAX+1, 2*LMAX+1).
!           lmax        Spherical harmonic bandwidth of the input grid.
!                       If LMAX_CALC is not specified, this corresponds
!                       to the maximum spherical harmonic degree of the
!                       expansion.
!           w           Gauss-Legendre points used in the integrations
!                       (determined from a call to SHGLQ).
!
!       OUT
!           cilm        Spherical harmonic coefficients of expansion with
!                       dimensions (2, LMAX+1, LMAX+1), or if LMAX_CAL is
!                       present (2, LMAX_CALC+1, LMAX_CALC+1).
!
!       OPTIONAL (IN)
!           plx         Input array of Associated Legendre Polnomials computed
!                       at the Gauss-Legendre points (determined from a call to
!                       SHGLQ). If this is not included, then the optional
!                       array ZERO MUST be inlcuded. PLX must be computed using
!                       CNORM=1.
!           zero        Array of dimension LMAX+1 that contains the latitudinal
!                       gridpoints used in the Gauss-Legendre quadrature
!                       integration scheme, calculated from a call to SHGLQ.
!                       This is only needed if PLX is not given.
!           norm        Normalization to be used when calculating the Legendre
!                       functions
!                           (1) "geodesy" (default)
!                           (2) Schmidt
!                           (3) unnormalized
!                           (4) orthonormalized
!           csphase     1: Do not include the phase factor of (-1)^m (default).
!                       -1: Apply the phase factor of (-1)^m.
!           lmax_calc   The maximum spherical harmonic degree calculated in the
!                       spherical harmonic expansion.
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
!   Copyright (c) 2005-2019, SHTOOLS
!   All rights reserved.
!
!------------------------------------------------------------------------------
    use FFTW3
    use ftypes
    use, intrinsic :: iso_c_binding

    implicit none

    real(dp), intent(in) :: w(:)
    complex(dp), intent(in) :: gridglq(:,:)
    real(dp), intent(in), optional :: plx(:,:), zero(:)
    complex(dp), intent(out) :: cilm(:,:,:)
    integer(int32), intent(in) :: lmax
    integer(int32), intent(in), optional :: norm, csphase, lmax_calc
    integer(int32), intent(out), optional :: exitstatus
    integer(int32) :: nlong, nlat, i, l, m, k, l1, m1, i_s, astat(4), lnorm, &
                      lmax_comp
    real(dp) :: pi, prod, scalef, rescalem, u, p, pmm, pm1, pm2, z
    complex(dp) :: cc(2*lmax+1), ccs(2*lmax+1), gridl(2*lmax+1), &
                   gridls(2*lmax+1), fcoef1(2*lmax+1), fcoef2(2*lmax+1), &
                   ffc1(-1:1), ffc2(-1:1)
    type(C_PTR) :: plan, plans
    real(dp), save, allocatable :: ff1(:,:), ff2(:,:), sqr(:)
    integer(int8), save, allocatable :: fsymsign(:,:)
    integer(int32), save :: lmax_old = 0, norm_old = 0
    integer(int32) :: phase

!$OMP   threadprivate(sqr, ff1, ff2, fsymsign, lmax_old, norm_old)

    if (present(exitstatus)) exitstatus = 0

    if (present(lmax_calc)) then
        if (lmax_calc > lmax) then
            print*, "Error --- SHExpandGLQC"
            print*, "LMAX_CALC must be less than or equal to LMAX."
            print*, "LMAX = ", lmax
            print*, "LMAX_CALC = ", lmax_calc
            if (present(exitstatus)) then
                exitstatus = 2
                return
            else
                stop
            end if

        else
            lmax_comp = min(lmax, lmax_calc)

        end if

    else
        lmax_comp = lmax

    end if

    if (size(cilm(:,1,1)) < 2 .or. size(cilm(1,:,1)) < lmax_comp+1 &
            .or. size(cilm(1,1,:)) < lmax_comp+1) then
        print*, "Error --- SHExpandGLQC"
        print*, "CILM must be dimensioned as (2, LMAX_COMP+1, LMAX_COMP+1)"
        print*, "where LMAX_COMP = MIN(LMAX+1, LMAX_CALC+1)"
        print*, "LMAX = ", lmax
        if (present(lmax_calc)) print*, "LMAX_CALC = ", lmax_calc
        print*, "Input dimension is ", size(cilm(:,1,1)), size(cilm(1,:,1)), &
                size(cilm(1,1,:))
        if (present(exitstatus)) then
            exitstatus = 1
            return
        else
            stop
        end if

    else if (size(gridglq(1,:)) < 2*lmax+1 &
            .or. size(gridglq(:,1)) < lmax+1 ) then
        print*, "Error --- SHExpandGLQC"
        print*, "GRIDGLQ must be dimensioned as (LMAX+1, 2*LMAX+1) " // &
                "where LMAX is ", lmax
        print*, "Input array is dimensioned ", size(gridglq(:,1)), &
                size(gridglq(1,:))
        if (present(exitstatus)) then
            exitstatus = 1
            return
        else
            stop
        end if

    else if (size(w) < lmax+1) then
        print*, "Error --- SHExpandGLQC"
        print*, "W must be dimensioned as (LMAX+1) where LMAX is ", lmax
        print*, "Input array is dimensioned as ", size(w)
        if (present(exitstatus)) then
            exitstatus = 1
            return
        else
            stop
        end if

    end if

    if (present(plx)) then
        if (size(plx(:,1)) < lmax+1 .or. size(plx(1,:)) &
                < (lmax+1)*(lmax+2)/2) then
            print*, "Error --- SHExpandGLQC"
            print*, "PLX must be dimensioned as (LMAX+1, " // &
                    "(LMAX+1)*(LMAX+2)/2) where LMAX is ", lmax
            print*, "Input array is dimensioned as ", size(plx(:,1)), &
                    size(plx(1,:))
            if (present(exitstatus)) then
                exitstatus = 1
                return
            else
                stop
            end if

        end if

    else if (present(zero)) then
        if (size(zero) < lmax+1) then
            print*, "Error --- SHExpandGLQC"
            print*, "ZERO must be dimensioned as (LMAX+1) where LMAX is ", lmax
            print*, "Input array is dimensioned ", size(zero)
            if (present(exitstatus)) then
                exitstatus = 1
                return
            else
                stop
            end if

        end if

    else
        print*, "Error --- SHExpandGLQC"
        print*, "Either PLX or ZERO must be specified."
        if (present(exitstatus)) then
            exitstatus = 5
            return
        else
            stop
        end if

    end if

    if (present(norm)) then
        if (norm > 4 .or. norm < 1) then
            print*, "Error - SHExpandGLQC"
            print*, "Parameter NORM must be 1 (geodesy), 2 (Schmidt), " // &
                    "3 (unnormalized), or 4 (orthonormalized)."
            print*, "Input value is ", norm
            if (present(exitstatus)) then
                exitstatus = 2
                return
            else
                stop
            end if

        end if

        lnorm = norm

    else
        lnorm = 1

    end if

    if (present(csphase)) then
        if (csphase /= -1 .and. csphase /= 1) then
            print*, "Error --- SHExpandGLQC"
            print*, "CSPHASE must be 1 (exclude) or -1 (include)."
            if (present(exitstatus)) then
                exitstatus = 2
                return
            else
                stop
            end if

        else
            phase = csphase

        end if

    else
        phase = 1

    end if

    nlong = 2 * (lmax + 1) - 1
    ! This is the number of points (and period) used
    ! in the FFT in order that m=0 to lmax.

    nlat = lmax + 1

    pi = acos(-1.0_dp)

    cilm = cmplx(0.0_dp, 0.0_dp, dp)

    scalef = 1.0e-280_dp

    !--------------------------------------------------------------------------
    !
    !   Calculate recursion constants used in computing the Legendre functions.
    !
    !--------------------------------------------------------------------------
    if ( (lmax_comp /= lmax_old .or. lnorm /= norm_old) &
            .and. .not. present(plx) ) then

        if (allocated (sqr)) deallocate (sqr)
        if (allocated (ff1)) deallocate (ff1)
        if (allocated (ff2)) deallocate (ff2)
        if (allocated (fsymsign)) deallocate (fsymsign)

        allocate (sqr(2*lmax_comp+1), stat=astat(1))
        allocate (ff1(lmax_comp+1,lmax_comp+1), stat=astat(2))
        allocate (ff2(lmax_comp+1,lmax_comp+1), stat=astat(3))
        allocate (fsymsign(lmax_comp+1,lmax_comp+1), stat=astat(4))

        if (sum(astat(1:4)) /= 0) then
            print*, "Error --- SHExpandGLQ"
            print*, "Problem allocating arrays SQR, FF1, FF2, or FSYMSIGN", &
                    astat(1), astat(2), astat(3), astat(4)
            if (present(exitstatus)) then
                exitstatus = 3
                return
            else
                stop
            end if

        end if

        !----------------------------------------------------------------------
        !
        !   Calculate signs used for symmetry of Legendre functions about
        !   equator.
        !
        !----------------------------------------------------------------------
        do l = 0, lmax_comp, 1
            do m = 0, l, 1
                if (mod(l-m,2) == 0) then
                    fsymsign(l+1,m+1) = 1

                else
                    fsymsign(l+1,m+1) = -1

                end if

            end do

        end do

        !----------------------------------------------------------------------
        !
        !   Precompute square roots of integers that are used several times.
        !
        !----------------------------------------------------------------------
        do l = 1, 2 * lmax_comp + 1
            sqr(l) = sqrt(dble(l))
        end do

        !----------------------------------------------------------------------
        !
        !   Precompute multiplicative factors used in recursion relationships
        !       P(l,m) = x*f1(l,m)*P(l-1,m) - P(l-2,m)*f2(l,m)
        !       k = l*(l+1)/2 + m + 1
        !   Note that prefactors are not used for the case when m=l as a
        !   different recursion is used. Furthermore, for m=l-1, Plmbar(l-2,m)
        !   is assumed to be zero.
        !
        !----------------------------------------------------------------------
        select case (lnorm)
            case (1,4)
                if (lmax_comp /= 0) then
                    ff1(2,1) = sqr(3)
                    ff2(2,1) = 0.0_dp

                end if

                do l = 2, lmax_comp, 1
                    ff1(l+1,1) = sqr(2*l-1) * sqr(2*l+1) / dble(l)
                    ff2(l+1,1) = dble(l-1) * sqr(2*l+1) / sqr(2*l-3) / dble(l)

                    do m = 1, l - 2, 1
                        ff1(l+1,m+1) = sqr(2*l+1) * sqr(2*l-1) / sqr(l+m) &
                                       / sqr(l-m)
                        ff2(l+1,m+1) = sqr(2*l+1) * sqr(l-m-1) * sqr(l+m-1) &
                                       / sqr(2*l-3) / sqr(l+m) / sqr(l-m) 

                    end do

                    ff1(l+1,l) = sqr(2*l+1) * sqr(2*l-1) / sqr(l+m) / sqr(l-m)
                    ff2(l+1,l) = 0.0_dp

                end do

            case (2)
                if (lmax_comp /= 0) then
                    ff1(2,1) = 1.0_dp
                    ff2(2,1) = 0.0_dp
                end if

                do l = 2, lmax_comp, 1
                    ff1(l+1,1) = dble(2*l-1) / dble(l)
                    ff2(l+1,1) = dble(l-1) / dble(l)

                    do m = 1, l - 2, 1
                        ff1(l+1,m+1) = dble(2*l-1) / sqr(l+m) / sqr(l-m)
                        ff2(l+1,m+1) = sqr(l-m-1) * sqr(l+m-1) / sqr(l+m) &
                                       / sqr(l-m)
                    end do

                    ff1(l+1,l) = dble(2*l-1) / sqr(l+m) / sqr(l-m)
                    ff2(l+1,l) = 0.0_dp

                end do

            case (3)
                do l = 1, lmax_comp, 1
                    ff1(l+1,1) = dble(2*l-1) / dble(l)
                    ff2(l+1,1) = dble(l-1) / dble(l)

                    do m = 1, l - 1, 1
                        ff1(l+1,m+1) = dble(2*l-1) / dble(l-m)
                        ff2(l+1,m+1) = dble(l+m-1) / dble(l-m)

                    end do

                end do

        end select

        lmax_old = lmax_comp
        norm_old = lnorm

    end if

    !--------------------------------------------------------------------------
    !
    !   Create generic plan for gridl and gridls.
    !
    !--------------------------------------------------------------------------
    plan = fftw_plan_dft_1d(nlong, gridl(1:nlong), cc(1:nlong), &
                            FFTW_FORWARD, FFTW_MEASURE)
    plans = fftw_plan_dft_1d(nlong, gridls(1:nlong), ccs(1:nlong), &
                             FFTW_FORWARD, FFTW_MEASURE)

    !--------------------------------------------------------------------------
    !
    !   Determine Cilms, one l at a time I by integrating over all
    !   latitudes using Gauss-Legendre Quadrature. When PLX is not
    !   present, the Legendre functions are computed on the fly
    !   during the summations over l and m. These are scaled using
    !   the methodology of Holmesand Featherstone (2002), with the
    !   exception of the m=0 terms that do not need to be scaled
    !
    !--------------------------------------------------------------------------
    if (present(plx)) then
        do i = 1, nlat

            gridl(1:nlong) = gridglq(i,1:nlong)
            call fftw_execute_dft(plan, gridl, cc)   ! take fourier transform
            fcoef1(1:nlong) = 2 * cc(1:nlong) * w(i) * pi / dble(nlong)

            k = 0

            do l = 0, lmax_comp, 1
                l1 = l + 1
                k = k + 1
                cilm(1,l1,1) = cilm(1,l1,1) + plx(i,k) * fcoef1(1)

                do m = 1, l, 1
                    m1 = m + 1
                    k = k + 1
                    cilm(1,l1,m1) = cilm(1,l1,m1) + plx(i,k) * fcoef1(m1)
                    cilm(2,l1,m1) = cilm(2,l1,m1) &
                                    + ((-1)**mod(m,2)) * plx(i,k) * &
                                    fcoef1(nlong-(m-1))

                end do

            end do

        end do

    else
        do i = 1, (nlat + 1) / 2
            if (i == (nlat + 1) / 2 .and. mod(nlat,2) /= 0) then
            ! This latitude is the equator; z=0, u=1

                gridl(1:nlong) = gridglq(i,1:nlong)
                call fftw_execute_dft(plan, gridl, cc)
                fcoef1(1:nlong) = 2 * w(i) * pi * cc(1:nlong) / dble(nlong)

                u = 1.0_dp

                select case (lnorm)
                    case (1,2,3); pm2 = 1.0_dp
                    case (4);     pm2 = 1.0_dp / sqrt(4*pi)
                end select

                cilm(1,1,1) = cilm(1,1,1) + pm2 * fcoef1(1)

                if (lmax_comp == 0) cycle

                do l = 2, lmax_comp, 2
                    l1 = l + 1
                    p = - ff2(l1,1) * pm2
                    pm2 = p
                    cilm(1,l1,1) = cilm(1,l1,1) + p * fcoef1(1)

                end do

                select case (lnorm)
                    case (1,2,3); pmm = scalef
                    case (4); pmm = scalef / sqrt(4*pi)
                end select

                rescalem = 1.0_dp / scalef

                do m = 1, lmax_comp-1, 1
                    m1 = m + 1

                    select case (lnorm)
                        case (1,4)
                            pmm = phase * pmm * sqr(2*m+1) / sqr(2*m)
                            pm2 = pmm
                        case (2)
                            pmm = phase * pmm * sqr(2*m+1) / sqr(2*m)
                            pm2 = pmm / sqr(2*m+1)
                        case (3)
                            pmm = phase * pmm * (2*m-1)
                            pm2 = pmm
                    end select

                    fcoef1(m1) = fcoef1(m1) * rescalem
                    fcoef1(nlong-(m-1)) = fcoef1(nlong-(m-1)) &
                                          * rescalem * ((-1)**mod(m,2))

                    cilm(1,m1,m1) = cilm(1,m1,m1) + pm2 * fcoef1(m1)
                    cilm(2,m1,m1) = cilm(2,m1,m1) + pm2 * fcoef1(nlong-(m-1))

                    do l = m + 2, lmax_comp, 2
                        l1 = l + 1
                        p = - ff2(l1,m1) * pm2
                        pm2 = p
                        cilm(1,l1,m1) = cilm(1,l1,m1) + p * fcoef1(m1)
                        cilm(2,l1,m1) = cilm(2,l1,m1) + p * fcoef1(nlong-(m-1))

                    end do

                end do

                select case (lnorm)
                    case (1,4)
                        pmm = phase * pmm * sqr(2*lmax_comp+1) &
                              / sqr(2*lmax_comp) * rescalem
                    case(2)
                        pmm = phase * pmm / sqr(2*lmax_comp) * rescalem
                    case(3)
                        pmm = phase * pmm * (2*lmax_comp-1) * rescalem
                end select

                cilm(1,lmax_comp+1,lmax_comp+1) = &
                                cilm(1,lmax_comp+1,lmax_comp+1) &
                                + pmm * fcoef1(lmax_comp+1)
                cilm(2,lmax_comp+1,lmax_comp+1) = &
                                cilm(2,lmax_comp+1,lmax_comp+1) &
                                + ((-1)**mod(lmax_comp,2)) * pmm &
                                * fcoef1(nlong-(lmax_comp-1))

            else
                z = zero(i)
                u = sqrt( (1.0_dp-z) * (1.0_dp+z) )

                gridl(1:nlong) = gridglq(i,1:nlong)
                call fftw_execute_dft(plan, gridl, cc)
                fcoef1(1:nlong) = 2 * w(i) * pi * cc(1:nlong) / dble(nlong)

                i_s = nlat + 1 - i  ! point symmetric about the equator

                gridls(1:nlong) = gridglq(i_s,1:nlong)
                call fftw_execute_dft(plans, gridls, ccs)
                fcoef2(1:nlong) = 2 * w(i_s) * pi * ccs(1:nlong) / dble(nlong)

                select case (lnorm)
                    case (1,2,3); pm2 = 1.0_dp
                    case (4);     pm2 = 1.0_dp / sqrt(4*pi)
                end select

                cilm(1,1,1) = cilm(1,1,1) + pm2 * (fcoef1(1) + fcoef2(1))
                ! fsymsign = 1

                if (lmax_comp == 0) cycle

                pm1 = ff1(2,1) * z * pm2
                cilm(1,2,1) = cilm(1,2,1) + pm1 * (fcoef1(1) - fcoef2(1))
                ! fsymsign = -1

                ffc1(-1) = fcoef1(1) - fcoef2(1)
                ffc1(1) = fcoef1(1) + fcoef2(1)

                do l = 2, lmax_comp, 1
                    l1 = l + 1
                    p = ff1(l1,1) * z * pm1 - ff2(l1,1) * pm2
                    pm2 = pm1
                    pm1 = p
                    cilm(1,l1,1) = cilm(1,l1,1) + p * ffc1(fsymsign(l1,1))
                end do

                select case (lnorm)
                    case (1,2,3); pmm = scalef
                    case (4); pmm = scalef / sqrt(4*pi)
                end select

                rescalem = 1.0_dp / scalef

                do m = 1, lmax_comp-1, 1
                    m1 = m + 1
                    rescalem = rescalem * u

                    select case (lnorm)
                        case (1,4)
                            pmm = phase * pmm * sqr(2*m+1) / sqr(2*m)
                            pm2 = pmm

                        case (2)
                            pmm = phase * pmm * sqr(2*m+1) / sqr(2*m)
                            pm2 = pmm / sqr(2*m+1)

                        case (3)
                            pmm = phase * pmm * (2*m-1)
                            pm2 = pmm

                    end select

                    fcoef1(m1) = fcoef1(m1) * rescalem
                    fcoef1(nlong-(m-1)) = fcoef1(nlong-(m-1)) &
                                          * rescalem * ((-1)**mod(m,2))
                    fcoef2(m1) = fcoef2(m1) * rescalem
                    fcoef2(nlong-(m-1)) = fcoef2(nlong-(m-1)) &
                                          * rescalem * ((-1)**mod(m,2))

                    cilm(1,m1,m1) = cilm(1,m1,m1) + pm2 &
                                    * (fcoef1(m1) + fcoef2(m1))
                    cilm(2,m1,m1) = cilm(2,m1,m1) + pm2 * &
                                    (fcoef1(nlong-(m-1)) + fcoef2(nlong-(m-1)))
                                    ! fsymsign = 1

                    pm1 = z * ff1(m1+1,m1) * pm2

                    cilm(1,m1+1,m1) = cilm(1,m1+1,m1) + pm1 &
                                      * ( fcoef1(m1) - fcoef2(m1) )
                    cilm(2,m1+1,m1) = cilm(2,m1+1,m1) + pm1 * &
                                      (fcoef1(nlong-(m-1)) - fcoef2(nlong-(m-1)))
                                      ! fsymsign = -1

                    ffc1(-1) = fcoef1(m1) - fcoef2(m1)
                    ffc1(1) = fcoef1(m1) + fcoef2(m1)
                    ffc2(-1) = fcoef1(nlong-(m-1)) - fcoef2(nlong-(m-1))
                    ffc2(1) = fcoef1(nlong-(m-1)) + fcoef2(nlong-(m-1))

                    do l = m + 2, lmax_comp, 1
                        l1 = l + 1
                        p = z * ff1(l1,m1) * pm1-ff2(l1,m1) * pm2
                        pm2 = pm1
                        pm1 = p
                        cilm(1,l1,m1) = cilm(1,l1,m1) &
                                        + p * ffc1(fsymsign(l1,m1))
                        cilm(2,l1,m1) = cilm(2,l1,m1) &
                                        + p * ffc2(fsymsign(l1,m1))

                    end do

                end do

                rescalem = rescalem * u

                select case (lnorm)
                    case (1,4)
                        pmm = phase * pmm * sqr(2*lmax_comp+1) &
                              / sqr(2*lmax_comp) * rescalem
                    case (2)
                        pmm = phase * pmm / sqr(2*lmax_comp) * rescalem
                    case (3)
                        pmm = phase * pmm * (2*lmax_comp-1) * rescalem
                end select

                cilm(1,lmax_comp+1,lmax_comp+1) = &
                                cilm(1,lmax_comp+1,lmax_comp+1) + pmm * &
                                ( fcoef1(lmax_comp+1) + fcoef2(lmax_comp+1) )
                cilm(2,lmax_comp+1,lmax_comp+1) = &
                                cilm(2,lmax_comp+1,lmax_comp+1) &
                                + ((-1)**mod(lmax_comp,2)) * pmm * &
                                ( fcoef1(nlong-(lmax_comp-1)) &
                                + fcoef2(nlong-(lmax_comp-1)) )
                                ! fsymsign = 1

            end if

        end do

    end if

    call fftw_destroy_plan(plan)
    call fftw_destroy_plan(plans)

    !--------------------------------------------------------------------------
    !
    !   Divide by integral of Ylm*Ylm 
    !
    !--------------------------------------------------------------------------
    select case (lnorm)
        case (1)
            do l = 0, lmax_comp, 1
                cilm(1:2,l+1, 1:l+1) = cilm(1:2,l+1, 1:l+1) / (4*pi)

            end do

        case (2)
            do l = 0, lmax_comp, 1
                cilm(1:2,l+1, 1:l+1) = (2*l+1) * cilm(1:2,l+1, 1:l+1) / (4*pi)

            end do

        case (3)
            do l = 0, lmax_comp, 1
                prod = 4 * pi / dble(2*l+1)
                cilm(1,l+1,1) = cilm(1,l+1,1) / prod

                do m = 1, l - 1, 1
                    prod = prod * (l+m) * (l-m+1)
                    cilm(1:2,l+1,m+1) = cilm(1:2,l+1,m+1) / prod

                end do

                !do m=l case
                if (l /= 0) cilm(1:2,l+1,l+1) = cilm(1:2,l+1, l+1) / (prod*2*l)

            end do

    end select

end subroutine SHExpandGLQC
