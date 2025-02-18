theory NotOrIff
  imports Main
begin

theorem not_or_iff: 
  "\<not> (P \<or> Q) \<longleftrightarrow> (\<not> P \<and> \<not> Q)"
proof
  -- "证明 \<not> (P \<or> Q) \<Longrightarrow> \<not> P \<and> \<not> Q"
  {
    assume "\<not> (P \<or> Q)"
    hence "\<not> P" 
      by (metis disjI1)
    moreover
    hence "\<not> Q" 
      by (metis disjI2)
    ultimately show "\<not> P \<and> \<not> Q" 
      by simp
  }

  -- "证明 \<not> P \<and> \<not> Q \<Longrightarrow> \<not> (P \<or> Q)"
  {
    assume "\<not> P \<and> \<not> Q"
    then show "\<not> (P \<or> Q)"
      by (metis disjI1 disjI2)
  }
qed

end