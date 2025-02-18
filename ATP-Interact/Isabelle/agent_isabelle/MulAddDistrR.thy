theory MulAddDistrR
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

theorem mul_add_distr_r: "mymul (myadd n m) p = myadd (mymul n p) (mymul m p)"
proof (induction n)
  case MyZero
  then show ?case by simp
next
  case (MySuc n)
  then show ?case
    using myadd_assoc by (simp add: myadd_assoc)
qed

end
