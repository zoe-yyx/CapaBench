theory ShiftUp1Eq
  imports Main 
begin

(* 定义 shift_up1 函数 *)
definition shift_up1 :: "(int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
  "shift_up1 f x \<equiv> f x + 1"

(* 定义 func_plus 函数 *)
definition func_plus :: "(int \<Rightarrow> int) \<Rightarrow> (int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
  "func_plus f g x \<equiv> f x + g x"

(* 证明 shift_up1 和 func_plus 的等价性 *)
lemma shift_up1_eq: "shift_up1 f = func_plus f (\<lambda>x. 1)"
proof -
  (* 展开定义 *)
  show ?thesis
    unfolding shift_up1_def func_plus_def
    (* 使用 auto 证明 *)
    by auto
qed

end
