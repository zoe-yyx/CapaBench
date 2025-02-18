theory AddSuccR
  imports Main
begin

datatype mynat = MyZero ("0") | MySuc mynat

fun myadd :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "myadd MyZero m = m" |
  "myadd (MySuc n) m = MySuc (myadd n m)"

lemma add_succ_r: "myadd n (MySuc m) = MySuc (myadd n m)"
proof (induction n)
  case MyZero
  then show ?case by simp
next
  case (MySuc n)
  then show ?case by simp
qed

end