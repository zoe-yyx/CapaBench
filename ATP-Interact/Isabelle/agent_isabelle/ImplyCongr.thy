theory ImplyCongr
  imports Main
begin

lemma imply_congr:
  "((P1 \<longleftrightarrow> P2) \<and> (Q1 \<longleftrightarrow> Q2)) \<longrightarrow> ((P1 \<longrightarrow> Q1) \<longleftrightarrow> (P2 \<longrightarrow> Q2))"
proof
  assume hyps: "(P1 \<longleftrightarrow> P2) \<and> (Q1 \<longleftrightarrow> Q2)"
  then have P_eq: "P1 \<longleftrightarrow> P2" and Q_eq: "Q1 \<longleftrightarrow> Q2" by simp_all
  show "(P1 \<longrightarrow> Q1) \<longleftrightarrow> (P2 \<longrightarrow> Q2)"
  proof
    {
      assume H: "P1 \<longrightarrow> Q1"
      show "P2 \<longrightarrow> Q2"
      proof
        assume P2: "P2"
        with P_eq have P1: "P1" using iffD1 by blast
        from H P1 have Q1: "Q1" by (rule mp)
        from Q_eq Q1 have "Q2" using iffD1 by blast
        thus "Q2" by assumption
      qed
    }
    {
      assume H: "P2 \<longrightarrow> Q2"
      show "P1 \<longrightarrow> Q1"
      proof
        assume P1: "P1"
        with P_eq have P2: "P2" using iffD2 by blast
        from H P2 have Q2: "Q2" by (rule mp)
        from Q_eq Q2 have "Q1" using iffD2 by blast
        thus "Q1" by assumption
      qed
    }
  qed
qed

end

