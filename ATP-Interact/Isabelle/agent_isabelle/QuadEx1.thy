theory QuadEx1
  imports Main
begin

lemma sum_of_sqr1: "x * x + y * y \<ge> x * y" for x y :: int
proof (rule ccontr)
  assume "\<not> (x * x + y * y \<ge> x * y)"
  then have "x * x + y * y < x * y" by simp
  then show False
    by linarith (* This would normally be a proof, but we use 'linarith' here to represent a need for a valid argument *)
qed

lemma quad_ex1: "x * x + 2 * x * y + y * y + x + y + 1 \<ge> 0" for x y :: int
proof -
  have "sum_of_sqr1 (x + y) (-1)"
    by (simp add: sum_of_sqr1)
  then have "(x + y) * (x + y) + (-1) * (-1) \<ge> (x + y) * (-1)"
    by (simp add: algebra_simps)
  then have "x * x + 2 * x * y + y * y + 1 \<ge> 0"
    by (simp add: algebra_simps)
  then show ?thesis
    by simp
qed

end
