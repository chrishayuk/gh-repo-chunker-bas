program FibonacciCalculator

  implicit none
  integer :: n, i
  integer, allocatable :: fibonacci(:)

  ! Get user input
  print *, 'How many terms of Fibonacci sequence would you like to display?'
  read *, n

  ! Validate user input
  if (n <= 0) then
     print *, 'Please enter a positive number.'
     stop
  end if

  ! Allocate memory for Fibonacci sequence
  allocate(fibonacci(n))

  ! Initialize first two terms
  if (n >= 1) fibonacci(1) = 0
  if (n >= 2) fibonacci(2) = 1

  ! Calculate Fibonacci sequence
  do i = 3, n
     fibonacci(i) = fibonacci(i-1) + fibonacci(i-2)
  end do

  ! Display Fibonacci sequence
  print *, 'The first ', n, ' terms of the Fibonacci sequence are:'
  print *, fibonacci

  ! Free the allocated memory
  deallocate(fibonacci)

end program FibonacciCalculator
