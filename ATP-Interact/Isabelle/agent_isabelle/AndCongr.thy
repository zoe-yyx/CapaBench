theory AndCongr
  imports Main
begin

lemma and_congr:
  "((P1 \<longleftrightarrow> P2) \<and> (Q1 \<longleftrightarrow> Q2)) \<longrightarrow> (P1 \<and> Q1 \<longleftrightarrow> P2 \<and> Q2)"
proof
  assume eqs: "(P1 \<longleftrightarrow> P2) \<and> (Q1 \<longleftrightarrow> Q2)"
  then have P_eq: "P1 \<longleftrightarrow> P2" and Q_eq: "Q1 \<longleftrightarrow> Q2" by simp_all
  show "P1 \<and> Q1 \<longleftrightarrow> P2 \<and> Q2"
  proof
    assume "P1 \<and> Q1"
    then have P1: "P1" and Q1: "Q1" by simp_all
    from P_eq P1 have P2: "P2" by (simp add: iffD1)
    from Q_eq Q1 have Q2: "Q2" by (simp add: iffD1)
    from P2 Q2 show "P2 \<and> Q2" by simp
  next
    assume "P2 \<and> Q2"
    then have P2: "P2" and Q2: "Q2" by simp_all
    from P_eq P2 have P1: "P1" by (simp add: iffD2)
    from Q_eq Q2 have Q1: "Q1" by (simp add: iffD2)
    from P1 Q1 show "P1 \<and> Q1" by simp
  qed
qed

end
