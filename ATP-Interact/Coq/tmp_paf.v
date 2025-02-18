Require Import Coq.Arith.PeanoNat.
  Theorem iter_S: forall {A: Type} (n: nat) (f: A -> A) (x: A),   Nat.iter n f (f x) = Nat.iter (S n) f x. 
vbnet
Fixpoint iter_f (n: nat) (f: A -> A) (x: A) : A :=
  match n with
  | 0 => x
  | S n' => f (iter_f n' f x)
  end.
Lemma iter_f_def: forall {A: Type} (n: nat) (f: A -> A) (x: A), Nat.iter n f x = iter_f n f x.
Proof.
  induction n as [|n IHn].
  - simpl. reflexivity.
  - simpl. rewrite IHn. apply f.
Qed.
Theorem iter_S: forall {A: Type} (n: nat) (f: A -> A) (x: A), Nat.iter n f (f x) = Nat.iter (S n) f x.
Proof.
  induction n as [|n IHn].
  - simpl. reflexivity.
  - simpl.
    rewrite <- iter_f_def, <- iter_f_def, IHn.
    apply f.
Qed.