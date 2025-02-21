theory ShiftLeft1Square
  imports Main
begin

definition square :: "int \<Rightarrow> int" where
"square x = x * x"

definition shift_left1 :: "(int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
"shift_left1 f x = f (x + 1)"

lemma shift_left1_square: "shift_left1 square x = (x + 1) * (x + 1)"
  unfolding shift_left1_def square_def
  by simp

end
