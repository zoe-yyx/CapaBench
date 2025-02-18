Require Import Coq.Arith.PeanoNat.
  Theorem iter_S: forall {A: Type} (n: nat) (f: A -> A) (x: A),   Nat.iter n f (f x) = Nat.iter (S n) f x. 
(Definition iter_S_helper (m: nat) (f: A -> A) (x: A) : Nat.iter m f (f x) = Nat.iter (S m) f x := 
  match m with 
    | O => eq_refl 
    | S n => 
      rewrite Nat.iter_S with (n := n) (f := f) (x := f x); 
      rewrite <- iter_S_helper with (m := n) (f := f) (x := f x); 
      reflexivity 
  end.)