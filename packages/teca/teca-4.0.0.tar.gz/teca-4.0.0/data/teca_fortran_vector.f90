module teca_@name@_vec_module
  use ISO_C_BINDING
  use ISO_FORTRAN_ENV, only : ERROR_UNIT

  type teca_@name@_vec
    @type@, pointer, dimension(:) :: m_data
    integer*8 m_data_at
    integer*8 m_data_end
    logical m_own
  end type

  type p_teca_@name@_vec
    type(teca_@name@_vec), pointer :: vec
  end type

  type teca_@name@_vec_vec
    type(p_teca_@name@_vec), pointer, dimension(:) :: vec
    integer*8 :: vec_size
  end type

  interface new_teca_@name@_vec
    module procedure new_teca_@name@_vec_default
    module procedure new_teca_@name@_vec_copy
    module procedure new_teca_@name@_vec_zero_copy
  end interface

  interface teca_@name@_vec_append
    module procedure teca_@name@_vec_append_n
    module procedure teca_@name@_vec_append_range
  end interface

contains


!----------------------------------------------------------------------------
function new_teca_@name@_vec_default() result(vec)
  implicit none
  type(teca_@name@_vec), pointer :: vec
  integer i_err

  allocate(vec, stat = i_err)
  if (i_err.ne.0) then
    write(ERROR_UNIT, *)"Error: Failed to allocate object teca_@name@_vec."
    stop
  end if

  vec%m_data => null()
  vec%m_data_end = 0
  vec%m_data_at = 1
  vec%m_own = .true.

  call teca_@name@_vec_realloc(vec, 16_8)

end function

!----------------------------------------------------------------------------
function new_teca_@name@_vec_zero_copy(a_data, a_data_size) result(vec)
  implicit none
  type(teca_@name@_vec),  pointer :: vec
  @type@, pointer, dimension(:) :: a_data
  integer*8 a_data_size
  integer i_err

  allocate(vec, stat = i_err)
  if (i_err.ne.0) then
    write(ERROR_UNIT, *)"Error: Failed to allocate object teca_@name@_vec."
    stop
  end if

  vec%m_data => a_data
  vec%m_data_end = a_data_size
  vec%m_data_at = a_data_size
  vec%m_own = .false.

end function


!----------------------------------------------------------------------------
function new_teca_@name@_vec_copy(other) result(vec)
  implicit none
  type(teca_@name@_vec),  pointer :: vec
  type(teca_@name@_vec) other
  integer i_err

  allocate(vec, stat = i_err)
  if (i_err.ne.0) then
    write(ERROR_UNIT, *)"Error: Failed to allocate object teca_@name@_vec."
    stop
  end if

  call teca_@name@_vec_truncate(vec)
  call teca_@name@_vec_append(vec, other%m_data, teca_@name@_vec_get_size(other))

end function

!----------------------------------------------------------------------------
subroutine delete_teca_@name@_vec(vec)
  implicit none
  type(teca_@name@_vec),  pointer :: vec

  if (.not.associated(vec)) return

  if (vec%m_own .and. associated(vec%m_data)) then
    deallocate(vec%m_data)
  end if
  nullify(vec%m_data)

  deallocate(vec)
  nullify(vec)

end subroutine

!---------------------------------------------------------------------------
function teca_@name@_vec_get_size(vec) result(n)
  implicit none
  type(teca_@name@_vec) vec
  integer*8 n

  n = vec%m_data_at - 1

end function

!---------------------------------------------------------------------------
subroutine teca_@name@_vec_truncate(vec)
  implicit none
  type(teca_@name@_vec) vec

  vec%m_data_at = 1

end subroutine

!----------------------------------------------------------------------------
function teca_@name@_vec_get_allocated_size(vec) result(n)
  implicit none
  type(teca_@name@_vec) vec
  integer*8 n

  n = vec%m_data_end

end function

!----------------------------------------------------------------------------
function teca_@name@_vec_get_free_space(vec) result(n)
  implicit none
  type(teca_@name@_vec) vec
  integer*8 n

  n = vec%m_data_end - vec%m_data_at + 1

end function

!----------------------------------------------------------------------------
subroutine teca_@name@_vec_realloc(vec, n)
  implicit none
  type(teca_@name@_vec) vec
  @type@, pointer, dimension(:) :: new_data
  integer*8 n, m, i
  integer i_err

  ! requested size is smaller then the current size
  m = teca_@name@_vec_get_size(vec)
  if (n .le. m) then
      if (vec%m_data_at .ge. n) then
          vec%m_data_at = 1
      end if
      return
  end if

  ! allocte the new array
  allocate(new_data(n), stat = i_err)
  if (i_err .ne. 0) then
    write(ERROR_UNIT, *)"Error: Failed to allocate new_data."
    stop
  end if

  ! copy
  do i = 1, m
    new_data(i) = vec%m_data(i)
  end do

  ! initialize remainder
  !do i = m + 1, n
  !  new_data(i) = @val@
  !end do

  !  free the old array
  if (vec%m_own .and. associated(vec%m_data)) then
    deallocate(vec%m_data)
  end if

  ! asign
  vec%m_data => new_data
  vec%m_data_end = n
  vec%m_own = .true.

