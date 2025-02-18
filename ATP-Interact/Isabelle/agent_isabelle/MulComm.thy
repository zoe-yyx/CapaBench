theory MulComm
  imports Main
begin

datatype mynat = MyZero ("0") | MySuc mynat

fun myadd :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "myadd MyZero m = m" |
  "myadd (MySuc n) m = MySuc (myadd n m)"

fun mymul :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "mymul MyZero m = MyZero" |
  "mymul (MySuc n) m = myadd m (mymul n m)"

lemma myadd_comm: "myadd n m = myadd m n"
  sorry

lemma mymul_0_r: "mymul n MyZero = MyZero"
  sorry

lemma mymul_succ_r: "mymul n (MySuc m) = myadd (mymul n m) n"
  sorry

theorem mul_comm: "mymul n m = mymul m n"
proof (induction n)
  case MyZero
  then show ?case
    using mymul_0_r by simp
next
  case (MySuc n)
  then show ?case
    using mymul_succ_r myadd_comm by (simp add: mymul_0_r mymul_succ_r)
qed

end
