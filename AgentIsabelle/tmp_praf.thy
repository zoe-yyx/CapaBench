theory NotExists
  imports Main
begin

theorem not_exists: "(\<not> (\<exists>x. P x)) \<Longrightarrow> (\<forall>x. \<not> P x)"
proof
  assume assm: "\<not> (\<exists>x. P x)"
  show "\<forall>x. \<not> P x"
  proof (rule ccontr)
    assume "\<not> (\<forall>x. \<not> P x)"
    then obtain x where "\<not>\<not>P x" by auto
    hence "P x" by simp
    then have "\<exists>x. P x" by auto
    with assm show False by contradiction
  qed
qed

end
