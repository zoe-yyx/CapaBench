theory SumOfSqrLt
  imports Main
begin

lemma sum_of_sqr_lt: "x < y \<Longrightarrow> x * x + x * y + y * y > 0"
  for x y :: int
proof -
  assume "x < y"
  hence "(x + y) * (x + y) > 0"
    by (metis add_less_mono zero_less_power2)
  thus "x * x + x * y + y * y > 0"
    using `x < y` by (simp add: power2_eq_square algebra_simps)
qed

end
