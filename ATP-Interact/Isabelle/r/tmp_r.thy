theory tmp_r
  imports Main
begin

theorem not_or_iff: 
  "\<not> (P \<or> Q) \<longleftrightarrow> (\<not> P \<and> \<not> Q)"
proof -
  have "¬(P ∨ Q) = (¬P ∧ ¬Q)"
  proof
    assume "¬P ∨ ¬Q"
    show "¬P ∧ ¬Q"
    proof
      assume "¬P"
      show "¬Q"
      proof
        assume "Q"
        have "P ∨ Q" by assumption
        have "False" : "P" using `¬P` by simp
        have "False" : "Q" using assumption
        contradiction
        thus "¬Q"
      qed
      thus "¬P ∧ ¬Q" by simp
    next
      assume "¬Q"
      show "¬P"
      proof
        assume "P"
        have "P ∨ Q" by assumption
        have "False" : "Q" using `¬Q` by simp
        have "False" : "P" using assumption
        contradiction
        thus "¬P"
      qed
      thus "¬P ∧ ¬Q" by simp
    qed

    assume "¬P ∧ ¬Q"
    show "¬P ∨ ¬Q"
    proof
      assume "¬P"
      show "¬P ∨ ¬Q" by simp
    next
      assume "¬Q"
      show "¬P ∨ ¬Q" by simp
    qed

    thus ?thesis by simp
  qed

  thus not_or_iff by simp
qed
end
