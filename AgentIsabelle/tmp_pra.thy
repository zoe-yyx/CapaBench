theory SumOfSqrLt
  imports Main
begin

lemma sum_of_sqr_lt: "x < y ⟹ x * x + x * y + y * y > 0"
  for x y :: int
proof (intro impI)
  assume "x < y"
  show "x * x + x * y + y * y > 0"
  proof (cases "y > 0")
    case True
    then show ?thesis by arith
  next
    case False
    then have "y ≤ 0" by simp
    (* We'll handle this case in the next step *)
    oops
  qed
qed

end
