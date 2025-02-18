theory ConstMono
  imports Main
begin

(* Define monotonicity *)
definition mono :: "(int ⇒ int) ⇒ bool" where
  "mono f ≡ ∀n m. n ≤ m ⟶ f n ≤ f m"

(* Prove that constant functions are monotonic *)
lemma const_mono: "∀a. mono (λx. a)"
proof
  fix a
  show "mono (λx. a)"
  unfolding mono_def
  proof
    fix n m
    assume "n ≤ m"
    show "(λx. a) n ≤ (λx. a) m"
      by simp
  qed
qed

end
