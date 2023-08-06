subroutine SHBiasK(tapers, lwin, k, incspectra, ldata, outcspectra, &
                   taper_wt, save_cg, exitstatus)
!------------------------------------------------------------------------------
!
!   This subroutine will compute the expected multitaper windowed (cross-)power
!   spectra using the first K tapers of the spherical-cap concentration problem
!   for a given input (cross-)power spectrum. Note that this routine makes the
!   assumption that the known spectrum can be described as a random variable.
!   If the input spectrum is a cross-power spectra, then it is assumed that the
!   two fields are linearly related. The default is to apply an equal weight to
!   each expected spectrum, but this can be changed by specifying the optional
!   arguement taper_wt. The sum of taper_wt will be normalized to unity.
!
!   Calling Parameteters
!
!       IN
!           tapers      The coefficients of the tapers (lwin+1, >= k)
!                       corresponding to the spherical cap concentration
!                       problem, where each column corresponds to the
!                       coefficients for a given value of m. Note the the exact
!                       value of m is not important for this routine.
!           lwin        Maximum spherical harmonic degree of the window
!                       coefficients.
!           incspectra  Knonw input (cross-)power spectrum as a function of
!                       degree.
!           ldata       Maximum degree of incspectra. Beyong this degree
!                       incspectra is assumed to be zero.
!
!       IN (Optional)
!           taper_wt    Vector of length k corresponding to the weights
!                       applied to each spectal estimate. The sum of taper_wt
!                       will be normalized to unity.
!           save_cg     If 1, the Clebsch-Gordon coefficients will be calculated
!                       and saved, and then used in all subsequent calls (if
!                       lwin and ldata are not changed). If -1, the allocated
!                       memory for these terms will be deallocated.
!
!       OUT 
!           outcspectra Biased estimate of the windowed power spectra. Maximum
!                       degree calculated is equal to lwin + ldata, or the
!                       dimension of outspectra.
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

    real(dp), intent(in) :: tapers(:,:), incspectra(:)
    real(dp), intent(out) :: outcspectra(:)
    integer(int32), intent(in) :: lwin, ldata, k
    real(dp), intent(in), optional :: taper_wt(:)
    integer(int32), intent(in), optional :: save_cg
    integer(int32), intent(out), optional :: exitstatus
    integer(int32) :: l, i, j, lmax, imin, imax, n, astat
    real(dp) :: wig(2*lwin+ldata+1)
    real(dp), allocatable, save :: cg2(:,:,:)

