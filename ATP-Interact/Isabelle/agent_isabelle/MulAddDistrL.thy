theory MulAddDistrL
  imports Main
begin

datatype mynat = MyZero ("0") | MySuc mynat

fun myadd :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "myadd MyZero m = m" |
  "myadd (MySuc n) m = MySuc (myadd n m)"

fun mymul :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "mymul MyZero m = MyZero" |
  "mymul (MySuc n) m = myadd m (mymul n m)"

theorem myadd_assoc: "myadd n (myadd m p) = myadd (myadd n m) p"
  by (induction n; simp)

theorem mymul_add_distr_r: "mymul (myadd n m) p = myadd (mymul n p) (mymul m p)"
  by (induction n; simp add: myadd_assoc)

theorem mymul_comm: "mymul n m = mymul m n"
  sorry

theorem mul_add_distr_l: "mymul n (myadd m p) = myadd (mymul n m) (mymul n p)"
proof -
  have "mymul n (myadd m p) = mymul (myadd m p) n" using mymul_comm by simp
  also have "... = myadd (mymul m n) (mymul p n)" by (simp add: mymul_add_distr_r)
  also have "... = myadd (mymul n m) (mymul n p)" using mymul_comm by simp
  finally show ?thesis by simp
qed

end
