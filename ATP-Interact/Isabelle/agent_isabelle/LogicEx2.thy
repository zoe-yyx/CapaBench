theory LogicEx2
  imports Main
begin

lemma logic_ex2:
  assumes "P1 \<and> Q1"
  and "P1 \<Longrightarrow> P2"
  and "Q1 \<Longrightarrow> Q2"
  shows "P2 \<and> Q2"
proof -
  from assms(1) have P1 by simp
  from assms(1) have Q1 by simp
  from assms(2) and `P1` have P2 by simp
  from assms(3) and `Q1` have Q2 by simp
  thus "P2 \<and> Q2" by simp
qed

end



