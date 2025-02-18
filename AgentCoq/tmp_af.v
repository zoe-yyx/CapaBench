Require Import Coq.Arith.PeanoNat.
  Theorem iter_S: forall {A: Type} (n: nat) (f: A -> A) (x: A),   Nat.iter n f (f x) = Nat.iter (S n) f x. 
coq
Lemma iter_S_helper {A: Type} (m: nat) (f: A -> A) (x: A): Nat.iter m f (f x) = Nat.iter (S m) f x.
Proof.
  induction m as [|m IHm].
  - reflexivity.
  - simpl.
    rewrite <- IHm.
    reflexivity.
Qed.
Theorem iter_S: forall {A: Type} (n: nat) (f: A -> A) (x: A),   Nat.iter n f (f x) = Nat.iter (S n) f x.
Proof.
  induction n as [|n IHn].
  - simpl.
    apply iter_S_helper.
  - simpl.
    rewrite IHn.
    apply iter_S_helper.
Qed.