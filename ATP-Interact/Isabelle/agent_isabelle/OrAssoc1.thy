theory OrAssoc1
  imports Main
begin

theorem or_assoc1:
  assumes "P \<or> (Q \<or> R)"
  shows "(P \<or> Q) \<or> R"
proof -
  from assms show ?thesis
  proof
    assume "P"
    then have "P \<or> Q" by (rule disjI1)
    then show "(P \<or> Q) \<or> R" by (rule disjI1)
  next
    assume "Q \<or> R"
    then show "(P \<or> Q) \<or> R"
    proof
      assume "Q"
      then have "P \<or> Q" by (rule disjI2)
      then show "(P \<or> Q) \<or> R" by (rule disjI1)
    next
      assume "R"
      then show "(P \<or> Q) \<or> R" by (rule disjI2)
    qed
  qed
qed

end
