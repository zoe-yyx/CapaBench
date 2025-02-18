open Classical

theorem notEx1 (n m : Int) : n < m ∨ ¬ n < m := by
  assume h : n < m
  have h1 : n + 1 < m + 1, from add_lt_add_right h 1
  have h2 : n + 1 < m, from h1.trans (lt_add_one m)
  have h3 : n < m - 1, from sub_lt_sub_left h 1
  have h4 : n < m, from h3.trans (lt_add_one m)
  contradiction
