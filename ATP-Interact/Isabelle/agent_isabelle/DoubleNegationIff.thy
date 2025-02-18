theory DoubleNegationIff
  imports Main
begin

theorem double_negation_iff: "\<not>\<not>P \<longleftrightarrow> P"
proof
  show "\<not>\<not>P \<longrightarrow> P"
  proof (rule classical)
    assume "\<not>\<not>P"
    show "P"
    proof (rule classical)
      assume "\<not>P"
      thus False using \<open>\<not>\<not>P\<close> by contradiction
    qed
  qed
next
  show "P \<longrightarrow> \<not>\<not>P"
  proof
    assume "P"
    show "\<not>\<not>P"
    proof
      assume "\<not>P"
      thus False using \<open>P\<close> by contradiction
    qed
  qed
qed

end
