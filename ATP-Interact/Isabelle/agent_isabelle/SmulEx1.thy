theory SmulEx1
  imports Main
begin

definition smul :: "int \<Rightarrow> int \<Rightarrow> int" where
"smul x y = x * y + x + y"

lemma smul_ex1: "smul 1 1 = 3"
  unfolding smul_def
  by simp

end
