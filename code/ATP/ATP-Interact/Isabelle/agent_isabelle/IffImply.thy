theory IffImply
  imports Main
begin
  
lemma iff_imply: "(P \<longleftrightarrow> Q) \<Longrightarrow> (P \<longrightarrow> Q)"
proof -
  assume H: "P \<longleftrightarrow> Q"
  show "P \<longrightarrow> Q"
  proof
    assume "P"
    from H have "P \<Longrightarrow> Q" by (rule iffD1)
    then show "Q" using \<open>P\<close> by (rule mp)
  qed
qed

end