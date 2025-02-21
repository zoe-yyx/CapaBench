theory AddCancelR
  imports Main
begin

datatype mynat = MyZero ("0") | MySuc mynat

fun myadd :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "myadd MyZero m = m" |
  "myadd (MySuc n) m = MySuc (myadd n m)"

theorem myadd_comm: "myadd n m = myadd m n"
  sorry

lemma myadd_cancel_l: "myadd p n = myadd p m \<longleftrightarrow> n = m"
  sorry

theorem add_cancel_r: "myadd n p = myadd m p \<longleftrightarrow> n = m"
proof
  assume "myadd n p = myadd m p"
  then have "myadd p n = myadd p m" using myadd_comm by simp
  then show "n = m" using myadd_cancel_l by simp
next
  assume "n = m"
  then show "myadd n p = myadd m p" by simp
qed

end
