theory IterS
  imports Main
begin

fun iter :: "nat \<Rightarrow> ('a \<Rightarrow> 'a) \<Rightarrow> 'a \<Rightarrow> 'a" where
  "iter 0 f x = x" |
  "iter (Suc n) f x = f (iter n f x)"

theorem iter_S: "iter n f (f x) = iter (Suc n) f x"
proof (induction n)
  case 0
  then show ?case by simp
next
  case (Suc n)
  then show ?case by simp
qed

end
