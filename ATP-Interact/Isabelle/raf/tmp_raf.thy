
(* Corrected proof script *)
lemma const_mono: "<forall>a. mono (<lambda>x. a)"
proof
  fix a
  show "mono (<lambda>x. a)"
  proof
    fix n m
    assume "n <= m"
    show "(\<lambda>x. a) n <= (\<lambda>x. a) m"
    by simp
  next
  show "(\<lambda>x. a) n <= (\<lambda>x. a) m"
  by simp
  show "a <= a"
  by simp
  show "true"
  by auto
  qed
qed
