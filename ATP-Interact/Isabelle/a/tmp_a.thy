
(* Completing the definition of the theory *)
theory tmp_a
  imports Main
begin

(* Defining the constant function f as λx. a where a is a constant integer *)
definition f :: int => int where "f x = a"
  fix a

(* Adding the missing begin keyword *)
begin

(* Proving that f is monotonically increasing *)
lemma const_mono: "\<forall>a. mono (\<lambda>x. a)"
proof
  fix n m
  assume "n <= m"
  then show "(\<lambda>x. a) n <= (\<lambda>x. a) m"
  by (simp add: mono_def f_def)
qed
end
end
