theory ShiftUp1PlusOne
  imports Main
begin

definition plus_one :: "int \<Rightarrow> int" where
"plus_one x = x + 1"

definition shift_up1 :: "(int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
"shift_up1 f x = f x + 1"

lemma shift_up1_plus_one: "shift_up1 plus_one x = x + 2"
  unfolding shift_up1_def plus_one_def
  by simp

end
