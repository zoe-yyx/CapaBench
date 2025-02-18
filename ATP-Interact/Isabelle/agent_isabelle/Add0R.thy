theory Add0R
  imports Main
begin

datatype mynat = MyZero ("0") | MySuc mynat

fun myadd :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "myadd MyZero m = m" |
  "myadd (MySuc n) m = MySuc (myadd n m)"

lemma add_0_r: "myadd n MyZero = n"
proof (induction n)
  case MyZero
  then show ?case by simp
next
  case (MySuc n)
  then have "myadd n MyZero = n" by simp
  then show ?case by simp
qed

end