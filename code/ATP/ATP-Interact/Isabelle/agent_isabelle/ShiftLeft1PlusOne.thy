theory ShiftLeft1PlusOne
  imports Main
begin

definition plus_one :: "int \<Rightarrow> int" where
"plus_one x = x + 1"

definition shift_left1 :: "(int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
"shift_left1 f x = f (x + 1)"

lemma shift_left1_plus_one: "shift_left1 plus_one x = x + 2"
  unfolding shift_left1_def plus_one_def
  by simp

end
