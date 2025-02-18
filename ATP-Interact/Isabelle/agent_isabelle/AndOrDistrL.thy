theory AndOrDistrL
  imports Main
begin

lemma and_or_distr_l:
  "P \<and> (Q \<or> R) \<longleftrightarrow> (P \<and> Q) \<or> (P \<and> R)"
proof
  assume "P \<and> (Q \<or> R)"
  then have P: "P" and QR: "Q \<or> R"
    by auto
  from QR show "(P \<and> Q) \<or> (P \<and> R)"
  proof
    assume Q: "Q"
    have "P \<and> Q" by (simp add: P Q)
    thus ?thesis by simp
  next
    assume R: "R"
    have "P \<and> R" by (simp add: P R)
    thus ?thesis by simp
  qed
next
  assume "(P \<and> Q) \<or> (P \<and> R)"
  then show "P \<and> (Q \<or> R)"
  proof
    assume "P \<and> Q"
    then have P: "P" and Q: "Q"
      by simp_all
    from P Q have "Q \<or> R" by simp
    thus ?thesis by (simp add: P)
  next
    assume "P \<and> R"
    then have P: "P" and R: "R"
      by simp_all
    from P R have "Q \<or> R" by simp
    thus ?thesis by (simp add: P)
  qed
qed

end

