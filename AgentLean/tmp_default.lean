theorem sum_of_sqr_lt (x y : ℤ) (h : x < y) : x * x + x * y + y * y > 0 := by
  simp [add_assoc, add_comm (x * x) (x * y), add_assoc (x * x) (x * y) y * y]
  linarith [h]
