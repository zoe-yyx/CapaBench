theory OrAssoc2
  imports Main
begin

theorem or_assoc2:
  assumes "((P \<or> Q) \<or> R)"
  shows "P \<or> (Q \<or> R)"
proof -
  from assms show ?thesis
  proof
    assume "P \<or> Q"
    then show "P \<or> (Q \<or> R)"
    proof
      assume "P"
      then show "P \<or> (Q \<or> R)" by (rule disjI1)
    next
      assume "Q"
      then have "Q \<or> R" by (rule disjI1)
      then show "P \<or> (Q \<or> R)" by (rule disjI2)
    qed
  next
    assume "R"
    then have "Q \<or> R" by (rule disjI2)
    then show "P \<or> (Q \<or> R)" by (rule disjI2)
  qed
qed

end
