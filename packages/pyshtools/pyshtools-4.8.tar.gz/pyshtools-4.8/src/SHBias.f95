subroutine SHBias(Shh, lwin, incspectra, ldata, outcspectra, save_cg, &
                  exitstatus)
!------------------------------------------------------------------------------
!
!   This subroutine will compute the expected windowed (cross-)power spectra
!   given the power spectrum of an arbitrary window, and the "known" input
!   (cross-)power spectra. Note that this routine makes the assumption that
!   the known spectra can be described as a random variable.
!
!   Calling Parameteters
!
!       IN
!           Shh         Window power spectrum.
!           lwin        Maximum spherical harmonic degree of the window.
!           incspectra  Known input (cross-)power spectrum as a function of
!                       degree.
!           ldata       Maximum degree of incspectra. Beyong this degree
!                       incspectra is assumed to be zero.
!
!       OUT 
!           outcspectra Biased estimate of the windowed
!                       power spectra. Maximum degree calculated is equal
!                       to lwin + ldata, or the dimension of outcspectra.
!
!       IN, OPTIONAL
!           save_cg     If 1, the Clebsch-Gordon coefficients will be calculated
!                       and saved, and then used in all subsequent calls
!                       (if lwin and ldata are not changed).
!                       If -1, the allocated memory for these terms will be
!                       deallocated.
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
    use SHTOOLS, only: Wigner3j
    use ftypes

    implicit none

    real(dp), intent(in) :: Shh(:), incspectra(:)
    real(dp), intent(out) :: outcspectra(:)
    integer(int32), intent(in) :: lwin, ldata
    integer(int32), intent(in), optional :: save_cg
    integer(int32), intent(out), optional :: exitstatus
    integer(int32) :: l, i, j, lmax, imin, imax, astat
    real(dp) :: wig(2*lwin+ldata+1)
    real(dp), allocatable, save :: cg2(:,:,:)

!$OMP   threadprivate(cg2)

    if (present(exitstatus)) exitstatus = 0

    lmax = ldata + lwin
    outcspectra = 0.0_dp

    if (size(Shh) < lwin+1) then
        print*, "Error --- SHBias"
        print*, "SHH must be dimensioned as (LWIN+1) where LWIN is ", lwin
        print*, "Input array is dimensioned as ", size(Shh)
        if (present(exitstatus)) then
            exitstatus = 1
            return
        else
            stop
        end if

    else if (size(incspectra) < ldata+1) then
        print*, "Error --- SHBias"
        print*, "INCSPECTRA must be dimensioned as (LDATA+1) " // &
                "where LDATA is ", ldata
        print*, "Input array is dimensioned as ", size(incspectra)
        if (present(exitstatus)) then
            exitstatus = 1
            return
        else
            stop
        end if

    end if

    if (present(save_cg)) then
        if (save_cg /= 1 .and. save_cg /= -1 .and. save_cg /= 0) then
            print*, "Error --- SHBias"
            print*, "SAVE_CG must be 1 (to save the Clebsch-Gordon " // &
                    "coefficients), -1 (to deallocate the memory), " // &
                    "or 0 (to do nothing)."
            print*, "Input value is ", save_cg
            if (present(exitstatus)) then
                exitstatus = 2
                return
            else
                stop
            end if

        end if

    end if

    !--------------------------------------------------------------------------
    !
    !   Calculate the biased power spectrum
    !
    !--------------------------------------------------------------------------
    if (present(save_cg)) then
        if (save_cg == -1) then
            if (allocated(cg2)) deallocate(cg2)
            return

        else if (save_cg == 0) then
            do l = 0, min(lmax, size(outcspectra)-1)
                do j = 0, lwin
                    if (present(exitstatus)) then
                        call Wigner3j(wig, imin, imax, j, l, 0, 0, 0, &
                                      exitstatus = exitstatus)
                        if (exitstatus /= 0) return
                    else
                        call Wigner3j(wig, imin, imax, j, l, 0, 0, 0)
                    end if

                    do i = imin, min(imax, ldata), 2
                        outcspectra(l+1) = outcspectra(l+1) + Shh(j+1) &
                                           * incspectra(i+1) * (2.0_dp*l+1.0_dp) &
                                           * wig(i-imin+1)**2
                    end do

                end do

            end do

            return

        end if

        if (allocated(cg2) .and. (size(cg2(:,1,1)) /= lmax+1 .or. &
                size(cg2(1,:,1)) /= lwin+1 .or. &
                size(cg2(1,1,:)) /= lmax+lwin+1) ) deallocate(cg2)

        if (.not. allocated(cg2)) then
            allocate (cg2(lmax+1, lwin+1, lmax+lwin+1), stat = astat)
            
            if (astat /= 0) then
                print*, "Error --- SHBias"
                print*, "Problem allocating internal array CG2"
                if (present(exitstatus)) then
                    exitstatus = 3
                    return
                else
                    stop
                end if

            end if

            cg2 = 0.0_dp

            do l = 0, lmax
                do j = 0, lwin
                    if (present(exitstatus)) then
                        call Wigner3j(wig, imin, imax, j, l, 0, 0, 0, &
                                      exitstatus = exitstatus)
                        if (exitstatus /= 0) return
                    else
                        call Wigner3j(wig, imin, imax, j, l, 0, 0, 0)
                    end if

                    cg2(l+1,j+1,1:imax-imin+1) = (2.0_dp*l+1.0_dp) &
                                                 * wig(1:imax-imin+1)**2
                end do
            end do

        end if

        do l = 0, min(lmax, size(outcspectra)-1)
            do j = 0, lwin
                imin = abs(j-l)
                imax = j + l

                do i = imin, min(imax, ldata), 2
                    outcspectra(l+1) = outcspectra(l+1) + Shh(j+1) &
                                       * incspectra(i+1) &
                                       * cg2(l+1,j+1,i-imin+1)
                end do

            end do

        end do

    else
        do l = 0, min(lmax, size(outcspectra)-1)
            do j = 0, lwin
                if (present(exitstatus)) then
                    call Wigner3j(wig, imin, imax, j, l, 0, 0, 0, &
                                    exitstatus = exitstatus)
                    if (exitstatus /= 0) return
                else
                    call Wigner3j(wig, imin, imax, j, l, 0, 0, 0)
                end if

                do i = imin, min(imax, ldata), 2
                    outcspectra(l+1) = outcspectra(l+1) + Shh(j+1) &
                                       * incspectra(i+1) * (2.0_dp*l+1.0_dp) &
                                       * wig(i-imin+1)**2
                end do

            end do

        end do

    end if

end subroutine SHBias
