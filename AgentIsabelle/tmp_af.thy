theory IffImply
  imports Main
begin
  
lemma iff_imply: "(P \<longleftrightarrow> Q) \<Longrightarrow> (P \<longrightarrow> Q)"
proof
  assume iff: "P \<longleftrightarrow> Q"
  show "P \<longrightarrow> Q"
  proof
    assume P: "P"
    from iff have "(P \<longrightarrow> Q) \<and> (Q \<longrightarrow> P)" by (simp add: iff_def)
    then have "P \<longrightarrow> Q" by simp
    with P show "Q" by simp
  qed
qed

end
