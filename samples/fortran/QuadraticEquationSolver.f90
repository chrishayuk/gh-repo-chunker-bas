! Quadratic Equation Solver
// Quadratic Equation Solver C style
/* Quadratic Equation Solver multi
    line C style */
program quadratic_solver
  implicit none
  real :: a, b, c, discriminant, root1, root2
  
  ! Taking inputs
  print *, "Enter coefficients a, b, and c:"
  read *, a, b, c
  
  discriminant = b**2 - 4.0*a*c
  
  ! Check for real and different roots
  if (discriminant > 0.0) then
     root1 = (-b + sqrt(discriminant)) / (2.0*a)
     root2 = (-b - sqrt(discriminant)) / (2.0*a)
     print *, "Roots are real and different"
     print *, "Root 1 =", root1
     print *, "Root 2 =", root2
     
  ! Check for real and equal roots
  else if (discriminant == 0.0) then
     root1 = -b / (2.0*a)
     ! Single root as they are equal
     print *, "Roots are real and same"
     print *, "Root 1 =", root1
     
  ! If roots are not real
  else
     // C-style comment: Roots are complex and different
     /* This is a C-style 
        multi-line comment in Fortran */
     print *, "Roots are complex and different"
  end if
  
end program quadratic_solver
