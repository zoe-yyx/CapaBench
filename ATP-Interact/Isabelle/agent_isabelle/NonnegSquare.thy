theory NonnegSquare
  imports Main
begin

definition square :: "int \<Rightarrow> int" where
"square x = x * x"

definition nonneg :: "int \<Rightarrow> bool" where
"nonneg x = (x \<ge> 0)"

lemma nonneg_square: "nonneg (square x)"
  unfolding nonneg_def square_def
  using zero_le_power2 by simp

end
