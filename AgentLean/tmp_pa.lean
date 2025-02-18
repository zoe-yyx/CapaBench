def Function.iterate {α : Type} (f : α → α) : Nat → α → α
| 0,     x => x
| n + 1, x => f (Function.iterate f n x)

theorem iterate_S {A : Type} (n : Nat) (f : A → A) (x : A) :
  Function.iterate f n (f x) = Function.iterate f (n + 1) x := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [iterate_S, iterate]
    rw [ih]
    rw [iterate]
