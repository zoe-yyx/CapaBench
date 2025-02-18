theory NotForall
  imports Main
begin

theorem forall_iff:
  assumes "\<forall>x. (P x \<longleftrightarrow> Q x)"
  shows "(\<forall>x. P x) \<longleftrightarrow> (\<forall>x. Q x)"
  using assms by blast

theorem not_exists:
  assumes "\<not> (\<exists>x. P x)"
  shows "\<forall>x. \<not> P x"
  using assms by blast

theorem not_forall:
  assumes "\<not> (\<forall>x. P x)"
  shows "\<exists>x. \<not> P x"
proof -
  have "(\<exists>x. \<not> P x) \<or> (\<not> (\<exists>x. \<not> P x))" by (rule classical)
  thus ?thesis
  proof
    assume "\<exists>x. \<not> P x"
    thus ?thesis by simp
  next
    assume "\<not> (\<exists>x. \<not> P x)"
    then have "\<forall>x. P x"
      using not_exists by blast
    then show ?thesis using assms by blast
  qed
qed

end