!$OMP   threadprivate(cg2)

    if (present(exitstatus)) exitstatus = 0

    lmax = ldata + lwin
    outcspectra = 0.0_dp

    if (size(tapers(:,1)) < lwin+1 .or. size(tapers(1,:)) < k) then
        print*, "Error --- SHBiasK"
        print*, "TAPERS must be dimensioned as (LWIN+1, K) where " // &
                "LWIN and K are ", LWIN, K
        print*, "Input array is dimensioned ", size(tapers(:,1)), &
                size(tapers(1,:))
        if (present(exitstatus)) then
            exitstatus = 1
            return
        else
            stop
        end if

    else if (size(incspectra) < ldata +1) then
        print*, "Error --- SHBiasK"
        print*, "INCSPECTRA must be dimensioned as (LDATA+1) where " // &
                "LDATA is ", ldata
        print*, "Input array is dimensioned ", size(incspectra)
        if (present(exitstatus)) then
            exitstatus = 1
            return
        else
            stop
        end if

    end if

    if (present(taper_wt)) then
        if (size(taper_wt) < k) then 
            print*, "Error --- SHBiasK"
            print*, "TAPER_WT must be dimensioned as (K) " // &
                    "where K is ", k
            print*, "Input array is dimensioned as ", size(taper_wt)
        if (present(exitstatus)) then
            exitstatus = 1
            return
        else
            stop
        end if

        else if (sum(taper_wt(1:k)) /= 1.0_dp) then
            print*, "Error --- SHBiasK"
            print*, "TAPER_WT must sum to unity."
            print*, "Input array sums to ", sum(taper_wt(1:k))
            if (present(exitstatus)) then
                exitstatus = 5
                return
            else
                stop
            end if

        end if

    end if

    if (present(save_cg)) then
        if (save_cg /= 1 .and. save_cg /= -1 .and. save_cg /= 0) then
            print*, "Error --- SHBiasK"
            print*, "SAVE_CG must be 1 (to save the Clebsch-Gordon " // &
                    "coefficients), -1 (to deallocate the memory)" 
            print*, "or 0 (to do nothing)."
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
            if (allocated (cg2)) deallocate (cg2)
            return

        else if (save_cg == 0) then
            if (present(taper_wt)) then
                do l = 0, min(lmax, size(outcspectra)-1)
                    do j = 0, lwin
                        if (present(exitstatus)) then
                            call Wigner3j(wig, imin, imax, j, l, 0, 0, 0, &
                                          exitstatus = exitstatus)
                            if (exitstatus /= 0) return
                        else
                            call Wigner3j(wig, imin, imax, j, l, 0, 0, 0)
                        end if

                        do i = imin, min(imax,ldata), 2
                            do n = 1, k
                                outcspectra(l+1) = outcspectra(l+1) &
                                                   + taper_wt(n) &
                                                   * tapers(j+1,n)**2 &
                                                   * incspectra(i+1) &
                                                   * (2.0_dp*l+1.0_dp) &
                                                   * wig(i-imin+1)**2
                            end do

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

                        do i = imin, min(imax,ldata), 2
                            do n = 1, k
                                outcspectra(l+1) = outcspectra(l+1) &
                                                   + tapers(j+1,n)**2 &
                                                   * incspectra(i+1) &
                                                   * (2.0_dp*l+1.0_dp) &
                                                   * wig(i-imin+1)**2
                            end do

                        end do

                    end do

                end do

                outcspectra = outcspectra / dble(k)

            end if

            return

        end if

        if (allocated(cg2) .and. (size(cg2(:,1,1)) /= lmax+1 .or. &
                size(cg2(1,:,1)) /= lwin+1 .or. &
                size(cg2(1,1,:)) /= lmax+lwin+1) ) deallocate (cg2)

        if (.not. allocated(cg2)) then
            allocate (cg2(lmax+1, lwin+1, lmax+lwin+1), stat = astat)

            if (astat /= 0) then
                print*, "Error --- SHBiasK"
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

        if (present(taper_wt)) then
            do l = 0, min(lmax, size(outcspectra)-1)
                do j = 0, lwin
                    imin = abs(j-l)
                    imax = j + l

                    do i = imin, min(imax,ldata), 2
                        do n = 1, k
                            outcspectra(l+1) = outcspectra(l+1) + taper_wt(n) &
                                               * tapers(j+1,n)**2 &
                                               * incspectra(i+1) &
                                               * cg2(l+1,j+1,i-imin+1)
                        end do

                    end do

                end do

            end do

        else
            do l = 0, min(lmax, size(outcspectra)-1)
                do j = 0, lwin
                    imin = abs(j-l)
                    imax = j + l

                    do i = imin, min(imax,ldata), 2
                        do n = 1, k
                            outcspectra(l+1) = outcspectra(l+1) &
                                               + tapers(j+1,n)**2 &
                                               * incspectra(i+1) &
                                               * cg2(l+1,j+1,i-imin+1)
                        end do

                    end do

                end do

            end do

            outcspectra = outcspectra / dble(k)

        end if

    else
        if (present(taper_wt)) then
            do l = 0, min(lmax, size(outcspectra)-1)
                do j = 0, lwin
                    if (present(exitstatus)) then
                        call Wigner3j(wig, imin, imax, j, l, 0, 0, 0, &
                                      exitstatus = exitstatus)
                        if (exitstatus /= 0) return
                    else
                        call Wigner3j(wig, imin, imax, j, l, 0, 0, 0)
                    end if

                    do i = imin, min(imax,ldata), 2
                        do n = 1, k
                            outcspectra(l+1) = outcspectra(l+1) + taper_wt(n) &
                                               * tapers(j+1,n)**2 &
                                               * incspectra(i+1) &
                                               * (2.0_dp*l+1.0_dp) &
                                               * wig(i-imin+1)**2
                        end do

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

                    do i = imin, min(imax,ldata), 2
                        do n = 1, k
                            outcspectra(l+1) = outcspectra(l+1) &
                                               + tapers(j+1,n)**2 &
                                               * incspectra(i+1) &
                                               * (2.0_dp*l+1.0_dp) &
                                               * wig(i-imin+1)**2
                        end do

                    end do

                end do

            end do

            outcspectra = outcspectra / dble(k)

        end if

    end if

end subroutine SHBiasK
