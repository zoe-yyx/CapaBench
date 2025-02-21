theory LogicEx6
  imports Main
begin

(* 对应 Coq 中的 logic_ex6 事实 *)
theorem logic_ex6:
  assumes "P a0"
  assumes "\<forall>a. P a \<longrightarrow> Q a"
  shows "Q a0"
proof -
  from assms(2) have "P a0 \<longrightarrow> Q a0" by simp
  from assms(1) have "P a0" by simp
  thus "Q a0" using `P a0 \<longrightarrow> Q a0` by blast
qed

end
