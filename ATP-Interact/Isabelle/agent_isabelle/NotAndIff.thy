theory NotAndIff
  imports Main
begin

theorem not_and_iff: "\<not> (P \<and> Q) \<longleftrightarrow> (\<not> P \<or> \<not> Q)"
proof
  show "\<not> (P \<and> Q) \<longrightarrow> (\<not> P \<or> \<not> Q)"
  proof
    assume "\<not> (P \<and> Q)"
    show "\<not> P \<or> \<not> Q"
    proof (rule classical)
      assume "\<not> (\<not> P \<or> \<not> Q)"
      hence "P \<and> Q" by (metis (no_types, lifting) classical)
      thus False using `\<not> (P \<and> Q)` by contradiction
    qed
  qed
next
  show "(\<not> P \<or> \<not> Q) \<longrightarrow> \<not> (P \<and> Q)"
  proof
    assume "\<not> P \<or> \<not> Q"
    show "\<not> (P \<and> Q)"
    proof
      assume "P \<and> Q"
      then obtain P and Q by auto
      thus False using `\<not> P \<or> \<not> Q` by auto
    qed
  qed
qed

end
