theory tmp_pf imports Main begin

(* 定义单调性 *)
definition mono :: "(int \<Rightarrow> int) \<Rightarrow> bool" where
  "mono f \<equiv> \<forall>n m. n \<le> m \<longrightarrow> f n \<le> f m"

(* 证明常数函数是单调的 *)
lemma const_mono: "\<forall>a. mono (\<lambda>x. a)"
begin
  fix a
  show "mono (\<lambda>x. a)"
  proof -
    show ?thesis
  qed
end

theory ConstMono imports Main begin
  lemma const_mono: "\<forall>a. mono (\<lambda>x. a)"
  proof -
    show ?thesis
  proof
    fix i
    show "mono (\<lambda>x. a)"
      apply (rule monoI)
      apply (rule refl)
      apply (rule sorry)
    done
  qed
end
