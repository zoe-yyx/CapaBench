theory LogicEx8
  imports Main
begin

(* 对应 Coq 中的 logic_ex8 事实 *)
theorem logic_ex8:
  assumes "\<forall>a b. P a b \<longrightarrow> Q a b"
  shows "\<forall>a b. \<not> P a b \<or> Q a b"
proof (intro allI)
  fix a b
  show "\<not> P a b \<or> Q a b"
  proof (cases "P a b")
    case True
    then have "Q a b" using assms by blast
    thus "\<not> P a b \<or> Q a b" by simp
  next
    case False
    thus "\<not> P a b \<or> Q a b" by simp
  qed
qed

end

