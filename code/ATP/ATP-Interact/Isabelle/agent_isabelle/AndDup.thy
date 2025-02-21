theory AndDup
  imports Main
begin

lemma and_dup: "P \<and> P \<longleftrightarrow> P"
proof
  show "P \<and> P \<Longrightarrow> P" by (erule conjE)
next
  show "P \<Longrightarrow> P \<and> P" by (rule conjI)
qed


end
