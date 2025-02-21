theory AndComm
  imports Main
begin


theorem and_comm:
  fixes P Q :: "bool"
  assumes H: "P \<and> Q"
  shows "Q \<and> P"
proof -
  from H have "P" by (rule conjunct1)
  from H have "Q" by (rule conjunct2)
  show "Q \<and> P" using `Q` `P` by (rule conjI)
qed

end