end subroutine

!----------------------------------------------------------------------------
subroutine teca_@name@_vec_push(vec, val)
  implicit none
  type(teca_@name@_vec) vec
  @type@ val
  @type@ a_data(1)

  a_data(1) = val
  call teca_@name@_vec_append_range(vec, a_data, 1_8, 1_8)

end subroutine

!----------------------------------------------------------------------------
function teca_@name@_vec_pop(vec) result(a_data)
  implicit none
  type(teca_@name@_vec) vec
  @type@ a_data

  vec%m_data_at = vec%m_data_at - 1

  a_data = vec%m_data(vec%m_data_at)

end function

!----------------------------------------------------------------------------
subroutine teca_@name@_vec_append_n(vec, a_data, n)
  implicit none
  type(teca_@name@_vec) vec
  @type@ a_data(:)
  integer*8 n

  call teca_@name@_vec_append_range(vec, a_data, 1_8, n)

end subroutine

!----------------------------------------------------------------------------
subroutine teca_@name@_vec_append_range(vec, a_data, start_id, end_id)
  implicit none
  type(teca_@name@_vec) vec
  @type@ a_data(:)
  integer*8 i, j
  integer*8 req_size, cur_size, new_size, start_id, end_id, a_data_size

  a_data_size = end_id - start_id + 1

  ! resize
  req_size = teca_@name@_vec_get_size(vec) + a_data_size
  cur_size = teca_@name@_vec_get_allocated_size(vec)

  if (req_size.gt.cur_size) then
    new_size = cur_size
    do
      if (req_size.le.new_size) exit
      new_size = 2*new_size
    end do

    call teca_@name@_vec_realloc(vec, new_size)

  end if

  ! append
  i = vec%m_data_at
  do j = start_id, end_id
    vec%m_data(i) = a_data(j)
    i = i + 1
  end do

  vec%m_data_at = vec%m_data_at + a_data_size

end subroutine

!----------------------------------------------------------------------------
subroutine teca_@name@_vec_write(vec, unit_no, i_err)
  implicit none
  type(teca_@name@_vec) vec
  integer unit_no
  integer n
  integer i_err
  character(len = 256) e_str

  n = teca_@name@_vec_get_size(vec)

  ! write(unit = unit_no, fmt = '(A, I5)')'Data_at = ', vec%m_data_at
  ! write(unit = unit_no, fmt = '(A, I5)')'Data_end = ', vec%m_data_end
  ! write(unit = unit_no, fmt = '(A, I5)')'Size = ', n

  write(unit = unit_no, iostat = i_err, iomsg = e_str)vec%m_data(1:n)
  if (i_err.ne.0) then
    write(ERROR_UNIT, *)"Error: ", trim(e_str)
    write(ERROR_UNIT, *)"Error: Failed to write file."
    return
  end if

end subroutine

!----------------------------------------------------------------------------
function new_teca_@name@_vec_vec(n) result(vec_vec)
  implicit none
  integer*8, intent(in) :: n
  integer*8 :: i, i_err
  type(teca_@name@_vec_vec), pointer :: vec_vec
  type(p_teca_@name@_vec), pointer, dimension(:) :: tmp_vec

  allocate(vec_vec, stat = i_err)
  if (i_err.ne.0) then
    write(ERROR_UNIT, *)"Error: Failed to allocate object teca_@name@_vec_vec."
    stop
  end if

  allocate(tmp_vec(n), stat = i_err)
  if (i_err .ne. 0) then
    write(ERROR_UNIT, *)"Error: Failed to allocate new_data."
    stop
  end if

  do i = 1,n
    tmp_vec(i)%vec => new_teca_@name@_vec()
  end do

  vec_vec%vec => tmp_vec
  vec_vec%vec_size = n

end function

!----------------------------------------------------------------------------
subroutine delete_teca_@name@_vec_vec(vec_vec)
  implicit none
  integer*8 :: i
  integer i_err
  type(teca_@name@_vec_vec), pointer :: vec_vec

  do i = 1,vec_vec%vec_size
    if (associated(vec_vec%vec(i)%vec)) then
      deallocate(vec_vec%vec(i)%vec)
      nullify(vec_vec%vec(i)%vec)
    end if
  end do

  if (associated(vec_vec)) then
     deallocate(vec_vec)
     nullify(vec_vec)
  end if

end subroutine

end module
