theory SumOfSqr1
  imports Main
begin

lemma sum_of_sqr1:
  fixes x y :: int
  shows "x * x + y * y \<ge> x * y"
proof -
  have "x * x + y * y - x * y \<ge> 0"
    by arith
  thus ?thesis by simp
qed

end
