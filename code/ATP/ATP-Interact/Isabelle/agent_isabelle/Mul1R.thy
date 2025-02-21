theory Mul1R
  imports Main
begin

datatype mynat = MyZero ("0") | MySuc mynat

fun myadd :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "myadd MyZero m = m" |
  "myadd (MySuc n) m = MySuc (myadd n m)"

fun mymul :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "mymul MyZero m = MyZero" |
  "mymul (MySuc n) m = myadd m (mymul n m)"

theorem mymul_comm: "mymul n m = mymul m n"
  sorry

theorem mymul_1_l: "mymul (MySuc MyZero) n = n"
  sorry

theorem mul_1_r: "mymul n (MySuc MyZero) = n"
proof -
  have "mymul n (MySuc MyZero) = mymul (MySuc MyZero) n" using mymul_comm by simp
  also have "... = n" using mymul_1_l by simp
  finally show ?thesis by assumption
qed

end
