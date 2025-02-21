theory SixIsNotPrime
  imports Main
begin

lemma six_is_not_prime: "\<exists>n q. 2 \<le> n \<and> n < 6 \<and> n * q = 6"
proof -
  show "\<exists>n q. 2 \<le> n \<and> n < 6 \<and> n * q = 6"
    by (rule exI[of _ 2], rule exI[of _ 3], simp)
qed

end