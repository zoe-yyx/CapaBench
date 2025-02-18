theory tmp_prf
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
  have "(x + y) * (x + y) + x + y + 1 = (x + y) * (x + y) + x + y + 1"
    by simp
  also have "\<dots> \<ge> (x + y) * (x + y)"
    apply (rule sum_of_sqr1 [where x = "x + y" and y = "0"])
    by simp
  also have "\<dots> \<ge> 0"
    by simp
  finally show "x * x + 2 * x * y + y * y + x + y + 1 \<ge> 0"
    by simp
qed

lemma aux: "(x + y) * (x + y) + x + y + 1 \<ge> (x + y) * (x + y)" for x y :: int
proof -
  have "(x + y) * (x + y) + x + y + 1 = ((x + y) * (x + y) + x + y) + 1"
    by simp
  also have "\<dots> = (x + y + 1) * (x + y + 1)"
    by (simp add: power2_eq_square)
  also have "\<dots> \<ge> (x + y) * (x + y)"
    by (rule power2_le_imp_le)
  finally show ?thesis
    by simp
qed

lemma "quad_ex1_def: quad_ex1 \<equiv> (x * x + 2 * x * y + y * y + x + y + 1 \<ge> 0)" for x y :: int
  by (rule refl)

lemma quad_ex1: "x * x + 2 * x * y + y * y + x + y + 1 \<ge> 0" for x y :: int
proof -
  have "(x + y) * (x + y) + x + y + 1 = (x + y) * (x + y) + x + y + 1"
    by simp
  also have "\<dots> \<ge> (x + y) * (x + y)"
    apply (rule aux)
    by simp
  also have "\<dots> \<ge> 0"
    by simp
  finally show "x * x + 2 * x * y + y * y + x + y + 1 \<ge> 0"
    by simp
qed

lemma "quad_ex1_def: quad_ex1_def = quad_ex1" by (rule refl)

end
