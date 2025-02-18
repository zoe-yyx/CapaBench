theory ConstMono
  imports Main
begin

(* Define monotonicity *)
definition mono :: "(int \<Rightarrow> int) \<Rightarrow> bool" where
  "mono f \<equiv> \<forall>n m. n \<le> m \<longrightarrow> f n \<le> f m"

(* Prove that constant functions are monotonic *)
lemma const_mono: "\<forall>a. mono (\<lambda>x. a)"
  unfolding mono_def
  by auto

end
