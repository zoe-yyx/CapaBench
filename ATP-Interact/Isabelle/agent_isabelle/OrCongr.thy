theory OrCongr
  imports Main
begin

lemma or_congr:
  "((P1 \<longleftrightarrow> P2) \<and> (Q1 \<longleftrightarrow> Q2)) \<longrightarrow> (P1 \<or> Q1 \<longleftrightarrow> P2 \<or> Q2)"
proof
  assume eqs: "(P1 \<longleftrightarrow> P2) \<and> (Q1 \<longleftrightarrow> Q2)"
  then have P_eq: "P1 \<longleftrightarrow> P2" and Q_eq: "Q1 \<longleftrightarrow> Q2" by simp_all
  show "P1 \<or> Q1 \<longleftrightarrow> P2 \<or> Q2"
  proof
    assume "P1 \<or> Q1"
    then show "P2 \<or> Q2"
    proof
      assume "P1"
      then have "P2" using P_eq by (simp add: iffD1)
      thus ?thesis by simp
    next
      assume "Q1"
      then have "Q2" using Q_eq by (simp add: iffD1)
      thus ?thesis by simp
    qed
  next
    assume "P2 \<or> Q2"
    then show "P1 \<or> Q1"
    proof
      assume "P2"
      then have "P1" using P_eq by (simp add: iffD2)
      thus ?thesis by simp
    next
      assume "Q2"
      then have "Q1" using Q_eq by (simp add: iffD2)
      thus ?thesis by simp
    qed
  qed
qed

end
