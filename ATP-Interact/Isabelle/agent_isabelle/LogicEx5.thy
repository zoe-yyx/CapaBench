theory LogicEx5
  imports Main
begin

(* 对应 Coq 中的 logic_ex5 事实 *)
theorem logic_ex5:
  assumes "\<forall>a. P a \<longrightarrow> Q a"
  assumes "\<forall>a. P a"
  shows "\<forall>a. Q a"
proof
  fix a
  from assms(1) have "P a \<longrightarrow> Q a" by simp
  from assms(2) have "P a" by simp
  thus "Q a" using `P a \<longrightarrow> Q a` by blast
qed

end
