! File: AdvancedProgram.f90
module MathOperations
  implicit none
  contains

  function add(a, b) result(sum)
    integer, intent(in) :: a, b
    integer :: sum
    sum = a + b
  end function add

  function subtract(a, b) result(difference)
    integer, intent(in) :: a, b
    integer :: difference
    difference = a - b
  end function subtract

end module MathOperations

module StringOperations
  implicit none
  contains

  function concatenate(str1, str2) result(concatenated_string)
    character(len=*), intent(in) :: str1, str2
    character(len=:), allocatable :: concatenated_string
    concatenated_string = trim(str1) // trim(str2)
  end function concatenate

  function string_length(str) result(len_str)
    character(len=*), intent(in) :: str
    integer :: len_str
    len_str = len_trim(str)
  end function string_length

end module StringOperations

program AdvancedTest
  use MathOperations
  use StringOperations
  implicit none
  integer :: x, y, result
  character(len=:), allocatable :: str1, str2, combined

  ! Math operations
  x = 5
  y = 3
  result = add(x, y)
  print *, 'The sum of', x, 'and', y, 'is', result
  result = subtract(x, y)
  print *, 'The difference between', x, 'and', y, 'is', result

  ! String operations
  str1 = "Hello, "
  str2 = "world!"
  combined = concatenate(str1, str2)
  print *, combined

end program AdvancedTest
