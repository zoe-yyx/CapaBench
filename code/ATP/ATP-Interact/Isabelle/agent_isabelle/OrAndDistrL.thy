theory OrAndDistrL
  imports Main
begin

lemma or_and_distr_l:
  "P \<or> (Q \<and> R) \<longleftrightarrow> (P \<or> Q) \<and> (P \<or> R)"
proof
  assume "P \<or> (Q \<and> R)"
  then show "(P \<or> Q) \<and> (P \<or> R)"
  proof
    assume P: "P"
    then have "P \<or> Q" and "P \<or> R" by simp_all
    thus ?thesis by simp
  next
    assume "Q \<and> R"
    then have Q: "Q" and R: "R" by simp_all
    then have "P \<or> Q" and "P \<or> R" by simp_all
    thus ?thesis by simp
  qed
next
  assume "(P \<or> Q) \<and> (P \<or> R)"
  then have PQ: "P \<or> Q" and PR: "P \<or> R" by simp_all
  show "P \<or> (Q \<and> R)"
  proof cases
    assume "P"
    thus ?thesis by simp
  next
    assume "\<not> P"
    with PQ have Q: "Q" by blast
    with PR have R: "R" by blast
    from Q R have "Q \<and> R" by simp
    thus ?thesis by simp
  qed
qed

end
