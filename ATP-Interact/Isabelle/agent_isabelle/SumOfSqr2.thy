theory SumOfSqr2
  imports Main
begin

lemma sum_of_sqr2: "x * x + y * y \<ge> 2 * x * y" for x y :: int
proof -
  have "(x - y) * (x - y) \<ge> 0"
    by (simp add: algebra_simps)
  then have "x * x - 2 * x * y + y * y \<ge> 0"
    by (simp add: power2_eq_square algebra_simps)
  then show ?thesis
    by (simp add: algebra_simps)
qed

end
