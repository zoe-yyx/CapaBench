theory OrComm
  imports Main
begin

theorem or_comm:
  assumes "P \<or> Q"
  shows "Q \<or> P"
proof -
  from assms show ?thesis
  proof
    assume "P"
    then show "Q \<or> P" by (rule disjI2)
  next
    assume "Q"
    then show "Q \<or> P" by (rule disjI1)
  qed
qed

end
