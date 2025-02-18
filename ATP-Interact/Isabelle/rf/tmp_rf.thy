theory tmp_rf
  imports Main
begin

(* 对应 Coq 中的 logic_ex6 事实 *)
theorem logic_ex6:
  assumes "P a0"
  assumes "\<forall>a. P a \<longrightarrow> Q a"
  shows "Q a0"
proof -
  have "P a0 -> Q a0" using assms(2) by blast
  then show ?thesis using assms(1) by (rule mp)
  show ?thesis using `P a0 -> Q a0` and `P a0` by (rule mp)
qed
