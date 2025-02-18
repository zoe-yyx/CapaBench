theory ShiftUp1Square
  imports Main
begin

definition square :: "int \<Rightarrow> int" where
"square x = x * x"

definition shift_up1 :: "(int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
"shift_up1 f x = f x + 1"

lemma shift_up1_square: "shift_up1 square x = x * x + 1"
  unfolding shift_up1_def square_def
  by simp

end
