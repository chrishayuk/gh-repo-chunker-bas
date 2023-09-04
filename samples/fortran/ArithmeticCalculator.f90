program ArithmeticCalculator
  implicit none
  real :: a, b, result

  print *, 'Enter two numbers:'
  read *, a, b

  call add(a, b, result)
  print *, 'Sum =', result

  call subtract(a, b, result)
  print *, 'Difference =', result

  call multiply(a, b, result)
  print *, 'Product =', result

  call divide(a, b, result)
  print *, 'Quotient =', result

contains

  subroutine add(x, y, z)
    implicit none
    real, intent(in) :: x, y
    real, intent(out) :: z
    z = x + y
  end subroutine add

  subroutine subtract(x, y, z)
    implicit none
    real, intent(in) :: x, y
    real, intent(out) :: z
    z = x - y
  end subroutine subtract

  subroutine multiply(x, y, z)
    implicit none
    real, intent(in) :: x, y
    real, intent(out) :: z
    z = x * y
  end subroutine multiply

  subroutine divide(x, y, z)
    implicit none
    real, intent(in) :: x, y
    real, intent(out) :: z
    if (y /= 0) then
      z = x / y
    else
      print *, 'Division by zero!'
      z = 0.0
    end if
  end subroutine divide

end program ArithmeticCalculator
