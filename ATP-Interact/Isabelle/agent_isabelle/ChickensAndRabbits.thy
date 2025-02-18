theory ChickensAndRabbits
  imports Main
begin

lemma chickens_and_rabbits:
  fixes C R :: int
  assumes "C + R = 35"
    and "2 * C + 4 * R = 94"
  shows "C = 23"
proof -
  from assms have "C = 23"
    by arith
  thus ?thesis.
qed

end
