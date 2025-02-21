theory MulSuccR
  imports Main
begin

datatype mynat = MyZero ("0") | MySuc mynat

fun myadd :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "myadd MyZero m = m" |
  "myadd (MySuc n) m = MySuc (myadd n m)"

fun mymul :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "mymul MyZero m = MyZero" |
  "mymul (MySuc n) m = myadd m (mymul n m)"

lemma myadd_succ_r: "myadd n (MySuc m) = MySuc (myadd n m)"
  by (induction n; simp)

theorem myadd_assoc: "myadd n (myadd m p) = myadd (myadd n m) p"
  by (induction n; simp)

lemma mul_succ_r: "mymul n (MySuc m) = myadd (mymul n m) n"
proof (induction n)
  case MyZero
  then show ?case by simp
next
  case (MySuc n)
  then show ?case 
    using myadd_succ_r myadd_assoc by simp
qed

end
