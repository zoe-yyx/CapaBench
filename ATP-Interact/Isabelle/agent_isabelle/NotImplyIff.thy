theory NotImplyIff
  imports Main
begin

theorem not_imply_iff: "\<not>(P \<longrightarrow> Q) \<longleftrightarrow> (P \<and> \<not>Q)"
proof
  show "\<not>(P \<longrightarrow> Q) \<longrightarrow> (P \<and> \<not>Q)"
  proof
    assume "\<not>(P \<longrightarrow> Q)"
    hence "P" 
      by (rule classical)
    moreover have "\<not>Q"
    proof
      assume "Q"
      hence "P \<longrightarrow> Q" by (rule impI)
      thus False using \<open>\<not>(P \<longrightarrow> Q)\<close> by contradiction
    qed
    ultimately show "P \<and> \<not>Q" by (rule conjI)
  qed
next
  show "(P \<and> \<not>Q) \<longrightarrow> \<not>(P \<longrightarrow> Q)"
  proof
    assume "P \<and> \<not>Q"
    then have "P" and "\<not>Q" by auto
    assume "P \<longrightarrow> Q"
    hence "Q" using \<open>P\<close> by (rule mp)
    thus False using \<open>\<not>Q\<close> by contradiction
  qed
qed

end
