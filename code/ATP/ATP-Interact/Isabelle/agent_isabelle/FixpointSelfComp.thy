theory FixpointSelfComp
  imports Main
begin

definition Zcomp :: "(int \<Rightarrow> int) \<Rightarrow> (int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
"Zcomp f g x = f (g x)"

definition is_fixpoint :: "(int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> bool" where
"is_fixpoint f x = (f x = x)"

theorem fixpoint_self_comp: 
  assumes "is_fixpoint f x"
  shows "is_fixpoint (Zcomp f f) x"
proof -
  (* 显式展开 is_fixpoint 的定义 *)
  have "f x = x" using assms unfolding is_fixpoint_def by simp
  (* 接下来展开 Zcomp 的定义 *)
  have "Zcomp f f x = f (f x)" unfolding Zcomp_def by simp
  (* 利用 f x = x 的假设 *)
  also have "... = f x" using \<open>f x = x\<close> by simp
  also have "... = x" using \<open>f x = x\<close> by simp
  finally show ?thesis unfolding is_fixpoint_def by simp
qed


end
