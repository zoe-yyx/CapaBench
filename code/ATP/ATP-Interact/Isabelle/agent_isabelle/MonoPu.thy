theory MonoPu
  imports Main 
begin

(* 定义单调性 *)
definition mono :: "(int \<Rightarrow> int) \<Rightarrow> bool" where
  "mono f \<equiv> \<forall>n m. n \<le> m \<longrightarrow> f n \<le> f m"

(* 定义 shift_up1 函数 *)
definition shift_up1 :: "(int \<Rightarrow> int) \<Rightarrow> int \<Rightarrow> int" where
  "shift_up1 f x \<equiv> f x + 1"

(* 定义命题在 shift_up1 下保持 *)
definition preserved_by_shifting_up :: "((int \<Rightarrow> int) \<Rightarrow> bool) \<Rightarrow> bool" where
  "preserved_by_shifting_up P \<equiv> \<forall>f. P f \<longrightarrow> P (shift_up1 f)"

(* 证明单调性在 shift_up1 下保持 *)
lemma mono_pu: "preserved_by_shifting_up mono"
  unfolding preserved_by_shifting_up_def mono_def shift_up1_def
  by auto

end
