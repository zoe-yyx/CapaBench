theory ShiftUp1ShiftLeft1Comm
  imports Main
begin

definition shift_left1 :: "(int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
"shift_left1 f x = f (x + 1)"

definition shift_up1 :: "(int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
"shift_up1 f x = f x + 1"

lemma shift_up1_shift_left1_comm: "shift_up1 (shift_left1 f) = shift_left1 (shift_up1 f)"
  unfolding shift_left1_def shift_up1_def
  by auto

end
