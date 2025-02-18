
(* Remove the transaction wrapper as it is causing the error *)
lemma chickens_and_rabbits:
  fixes C R :: int
  assumes "C + R = 35"
    and "2 * C + 4 * R = 94"
  shows "C = 23"
begin

(* Your proof code goes here *)

end

(* Simplify the given equations *)
have "C = 23" for C:int only if 23 = (35 - R) and 2 * 23 + 4 * R = 94
  by (simp add: arith.simps)

(* Your proof code after simplification goes here *)

end
