theorem logicEx2 (P1 Q1 P2 Q2 : Prop) :
  P1 ∧ Q1 →
  (P1 → P2) →
  (Q1 → Q2) →
  P2 ∧ Q2 := by
  assume h1 : P1 ∧ Q1
  have h2 : P1, from h1.left
  have h3 : P2, from h2.trans (show P1 → P2, from assumption)
  have h4 : Q1, from h1.right
  have h5 : Q2, from h4.trans (show Q1 → Q2, from assumption)
  show P2 ∧ Q2, from and.intro h3 h5
