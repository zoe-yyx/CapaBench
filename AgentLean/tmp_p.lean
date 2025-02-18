theorem Function.iterate {α : Type} (f : α → α) (n : Nat) (x : α) : α := 
  if n = 0 then x else f (Function.iterate f (n-1) x)

theorem iterate_S {A : Type} (n : Nat) (f : A → A) (x : A) :
  Function.iterate f n (f x) = Function.iterate f (n + 1) x := by
  induction n with
  | zero => 
    show Function.iterate f 0 (f x) = f x = Function.iterate f 1 x by
      refine eq.trans (Function.iterate f 0 (f x) = f x) _
      rw [Function.iterate]
      simp [Function.iterate]
  | succ m IH => 
    show Function.iterate f (m + 1) (f x) = Function.iterate f (m + 2) x by
      rw [Function.iterate]
      simp [Function.iterate]
      rw [IH]
      simp [Function.iterate]
      rfl

theorem iterate_S' : ∀ (n : Nat) (f : Nat → Nat) (x : Nat), 
  Function.iterate f n x = Function.iterate f (n + 1) x := by
  induction n with
  | zero => 
    show Function.iterate f 0 x = f x = Function.iterate f 1 x by
      refine eq.trans (Function.iterate f 0 x = f x) _
      rw [Function.iterate]
      simp [Function.iterate]
  | succ m IH => 
    show Function.iterate f (m + 1) x = Function.iterate f (m + 2) x by
      rw [Function.iterate]
      simp [Function.iterate]
      rw [IH]
      simp [Function.iterate]
      rfl

theorem iterate_S'' : ∀ (n : Nat) (f : Nat → Nat) (x : Nat), 
  Function.iterate f n (f x) = Function.iterate f (n + 1) x := by
  intro n
  intro f
  intro x
  induction n with
  | zero => 
    show Function.iterate f 0 (f x) = f x = Function.iterate f 1 x by
      refine eq.trans (Function.iterate f 0 (f x) = f x) _
      rw [Function.iterate]
      simp [Function.iterate]
  | succ m IH => 
    show Function.iterate f (m + 1) (f x) = Function.iterate f (m + 2) x by
      rw [Function.iterate]
      simp [Function.iterate]
      rw [IH]
      simp [Function.iterate]
      rfl

theorem iterate_S''' : ∀ (n : Nat) (f : Nat → Nat) (x : Nat), 
  Function.iterate f n (f x) = Function.iterate f (n + 1) x := by
  induction n with
  | zero => 
    show Function.iterate f 0 (f x) = f x = Function.iterate f 1 x by
      refine eq.trans (Function.iterate f 0 (f x) = f x) _
      rw [Function.iterate]
      simp [Function.iterate]
  | succ m IH => 
    show Function.iterate f (m + 1) (f x) = Function.iterate f (m + 2) x by
      rw [Function.iterate]
      simp [Function.iterate]
      rw [IH]
      simp [Function.iterate]
      rfl

theorem iterate_S'''' : ∀ (n : Nat) (f : Nat → Nat) (x : Nat), 
  Function.iterate f n (f x) = Function.iterate f (n + 1) x := by
  induction n with
  | zero => 
    show Function.iterate f 0 (f x) = f x = Function.iterate f 1 x by
      refine eq.trans (Function.iterate f 0 (f x) = f x) _
      rw [Function.iterate]
      simp [Function.iterate]
  | succ m IH => 
    show Function.iterate f (m + 1) (f x) = Function.iterate f (m + 2) x by
      rw [Function.iterate]
      simp [Function.iterate]
      rw [IH]
      simp [Function.iterate]
      rfl

