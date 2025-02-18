theory Mul1L
  imports Main
begin

datatype mynat = MyZero ("0") | MySuc mynat

fun myadd :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "myadd MyZero m = m" |
  "myadd (MySuc n) m = MySuc (myadd n m)"

fun mymul :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "mymul MyZero m = MyZero" |
  "mymul (MySuc n) m = myadd m (mymul n m)"

lemma myadd_0_r: "myadd n MyZero = n"
  sorry

theorem mul_1_l: "mymul (MySuc MyZero) n = n"
proof -
  have "mymul (MySuc MyZero) n = myadd n (mymul MyZero n)" by simp
  also have "... = myadd n MyZero" by simp
  also have "... = n" using myadd_0_r by simp
  finally show ?thesis by assumption
qed

end
