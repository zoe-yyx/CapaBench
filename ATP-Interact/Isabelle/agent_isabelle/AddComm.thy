theory AddComm
  imports Main
begin

datatype mynat = MyZero ("0") | MySuc mynat

fun myadd :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "myadd MyZero m = m" |
  "myadd (MySuc n) m = MySuc (myadd n m)"

lemma myadd_0_r: "myadd n MyZero = n"
proof (induction n)
  case MyZero
  then show ?case by simp
next
  case (MySuc n)
  then show ?case by simp
qed

lemma myadd_succ_r: "myadd n (MySuc m) = MySuc (myadd n m)"
proof (induction n)
  case MyZero
  then show ?case by simp
next
  case (MySuc n)
  then show ?case by simp
qed

theorem add_comm: "myadd n m = myadd m n"
proof (induction n)
  case MyZero
  then show ?case
    using myadd_0_r by simp
next
  case (MySuc n)
  then have "myadd n m = myadd m n" by simp
  then have "MySuc (myadd n m) = MySuc (myadd m n)" by simp
  then show ?case
    using myadd_succ_r by simp
qed

end
