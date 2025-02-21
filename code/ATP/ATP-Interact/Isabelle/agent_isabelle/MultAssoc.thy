theory MultAssoc
  imports Main
begin

(* 定义关联性 *)
definition assoc :: "(int \<Rightarrow> int \<Rightarrow> int) \<Rightarrow> bool" where
  "assoc f \<equiv> \<forall> x y z. f x (f y z) = f (f x y) z"

(* 证明乘法的关联性 *)
lemma mult_assoc: "assoc (\<lambda>x y. x * y)"
  unfolding assoc_def by auto

end

