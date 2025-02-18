theory tmp_praf
  imports Main
begin

theorem or_imply: "(P \<or> Q \<longrightarrow> R) \<longleftrightarrow> (P \<longrightarrow> R) \<and> (Q \<longrightarrow> R)"
  proof
    assume "P \<or> Q \<longrightarrow> R"
    show "(P \<longrightarrow> R) \<and> (Q \<longrightarrow> R)"
    proof cases
      case True
        assume P
        with `P \<or> Q \<longrightarrow> R` show R by (rule mp)
      case False
        assume Q
        with `P \<or> Q \<longrightarrow> R` show R by (rule mp)
    qed
  next
    assume "(P \<longrightarrow> R) \<and> (Q \<longrightarrow> R)"
    show "P \<or> Q \<longrightarrow> R"
    proof cases
      case True
        assume P
        with "(P \<longrightarrow> R) \<and> (Q \<longrightarrow> R)" show R by (rule mp)
      case False
        assume Q
        with "(P \<longrightarrow> R) \<and> (Q \<longrightarrow> R)" show R by (rule mp)
    qed
qed

end