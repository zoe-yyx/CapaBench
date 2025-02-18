theorem iterate_S {A : Type} (n : Nat) (f : A → A) (x : A) :
  Function.iterate f n (f x) = Function.iterate f (n + 1) x := by
  induction n with
  | zero => simp
  | succ n IH => simp [Function.iterate, IH]
  simp [Function.iterate]
