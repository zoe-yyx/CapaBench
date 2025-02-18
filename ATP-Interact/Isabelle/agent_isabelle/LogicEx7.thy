theory LogicEx7
  imports Main
begin

(* 对应 Coq 中的 logic_ex7 事实 *)
theorem logic_ex7:
  assumes "\<forall>a. P a \<longrightarrow> Q a \<longrightarrow> False"
  assumes "Q a0"
  shows "\<not> P a0"
proof
  assume "P a0"
  from assms(1) have "P a0 \<longrightarrow> Q a0 \<longrightarrow> False" by simp
  hence "Q a0 \<longrightarrow> False" using `P a0` by blast
  thus False using assms(2) by blast
qed

end
