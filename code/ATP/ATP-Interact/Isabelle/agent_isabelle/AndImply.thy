theory AndImply
  imports Main
begin

lemma and_imply:
  "((P \<and> Q \<longrightarrow> R) \<longleftrightarrow> (P \<longrightarrow> Q \<longrightarrow> R))"
proof
  {
    assume H: "P \<and> Q \<longrightarrow> R"
    show "P \<longrightarrow> Q \<longrightarrow> R"
    proof (rule impI)+
      assume P: "P" and Q: "Q"
      from H have "P \<and> Q \<longrightarrow> R" by assumption
      from this have R: "R" using P Q by auto
      thus "R" by assumption
    qed
  }
  {
    assume H: "P \<longrightarrow> Q \<longrightarrow> R"
    show "P \<and> Q \<longrightarrow> R"
    proof
      assume conj: "P \<and> Q"
      from conj have P: "P" and Q: "Q" by simp_all
      from H P Q show "R" by simp
    qed
  }
qed

end
