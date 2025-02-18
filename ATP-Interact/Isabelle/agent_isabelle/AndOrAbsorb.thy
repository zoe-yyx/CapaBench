theory AndOrAbsorb
  imports Main
begin

lemma and_or_absorb:
  "P \<and> (P \<or> Q) \<longleftrightarrow> P"
proof
  assume "P \<and> (P \<or> Q)"
  then show "P" by simp
next
  assume P: "P"
  then have "P \<or> Q" by simp
  with P show "P \<and> (P \<or> Q)" by simp
qed

end
