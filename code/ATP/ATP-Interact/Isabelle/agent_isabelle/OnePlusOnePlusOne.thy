theory OnePlusOnePlusOne
  imports Main
begin

definition plus_one :: "int \<Rightarrow> int" where
"plus_one x = x + 1"

lemma One_plus_one_plus_one: "plus_one (plus_one 1) = 3"
  unfolding plus_one_def
  by simp

end
