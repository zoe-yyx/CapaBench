theory tmp_pr
  imports Main
begin

(* 定义关联性 *)
definition assoc :: "(int \<Rightarrow> int \<Rightarrow> int) \<Rightarrow> bool" where
  "assoc f \<equiv> \<forall> x y z. f x (f y z) = f (f x y) z"

(* 证明乘法的关联性 *)
lemma mult_assoc: "assoc (\<lambda>x y. x * y)"
proof -
  define f where "f \<equiv> \<lambda>x y. x * y"
  have "assoc f"
  proof -
    fix x y z
    have "f x (f y z) = f x (x * y * z)"
      by (simp add: f_def)
    also have "... = f (f x y) z"
      by (simp add: f_def)
    finally show "f x (f y z) = f (f x y) z"
      by simp
  qed
  thus ?thesis by simp
qed
end
