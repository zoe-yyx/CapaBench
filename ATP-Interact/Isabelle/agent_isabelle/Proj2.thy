theory Proj2
  imports Main
begin



lemma proj2:
  fixes P Q :: "bool"
  assumes H: "P \<and> Q"
  shows "Q"
proof -
  from H show "Q" by (rule conjunct2)
qed

end