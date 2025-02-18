theory SixIsNotPrime
  imports Main
begin

lemma six_is_not_prime: "∃n q. 2 ≤ n ∧ n < 6 ∧ n * q = 6"
proof (rule exI[of _ 2], rule exI[of _ 3])
  show "2 ≤ 2 ∧ 2 < 6 ∧ 2 * 3 = 6"
  proof (rule conjI)
    show "2 ≤ 2" by simp
  next
    show "2 < 6" by simp
  next
    show "2 * 3 = 6" by simp
  qed
qed

end
