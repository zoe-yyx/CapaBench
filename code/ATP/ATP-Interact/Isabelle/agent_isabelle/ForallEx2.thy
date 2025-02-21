theory ForallEx2
  imports Main
begin

lemma forall_ex2:
  assumes "\<forall>x. P x \<and> Q x \<longrightarrow> R x"
  shows "\<forall>x. P x \<longrightarrow> Q x \<longrightarrow> R x"
proof (rule allI, rule impI, rule impI)
  fix x
  assume "P x" and "Q x"
  from assms have "\<forall>x. P x \<and> Q x \<longrightarrow> R x" by simp
  then have "P x \<and> Q x \<longrightarrow> R x" by simp
  from `P x` and `Q x` have "P x \<and> Q x" by simp
  with `P x \<and> Q x \<longrightarrow> R x` show "R x" by simp
qed

end
