theory FixpointSelfComp23
  imports Main
begin

definition Zcomp :: "(int \<Rightarrow> int) \<Rightarrow> (int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
  "Zcomp f g \<equiv> \<lambda> x. f (g x)"

definition is_fixpoint :: "(int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> bool" where
  "is_fixpoint f x \<equiv> f x = x"

lemma fixpoint_self_comp23:
  assumes "is_fixpoint (Zcomp f f) x"
      and "is_fixpoint (Zcomp f (Zcomp f f)) x"
    shows "is_fixpoint f x"
proof -
  have H1: "f (f x) = x"
    using assms(1) unfolding is_fixpoint_def Zcomp_def by simp
  have H2: "f (f (f x)) = x"
    using assms(2) unfolding is_fixpoint_def Zcomp_def by simp
  have "f x = f (f (f x))"
    using H1 by simp
  also have "... = x"
    using H2 by simp
  finally have "f x = x" .
  thus ?thesis
    unfolding is_fixpoint_def by simp
qed

end
