! This is a simple matrix multiplication program
module matrix_operations
  implicit none
  ! This module defines basic matrix operations
  
  contains
  
  subroutine matmul_custom(A, B, C, n)
    ! Custom matrix multiplication
    integer, intent(in) :: n
    real, intent(in) :: A(n,n), B(n,n)
    real, intent(out) :: C(n,n)
    integer :: i, j, k
    
    do i = 1, n
       do j = 1, n
          C(i,j) = 0.0
          do k = 1, n
             C(i,j) = C(i,j) + A(i,k)*B(k,j)
          end do
       end do
    end do
    
  end subroutine matmul_custom

end module matrix_operations

program matrix_main
  use matrix_operations
  implicit none
  real :: A(2,2) = reshape([1.0, 2.0, 3.0, 4.0], [2,2])
  real :: B(2,2) = reshape([2.0, 0.0, 1.0, 3.0], [2,2])
  real :: C(2,2)
  
  call matmul_custom(A, B, C, 2)
  
  print *, "Result:"
  print *, C
  
end program matrix_main
