theory SmulEx2
  imports Main
begin

definition smul :: "int \<Rightarrow> int \<Rightarrow> int" where
"smul x y = x * y + x + y"

lemma smul_ex2: "smul 2 3 = 11"
  unfolding smul_def
  by simp

end
