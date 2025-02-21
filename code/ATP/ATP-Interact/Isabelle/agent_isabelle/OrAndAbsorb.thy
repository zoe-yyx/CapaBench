theory OrAndAbsorb
  imports Main
begin

lemma or_and_absorb:
  "P \<or> (P \<and> Q) \<longleftrightarrow> P"
proof
  assume "P \<or> (P \<and> Q)"
  then show "P"
  proof
    assume "P"
    thus ?thesis by assumption
  next
    assume "P \<and> Q"
    then show "P" by simp
  qed
next
  assume P: "P"
  then show "P \<or> (P \<and> Q)" by simp
qed

end
