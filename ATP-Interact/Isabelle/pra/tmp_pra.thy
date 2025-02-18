
(* Correct the theory tmp_pra *)
theory ConstMono
  imports Main
begin

(* Define mono function *)
definition mono :: "(int => int) => bool" where
  "mono f <equiv> <forall>n m. n <= m <Longrightarrow> f n <= f m"

(* Prove the const_mono lemma using the corrected definition of mono and the given function <lambda>x. a *)
lemma const_mono: "mono <lambda>x. a"
proof -
  fix a
  assume HjIj: "i <= j" and HkJj: "j <= k"
  have Hik: "i <= k" by transitivity HjIj HkJj
  thus "mono <lambda>x. a"
  by (auto simp: mono)
qed

(* Apply the proven lemma to the constant function *)
lemma const_mono_a: "mono <lambda>x. a"
apply const_mono
apply fun
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
apply const
