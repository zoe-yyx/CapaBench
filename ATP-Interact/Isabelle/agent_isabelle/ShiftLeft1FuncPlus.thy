theory ShiftLeft1FuncPlus
  imports Main
begin

definition func_plus :: "(int \<Rightarrow> int) \<Rightarrow> (int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
"func_plus f g x = f x + g x"
                                   
definition shift_left1 :: "(int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
"shift_left1 f x = f (x + 1)"

lemma shift_left1_func_plus: "shift_left1 (func_plus f g) = func_plus (shift_left1 f) (shift_left1 g)"
  unfolding shift_left1_def func_plus_def
  by auto

end
