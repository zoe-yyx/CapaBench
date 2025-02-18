theory ConstMono
  imports Main
begin

(* 定义单调性 *)
definition mono :: "(int \<Rightarrow> int) \<Rightarrow> bool" where
  "mono f \<equiv> \<forall>n m. n \<le> m \<longrightarrow> f n \<le> f m"

(* 证明常数函数是单调的 *)
lemma const_mono: "\<forall>a. mono (\<lambda>x. a)"
proof
  fix a
  show "mono (\<lambda>x. a)"
    unfolding mono_def
    by auto
qed

end
