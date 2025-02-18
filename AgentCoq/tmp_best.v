Require Import Coq.Arith.PeanoNat.
  Theorem iter_S: forall {A: Type} (n: nat) (f: A -> A) (x: A),   Nat.iter n f (f x) = Nat.iter (S n) f x. 
Proof.
  intros A n f x.
  induction n as [|k IHk].
  - simpl. reflexivity.
  - simpl. 
    f_equal.
    apply IHk.
Qed.