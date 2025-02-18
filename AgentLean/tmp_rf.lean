theorem iterate_S {A : Type} (n : Nat) (f : A → A) (x : A) :
  Function.iterate f n (f x) = Function.iterate f (n + 1) x := by
  induction n with
  | zero => simp
  | succ n IH =>
    have h : Function.iterate f 0 (f x) = f x, from rfl,
    have h' : Function.iterate f (n + 1) x = f (Function.iterate f n x), from rfl,
    simp [Function.iterate, h, h']
