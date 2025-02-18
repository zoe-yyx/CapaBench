theory AddCancelL
imports Main
begin

datatype mynat = MyZero ("0") | MySuc mynat

fun myadd :: "mynat \<Rightarrow> mynat \<Rightarrow> mynat" where
  "myadd MyZero m = m" |
  "myadd (MySuc n) m = MySuc (myadd n m)"

theorem add_cancel_l: "myadd p n = myadd p m \<longleftrightarrow> n = m"
proof
  show "myadd p n = myadd p m \<Longrightarrow> n = m"
  proof (induction p)
    case MyZero
    then show ?case by simp
  next
    case (MySuc p)
    then have "myadd p n = myadd p m" by simp
    with MySuc.IH show ?case by simp
  qed
next
  show "n = m \<Longrightarrow> myadd p n = myadd p m"
    by simp
qed

end
