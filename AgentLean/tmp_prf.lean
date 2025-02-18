theorem fourIsEven : ∃ n, 4 = n + n := by
  assume n : ℤ
  cases n with
  | zero => 
    use 2
    linarith
  | nonzero => 
    have h : 4 - n = n, by simp
    linarith
