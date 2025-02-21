theory MonoCompose
  imports Main
begin

definition mono :: "(int \<Rightarrow> int) \<Rightarrow> bool" where
"mono f = (\<forall>n m. n \<le> m \<longrightarrow> f n \<le> f m)"

definition Zcomp :: "(int \<Rightarrow> int) \<Rightarrow> (int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
"Zcomp f g x = f (g x)"

lemma mono_compose: 
  assumes "mono f" and "mono g"
  shows "mono (Zcomp f g)"
  unfolding mono_def Zcomp_def
proof (clarify)
  fix n m :: int
  assume "n \<le> m"
  hence "g n \<le> g m" using assms(2) unfolding mono_def by blast
  thus "f (g n) \<le> f (g m)" using assms(1) unfolding mono_def by blast
qed

end
