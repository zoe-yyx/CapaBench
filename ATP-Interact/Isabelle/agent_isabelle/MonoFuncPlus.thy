theory MonoFuncPlus
  imports Main
begin

definition mono :: "(int \<Rightarrow> int) \<Rightarrow> bool" where
  "mono f \<equiv> \<forall> n m. n \<le> m \<longrightarrow> f n \<le> f m"

definition func_plus :: "(int \<Rightarrow> int) \<Rightarrow> (int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
  "func_plus f g \<equiv> \<lambda> x. f x + g x"

lemma mono_func_plus:
  assumes "mono f"
      and "mono g"
  shows "mono (func_plus f g)"
proof -
  have "mono (\<lambda> x. f x + g x)"
  proof (unfold mono_def, intro allI impI)
    fix n m :: int
    assume Hnm: "n \<le> m"
    from assms(1) have Hf_mono: "f n \<le> f m"
      unfolding mono_def by (simp add: Hnm)
    from assms(2) have Hg_mono: "g n \<le> g m"
      unfolding mono_def by (simp add: Hnm)
    then have "f n + g n \<le> f m + g m"
      using Hf_mono Hg_mono by (simp add: add_mono)
    thus "f n + g n \<le> f m + g m" .
  qed
  thus ?thesis
    unfolding func_plus_def by simp
qed

end
