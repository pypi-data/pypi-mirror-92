function SHSjkPG(incspectra, l, m, mprime, hj_real, hk_real, mj, mk, lwin, &
                 hkcc)
!------------------------------------------------------------------------------
!
!   This function will compute the expected windowed cross-power spectra for
!   two fields, which are windowed by tapers j and k. This corresponds to the
!   variable:
!
!        m(j)      m2(k)*
!   < Phi     Gamma      >
!        l         l
!
!   This routine will only work with tapers that are solutions to the spherical
!   cap concentration problem.
!
!   Calling Parameteters
!
!       IN
!           incspectra      Known input (cross) power spectra
!                           as a function of degree.
!           l, m, mprime    Angular degree and order.
!           hj, hk          Real vectors of length lwin+1 containing the
!                           the real spherical harmonic coefficients of the
!                           spherical cap concentration problem.
!           mj, mk          Angular orders of the two windows
!           lwin            Spherical harmonic bandwidth of the windows.
!           hkcc            If 1, the complex conjugate of the second window hk
!                           will be taken. If 2, it will remain as is.
!
!   Copyright (c) 2005-2019, SHTOOLS
!   All rights reserved.
!
!------------------------------------------------------------------------------
    use SHTOOLS, only: Wigner3j
    use ftypes

    implicit none

    complex(dp) :: SHSjkPG
    real(dp), intent(in) :: incspectra(:), hj_real(:), hk_real(:)
    integer(int32), intent(in) :: lwin, l, m, mprime, mj, mk, hkcc
    integer(int32) :: i, l1, l3, imin, imax, m1, m3, m2, l10min, l10max, &
                      l1min, l1max, l30min, l30max, l3min, l3max
    complex(dp) :: hj(lwin+1), hk(lwin+1), tj(lwin+1), tk(lwin+1), sum2, &
                   sum3, sum4
    real(dp) :: wl10(lwin+l+1), wl30(lwin+l+1), wl1(lwin+l+1), wl3(lwin+l+1), &
              sum1

    if (size(hj_real) < lwin+1) then
        print*, "Error --- SHSjkPG"
        print*, "HJ_REAL must be dimensioned as (LWIN+1), where LWIN is ", lwin
        print*, "Input array is dimensioned ", size(hj_real)
        stop

    else if (size(hk_real) < lwin+1) then
        print*, "Error --- SHSjkPG"
        print*, "HK_REAL must be dimensioned as (LWIN+1), where LWIN is ", lwin
        print*, "Input array is dimensioned ", size(hk_real)
        stop

    else if(size(incspectra(:)) < l+lwin+1) then
        print*, "Error --- SHSjkPG"
        print*, "INCSPECTRA must be dimensioned as (L+LWIN+1), where " // &
                "L and LWIN are ", l, lwin
        print*, "Input array is dimensioned ", size(incspectra)
        stop

    else if (hkcc > 2 .or. hkcc < 1) then
        print*, "Error --- SHSjkPG"
        print*, "HKCC must be either 1 or 2."
        print*, "Input parameter is equal to ", hkcc
        stop

    end if

    SHSjkPG = cmplx(0.0_dp, 0.0_dp, dp)

    if (l < abs(m) .or. l < abs(mprime)) return
    !--------------------------------------------------------------------------
    !
    !   Convert real coefficients to comlex form. This is only done for m>0.
    !   Negative orders are obtained from the relationship
    !   f_{lm} = (-1)^m f_{l-m}^*
    !
    !--------------------------------------------------------------------------
    if (mj == 0) then
        hj(1:lwin+1) = cmplx(hj_real(1:lwin+1), 0.0_dp, dp)

    else if (mj > 0) then
        hj(1:lwin+1) = cmplx(hj_real(1:lwin+1), 0.0_dp, dp) / sqrt(2.0_dp)

    else
        hj(1:lwin+1) = cmplx(0.0_dp, -hj_real(1:lwin+1), dp) / sqrt(2.0_dp)

    end if

    if (mk == 0) then
        hk(1:lwin+1) = cmplx(hk_real(1:lwin+1), 0.0_dp, dp)

    else if (mk > 0) then
        hk(1:lwin+1) = cmplx(hk_real(1:lwin+1), 0.0_dp, dp) / sqrt(2.0_dp)

    else
        hk(1:lwin+1) = cmplx(0.0_dp, -hk_real(1:lwin+1), dp) / sqrt(2.0_dp)

    end if

    if (hkcc == 1) hk = conjg(hk)

    !--------------------------------------------------------------------------
    !
    !   Calculate function
    !
    !--------------------------------------------------------------------------
    do l1 = abs(mj), lwin, 1
        sum4 = cmplx(0.0_dp, 0.0_dp, dp)

        call Wigner3j(wl10, l10min, l10max, l, l1, 0, 0, 0)

        do l3 = abs(mj), lwin, 1
            sum3 = cmplx(0.0_dp, 0.0_dp, dp)

            if (mod(l1+l3,2) == 0) then
                call Wigner3j(wl30, l30min, l30max, l, l3, 0, 0, 0)

                do m1 = -abs(mj), abs(mj), max(2*abs(mj), 1)
                    sum2 = cmplx(0.0_dp, 0.0_dp, dp)

                    if (m1 < 0) then
                        tj = conjg(hj) * (-1)**m1
                    else
                        tj = hj
                    end if

                    do m3 = -abs(mk), abs(mk), max(2*abs(mk), 1)
                        sum1 = 0.0_dp

                        if (m - m1 == mprime - m3) then
                            if (m3 < 0) then
                                tk = conjg(hk) * (-1)**m3
                            else
                                tk = hk
                            end if

                            m2 = m - m1

                            call Wigner3j(wl1, l1min, l1max, l, l1, m2, -m, m1)
                            call Wigner3j(wl3, l3min, l3max, l, l3, m2, &
                                          -mprime, m3)

                            imin = max(l1min, l3min)
                            imax = min(l1max, l3max)

                            if (mod(imin+l1+l,2) /= 0) imin = imin + 1
                            ! both mod(i+l1+l,2) and mod(i+l3+l,2) must be 0

                            do i = imin, imax, 2
                                sum1 = sum1 + incspectra(i+1) * &
                                       wl10(i-l10min+1) * &
                                       wl30(i-l30min+1) * wl1(i-l1min+1) &
                                       * wl3(i-l3min+1)
                            end do

                            sum2 = sum2 + sum1 * tk(l3+1)

                        end if

                    end do

                    sum3 = sum3 + sum2 * tj(l1+1)

                end do

            end if

            sum4 = sum4 + sum3 * sqrt(2.0_dp * l3 + 1.0_dp)

        end do

        SHSjkPG = SHSjkPG + sum4 * sqrt(2.0_dp * l1 + 1.0_dp)

    end do

    SHSjkPG = SHSjkPG * (2.0_dp * l + 1.0_dp)

end function SHSjkPG
