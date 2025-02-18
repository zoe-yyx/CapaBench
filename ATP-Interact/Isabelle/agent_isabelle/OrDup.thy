theory OrDup
  imports Main
begin

lemma or_dup: "P \<or> P \<longleftrightarrow> P"
proof
  show "P \<or> P \<Longrightarrow> P" by (erule disjE, assumption+)
next
  show "P \<Longrightarrow> P \<or> P" by (rule disjI1)
qed

end

