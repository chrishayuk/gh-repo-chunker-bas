program FactorialCalculator
  implicit none
  integer :: n
  integer :: fact_iterative, fact_recursive

  print *, 'Enter a positive integer:'
  read *, n

  if (n >= 0) then
    print *, 'Iterative factorial of', n, 'is', factorial_iterative(n)
    print *, 'Recursive factorial of', n, 'is', factorial_recursive(n)
  else
    print *, 'Please enter a non-negative number.'
  end if

contains

  function factorial_iterative(x) result(res)
    implicit none
    integer, intent(in) :: x
    integer :: res, i
    res = 1
    do i = 1, x
      res = res * i
    end do
  end function factorial_iterative

  recursive function factorial_recursive(x) result(res)
    implicit none
    integer, intent(in) :: x
    integer :: res
    if (x == 0) then
      res = 1
    else
      res = x * factorial_recursive(x-1)
    end if
  end function factorial_recursive

end program FactorialCalculator
