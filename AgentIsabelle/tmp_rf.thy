theory AddCancelL
imports Main
begin

datatype mynat = MyZero ("0") | MySuc mynat

fun myadd :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "myadd MyZero m = m" |
  "myadd (MySuc n) m = MySuc (myadd n m)"

lemma myadd_zero_left: "myadd MyZero n = n"
  by simp

lemma myadd_Suc: "myadd (MySuc n) m = MySuc (myadd n m)"
  by simp

theorem add_cancel_l: "myadd p n = myadd p m \<longleftrightarrow> n = m"
proof (induct p)
  case MyZero
  then show ?case using myadd_zero_left by simp
next
  case (MySuc k)
  then have "myadd (MySuc k) n = myadd (MySuc k) m" by assumption
  then have "MySuc (myadd k n) = MySuc (myadd k m)" using myadd_Suc by simp
  then show ?case using MySuc.IH by simp
qed

end
