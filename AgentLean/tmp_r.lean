theorem iterate_S {A : Type} (n : Nat) (f : A → A) (x : A) :
  Function.iterate f n (f x) = Function.iterate f (n + 1) x := by
  induction n with
  | zero => rfl
  | succ n IH => simp [Function.iterate, IH]
  simp [Function.iterate]
  rw [Function.iterate, Function.iterate]
  congr
  funext a
  induction a with
  | zero => rfl
  | succ a IH => simp [Function.iterate, IH]
