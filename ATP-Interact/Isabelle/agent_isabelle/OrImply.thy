theory OrImply
  imports Main
begin

theorem or_imply: "(P \<or> Q \<longrightarrow> R) \<longleftrightarrow> (P \<longrightarrow> R) \<and> (Q \<longrightarrow> R)"
proof
  assume pq_implies_r: "P \<or> Q \<longrightarrow> R"
  show "(P \<longrightarrow> R) \<and> (Q \<longrightarrow> R)"
  proof
    show "P \<longrightarrow> R"
    proof
      assume P
      then have "P \<or> Q" ..
      from pq_implies_r show R by (rule mp)
    qed
    show "Q \<longrightarrow> R"
    proof
      assume Q
      then have "P \<or> Q" ..
      from pq_implies_r show R by (rule mp)
    qed
  qed
next
  assume conj_pr_qr: "(P \<longrightarrow> R) \<and> (Q \<longrightarrow> R)"
  show "P \<or> Q \<longrightarrow> R"
  proof
    assume "P \<or> Q"
    from conj_pr_qr have pr: "P \<longrightarrow> R" and qr: "Q \<longrightarrow> R" by simp
    from `P \<or> Q` show R
    proof
      assume P
      from pr show R by (rule mp)
    next
      assume Q
      from qr show R by (rule mp)
    qed
  qed
qed

end
