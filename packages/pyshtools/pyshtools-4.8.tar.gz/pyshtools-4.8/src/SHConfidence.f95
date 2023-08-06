function SHConfidence(l_conf, r)
!------------------------------------------------------------------------------
!
!   This subroutine will calculate the probability that two sets of spherical
!   harmonic coefficients, which possess a correlation coefficients r, are
!   linearly correlated at a given degree. This is calucated according to
!   equation A7 in Pauer et al. (2007), which is from Eckhard 1984.
!
!   Calling Parameters
!
!       INPUT
!           l_conf      Degree to calculate confidence levels.
!           r           The correlation coefficient of two sets
!                       of spherical harmonic coeficients at degree l_conf.
!
!       OUTPUT
!           cl          The confidence level.
!
!   Copyright (c) 2005-2019, SHTOOLS
!   All rights reserved.
!
!------------------------------------------------------------------------------
    use ftypes

    implicit none

    real(dp) :: SHConfidence
    real(dp), intent(in) :: r
    integer(int32), intent(in) :: l_conf
    real(dp) :: prod
    integer(int32) :: l, i

    SHConfidence = abs(r)
    prod = 1.0_dp

    do l = 2, l_conf, 1
        i = l - 1
        prod = prod * dble(2*i-1) / dble(2*i)
        SHConfidence = SHConfidence + prod * abs(r) * (1.0_dp - r**2)**(l-1)
    end do

end function SHConfidence
