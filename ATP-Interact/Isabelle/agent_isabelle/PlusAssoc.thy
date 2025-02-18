theory PlusAssoc
  imports Main
begin


(* 定义关联性（associativity） *)
definition assoc :: "(int \<Rightarrow> int \<Rightarrow> int) \<Rightarrow> bool" where
  "assoc f \<longleftrightarrow> (\<forall>x y z. f x (f y z) = f (f x y) z)"

(* 证明加法是关联的 *)
lemma plus_assoc: "assoc (\<lambda>x y. x + y)"
proof -
  (* 展开定义 *)
  have "\<forall>x y z. (x + (y + z)) = ((x + y) + z)" 
    by auto
  thus ?thesis 
    unfolding assoc_def
    by auto
qed

end