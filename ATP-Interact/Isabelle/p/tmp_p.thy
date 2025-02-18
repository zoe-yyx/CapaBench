theory tmp_p
  imports Main
begin

(* 定义单调性 *)
definition mono :: "(int \<Rightarrow> int) \<Rightarrow> bool" where
  "mono f \<equiv> \<forall>n m. n \<le> m \<longrightarrow> f n \<le> f m"

(* 证明常数函数是单调的 *)
lemma const_mono: "\<forall>a. mono (\<lambda>x. a)"
proof -
  fix a
  show "mono (\<lambda>x. a)"
  proof
    fix n m
    assume "n \<le> m"
    show "(\<lambda>x. a) n \<le> (\<lambda>x. a) m"
      by (auto simp add: mono_def)
  qed
qed
end
