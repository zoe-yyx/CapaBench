
(* Corrected theory tmp_af *)
theory ConstMono
  begin
    imports Main

    (* Definition and lemma statements go here *)

    definition f :: int => int where "f x = a"
    constant a :: int

    lemma const_mono: "\<forall>a. mono (\<lambda>x. a)"
    proof
      fix a
      show "mono (\<lambda>x. a)"
      proof
        fix n m
        assume "n <= m"
        then show "(\<lambda>x. a) n <= (\<lambda>x. a) m"
        by (simp add: mono_def)
      qed
    qed
  end

(* Define constant a *)
definition a :: int where "a = 5"

(* Prove const_mono *)
lemma const_mono: "\<forall>a. mono (\<lambda>x. a)"
proof
  fix a
  show "mono (\<lambda>x. a)"
  proof
    fix n m
    assume "n <= m"
    then show "(\<lambda>x. a) n <= (\<lambda>x. a) m"
    by (simp add: mono_def fun_eq_iff)
  qed
qed
