theory Square5
  imports Main
begin

definition square :: "int \<Rightarrow> int" where
"square x = x * x"

lemma square_5: "square 5 = 25"
  unfolding square_def
  by simp

end
