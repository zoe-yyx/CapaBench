(HERE IS COMPLETE isabelle CODE)
theory tmp_f
  imports Main
begin

(* 定义关联性 *)
definition assoc :: "(int \<Rightarrow> int \<Rightarrow> int) \<Rightarrow> bool" where
  "assoc f \<equiv> \<forall> x y z. f x (f y z) = f (f x y) z"

(* 定义函数 f *)
definition f where "f x y = x * y"

(* 证明乘法的关联性 *)
lemma assoc_f: "assoc f" proof (unfold assoc_def, safe)
  fix x y z
  show "f x (f y z) = f (f x y) z" by simp
qed

(* 证明 main theorem *)
lemma mult_assoc: "assoc f" proof (rule assoc_f)
  show ?thesis by simp
qed

(*  Move the "definition" command for `f` to the correct position before the "lemma" command for `assoc_f` *)
definition f where "f x y = x * y"

(*  Continue with the proof of `assoc_f` by unfolding the definition of `assoc` and simplifying the formula using the distributive property of multiplication over addition *)
lemma assoc_f: "assoc f" proof (unfold assoc_def, safe)
  fix x y z
  show "f x (f y z) = f (f x y) z" by simp
qed

(*  Conclude that `f` is associative by showing that `f x (f y z) = f (f x y) z` *)
lemma mult_assoc: "assoc f" proof (rule assoc_f)
  show ?thesis by simp
qed

end
