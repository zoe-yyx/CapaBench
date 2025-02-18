
(* Correcting the original problem by adding the theory tmp_pa *)
theory ConstMono
  imports Main
begin

(* 定义单调性 *)
definition mono :: "(int -> int) -> bool" where
  "mono f <equiv> <forall>n m. n <= m -> f n <= f m"

(* 证明常数函数是单调的 *)
lemma const_mono: "\<forall>a. mono (\<lambda>x. a)"
proof -
  apply mono.
  apply fun.
  apply const.
  apply const_mono_ind.
  apply reflexivity.
  apply transitivity.
  apply const_mono_ind.
  apply (rule const_mono).
qed

(* Acting: Applying the corrected proof *)
apply (rule const_mono)
done
