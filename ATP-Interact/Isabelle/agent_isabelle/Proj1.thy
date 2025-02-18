theory Proj1
  imports Main
begin

lemma proj1:
  fixes P Q :: "bool"
  assumes H: "P \<and> Q"
  shows "P"
proof -
  from H show "P" by (rule conjunct1)
qed

end