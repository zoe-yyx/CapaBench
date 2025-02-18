Require Import Coq.Arith.PeanoNat.
  Theorem iter_S: forall {A: Type} (n: nat) (f: A -> A) (x: A),   Nat.iter n f (f x) = Nat.iter (S n) f x. 
| S n => 
  (** Fill in your proof here*)
  rewrite Nat.iter_S, Nat.iter_S