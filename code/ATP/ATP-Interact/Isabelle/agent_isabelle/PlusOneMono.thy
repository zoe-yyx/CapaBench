theory PlusOneMono
  imports Main
begin

definition plus_one :: "int \<Rightarrow> int" where
"plus_one x = x + 1"

definition mono :: "(int \<Rightarrow> int) \<Rightarrow> bool" where
"mono f = (\<forall>n m. n \<le> m \<longrightarrow> f n \<le> f m)"

lemma plus_one_mono: "mono plus_one"
  unfolding mono_def plus_one_def
  by (simp add: add_mono)  (* Simplify using the additive monotonicity rule *)

end